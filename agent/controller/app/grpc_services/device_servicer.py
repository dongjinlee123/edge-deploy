"""Real DeviceManagement gRPC servicer — ports controller/app/routers/devices.py."""
import logging
from datetime import datetime

import grpc

from app.database import async_session_factory
from app.models import Device
from app.services.stream_manager import stream_manager
from sqlmodel import select

try:
    from edgedeploy.v1 import device_management_pb2, device_management_pb2_grpc
    from edgedeploy.v1.common_pb2 import Labels
    from google.protobuf.timestamp_pb2 import Timestamp
    _STUBS_AVAILABLE = True
except ImportError:
    device_management_pb2 = None  # type: ignore
    device_management_pb2_grpc = None  # type: ignore
    _STUBS_AVAILABLE = False

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Conversion helpers
# ---------------------------------------------------------------------------

def _ts(dt: datetime | None) -> "Timestamp":
    ts = Timestamp()
    if dt:
        ts.FromDatetime(dt)
    return ts


def _to_proto(d: Device) -> "device_management_pb2.DeviceProto":
    return device_management_pb2.DeviceProto(
        id=d.id,
        name=d.name,
        address=d.address,
        agent_port=d.agent_port,
        status=d.status,
        last_seen=_ts(d.last_seen),
        labels=Labels(values=d.labels or {}),
        created_at=_ts(d.created_at),
        device_uuid=d.device_uuid or "",
    )


# ---------------------------------------------------------------------------
# Servicer
# ---------------------------------------------------------------------------

class DeviceManagementServicer:
    async def ListDevices(self, request, context):
        async with async_session_factory() as session:
            result = await session.execute(select(Device))
            devices = result.scalars().all()
        return device_management_pb2.ListDevicesResponse(
            devices=[_to_proto(d) for d in devices]
        )

    async def GetDevice(self, request, context):
        async with async_session_factory() as session:
            device = await session.get(Device, request.id)
        if not device:
            await context.abort(grpc.StatusCode.NOT_FOUND, f"Device {request.id} not found")
            return
        return _to_proto(device)

    async def CreateDevice(self, request, context):
        async with async_session_factory() as session:
            device = Device(
                name=request.name,
                address=request.address,
                agent_port=request.agent_port or 30080,
                labels=dict(request.labels.values) if request.HasField("labels") else None,
            )
            session.add(device)
            await session.commit()
            await session.refresh(device)
        return _to_proto(device)

    async def UpdateDevice(self, request, context):
        async with async_session_factory() as session:
            device = await session.get(Device, request.id)
            if not device:
                await context.abort(grpc.StatusCode.NOT_FOUND, f"Device {request.id} not found")
                return
            if request.name:
                device.name = request.name
            if request.address:
                device.address = request.address
            if request.agent_port:
                device.agent_port = request.agent_port
            if request.HasField("labels"):
                device.labels = dict(request.labels.values)
            session.add(device)
            await session.commit()
            await session.refresh(device)
        return _to_proto(device)

    async def DeleteDevice(self, request, context):
        async with async_session_factory() as session:
            device = await session.get(Device, request.id)
            if not device:
                await context.abort(grpc.StatusCode.NOT_FOUND, f"Device {request.id} not found")
                return
            await session.delete(device)
            await session.commit()
        return device_management_pb2.DeleteDeviceResponse(ok=True)

    async def PingDevice(self, request, context):
        async with async_session_factory() as session:
            device = await session.get(Device, request.id)
        if not device:
            await context.abort(grpc.StatusCode.NOT_FOUND, f"Device {request.id} not found")
            return
        reachable = stream_manager.is_connected(device.id)
        return device_management_pb2.PingDeviceResponse(
            reachable=reachable,
            message="online" if reachable else "offline",
        )


def add_to_server(server) -> None:
    if not _STUBS_AVAILABLE:
        logger.warning("DeviceManagement stubs not found — run `make proto-python`")
        return
    device_management_pb2_grpc.add_DeviceManagementServicer_to_server(
        DeviceManagementServicer(), server
    )
