"""Background task: mark devices without an active gRPC stream as offline.

Devices connected via bidi stream get status updates from heartbeats directly
(in edge_control_servicer), so they are kept online automatically.
"""
import asyncio
import logging

from app.config import settings
from app.database import async_session_factory
from app.models import Device
from app.services.stream_manager import stream_manager
from sqlmodel import select

logger = logging.getLogger(__name__)


async def run_health_monitor():
    logger.info("Health monitor started (interval=%ds)", settings.health_poll_interval)
    while True:
        try:
            async with async_session_factory() as session:
                all_devices = (await session.execute(select(Device))).scalars().all()

            offline_devices = [d for d in all_devices if not stream_manager.is_connected(d.id)]

            if offline_devices:
                async with async_session_factory() as session:
                    for device in offline_devices:
                        device.status = "offline"
                        session.add(device)
                    await session.commit()

        except Exception as exc:
            logger.error("Health monitor error: %s", exc)

        await asyncio.sleep(settings.health_poll_interval)
