"""Per-device desired-config versioning.

config_version is a monotonically increasing integer stored on the Device row.
Every time the desired state changes (deployment applied or stopped) the version
is bumped.  When an agent reconnects it sends its cached version; if it is stale
the controller pushes the full desired config via ConfigSyncCommand.
"""
import json
import logging

from app.database import async_session_factory
from app.models import Deployment, Device
from sqlmodel import select

logger = logging.getLogger(__name__)


async def get_config_version(device_id: int) -> int:
    """Return the current config_version for a device (0 if not set)."""
    async with async_session_factory() as session:
        device = await session.get(Device, device_id)
        return device.config_version if device else 0


async def bump_config_version(device_id: int) -> int:
    """Increment config_version by 1 and return the new value."""
    async with async_session_factory() as session:
        device = await session.get(Device, device_id)
        if not device:
            return 0
        device.config_version = (device.config_version or 0) + 1
        session.add(device)
        await session.commit()
        new_version = device.config_version
    logger.debug("config_version bumped → %d for device_id=%d", new_version, device_id)
    return new_version


async def get_desired_config(device_id: int) -> dict:
    """Return the full desired state for a device.

    Includes all deployments whose status is 'running'.  This dict is
    JSON-serialised and sent to the agent as ConfigSyncCommand.desired_config_json.
    """
    async with async_session_factory() as session:
        result = await session.execute(
            select(Deployment)
            .where(Deployment.device_id == device_id)
            .where(Deployment.status == "running")
        )
        deployments = result.scalars().all()

    return {
        "deployments": [
            {
                "id": d.id,
                "namespace": d.namespace,
                "manifests": d.manifests,
            }
            for d in deployments
        ]
    }
