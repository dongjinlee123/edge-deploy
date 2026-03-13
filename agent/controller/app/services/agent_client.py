"""Controller-side client for edge agents.

Sends commands via the active gRPC bidi stream.
"""
import json
import logging
import uuid

from app.config import settings
from app.models import Device
from app.services.stream_manager import stream_manager

logger = logging.getLogger(__name__)

TIMEOUT = settings.agent_timeout


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _cmd_id() -> str:
    return str(uuid.uuid4())


async def _grpc(device: Device, command) -> dict:
    return await stream_manager.send_command(device.id, command, timeout=TIMEOUT)


def _grpc_cmd():
    """Lazy import so the module loads even before proto stubs are generated."""
    from edgedeploy.v1 import edge_control_pb2  # noqa: PLC0415
    return edge_control_pb2


# ---------------------------------------------------------------------------
# Public API  (device: Device is now always the first argument)
# ---------------------------------------------------------------------------

async def apply_manifests(device: Device, manifests: str, namespace: str = "default") -> dict:
    pb2 = _grpc_cmd()
    cmd = pb2.EdgeCommand(
        command_id=_cmd_id(),
        apply_manifests=pb2.ApplyManifestsCommand(
            manifests=manifests, namespace=namespace
        ),
    )
    return await _grpc(device, cmd)


async def delete_resource(device: Device, namespace: str, kind: str, name: str) -> dict:
    pb2 = _grpc_cmd()
    cmd = pb2.EdgeCommand(
        command_id=_cmd_id(),
        delete_resource=pb2.DeleteResourceCommand(
            namespace=namespace, kind=kind, name=name
        ),
    )
    return await _grpc(device, cmd)


async def restart_deployment(device: Device, namespace: str, name: str) -> dict:
    pb2 = _grpc_cmd()
    cmd = pb2.EdgeCommand(
        command_id=_cmd_id(),
        restart_deployment=pb2.RestartDeploymentCommand(
            namespace=namespace, name=name
        ),
    )
    return await _grpc(device, cmd)


async def get_resources(device: Device, namespace: str) -> dict:
    pb2 = _grpc_cmd()
    cmd = pb2.EdgeCommand(
        command_id=_cmd_id(),
        get_resources=pb2.GetResourcesCommand(namespace=namespace),
    )
    result = await _grpc(device, cmd)
    return result if isinstance(result, dict) else json.loads(result)


async def get_pod_logs(device: Device, namespace: str, pod_name: str, tail: int = 200) -> str:
    pb2 = _grpc_cmd()
    cmd = pb2.EdgeCommand(
        command_id=_cmd_id(),
        get_pod_logs=pb2.GetPodLogsCommand(
            namespace=namespace, pod_name=pod_name, tail=tail
        ),
    )
    result = await _grpc(device, cmd)
    return result if isinstance(result, str) else str(result)
