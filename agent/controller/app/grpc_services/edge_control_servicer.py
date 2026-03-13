"""Real implementation of EdgeControl.CommandStream().

Phase 2: bidi stream registration, heartbeat → status updates, command ack routing.
Phase 5: config_version check on connect → ConfigSyncCommand when agent is stale.
"""
import asyncio
import json
import logging
import uuid
from datetime import datetime

from app.database import async_session_factory
from app.models import Device
from app.services import config_store
from app.services.stream_manager import stream_manager
from sqlmodel import select

try:
    from edgedeploy.v1 import edge_control_pb2, edge_control_pb2_grpc
    _STUBS_AVAILABLE = True
except ImportError:
    edge_control_pb2 = None  # type: ignore
    edge_control_pb2_grpc = None  # type: ignore
    _STUBS_AVAILABLE = False

logger = logging.getLogger(__name__)


class EdgeControlServicer:
    async def CommandStream(self, request_iterator, context):
        device_uuid: str | None = None
        ctx = None
        writer_task = None

        async def _writer():
            try:
                while True:
                    cmd = await ctx.queue.get()
                    await context.write(cmd)
            except asyncio.CancelledError:
                pass
            except Exception as exc:
                logger.error("Stream write error for %s: %s", device_uuid, exc)

        try:
            async for report in request_iterator:
                # ---- Heartbeat ----
                if report.HasField("heartbeat"):
                    hb = report.heartbeat

                    if device_uuid is None:
                        # First heartbeat — register stream.
                        device_uuid = report.device_uuid
                        device_id = await _lookup_device_id(device_uuid)
                        ctx = stream_manager.register(device_uuid, device_id)
                        writer_task = asyncio.create_task(_writer())
                        logger.info(
                            "CommandStream opened: uuid=%s db_id=%s",
                            device_uuid, device_id,
                        )

                        # Phase 5: push ConfigSyncCommand if agent config is stale.
                        if device_id is not None:
                            await _maybe_sync_config(ctx, device_id, hb.config_version)

                    await _update_device_status(device_uuid, "online")
                    logger.debug(
                        "Heartbeat %s  cpu=%.1f%%  mem=%.1f%%  cfg_v=%d",
                        device_uuid,
                        hb.cpu_usage_percent,
                        hb.memory_usage_percent,
                        hb.config_version,
                    )

                # ---- CommandAck ----
                elif report.HasField("command_ack"):
                    ack = report.command_ack
                    if device_uuid:
                        stream_manager.resolve_ack(
                            device_uuid,
                            ack.command_id,
                            ack.success,
                            ack.message,
                            ack.result_json,
                        )

                # ---- StatusReport ----
                elif report.HasField("status_report"):
                    sr = report.status_report
                    await _update_device_status(device_uuid or report.device_uuid, sr.status)

                # ---- ResourceSnapshot ----
                elif report.HasField("resource_snapshot"):
                    snap = report.resource_snapshot
                    if device_uuid:
                        stream_manager.resolve_ack(
                            device_uuid, snap.command_id, True, "", snap.resources_json
                        )

                # ---- LogChunk ----
                elif report.HasField("log_chunk"):
                    lc = report.log_chunk
                    if device_uuid:
                        stream_manager.buffer_log_chunk(
                            device_uuid, lc.command_id, lc.data, lc.eof
                        )

        except Exception as exc:
            logger.warning("CommandStream error for %s: %s", device_uuid, exc)
        finally:
            if writer_task:
                writer_task.cancel()
                try:
                    await writer_task
                except asyncio.CancelledError:
                    pass
            if device_uuid:
                stream_manager.unregister(device_uuid)
                await _update_device_status(device_uuid, "offline")
                logger.info("CommandStream closed: uuid=%s", device_uuid)


async def _maybe_sync_config(ctx, device_id: int, agent_version: int) -> None:
    """Push ConfigSyncCommand if the agent's cached version is behind the controller."""
    controller_version = await config_store.get_config_version(device_id)
    if agent_version >= controller_version:
        logger.debug(
            "Config in sync for device_id=%d (v=%d)", device_id, controller_version
        )
        return

    logger.info(
        "Config stale for device_id=%d: agent_v=%d controller_v=%d — pushing sync",
        device_id, agent_version, controller_version,
    )
    desired = await config_store.get_desired_config(device_id)
    cmd = edge_control_pb2.EdgeCommand(
        command_id=str(uuid.uuid4()),
        config_sync=edge_control_pb2.ConfigSyncCommand(
            desired_config_json=json.dumps(desired),
            config_version=controller_version,
        ),
    )
    await ctx.queue.put(cmd)


async def _lookup_device_id(device_uuid: str) -> int | None:
    async with async_session_factory() as session:
        result = await session.execute(
            select(Device).where(Device.device_uuid == device_uuid)
        )
        device = result.scalars().first()
        return device.id if device else None


async def _update_device_status(device_uuid: str | None, status: str) -> None:
    if not device_uuid:
        return
    async with async_session_factory() as session:
        result = await session.execute(
            select(Device).where(Device.device_uuid == device_uuid)
        )
        device = result.scalars().first()
        if device:
            device.status = status
            if status == "online":
                device.last_seen = datetime.utcnow()
            session.add(device)
            await session.commit()


def add_to_server(server) -> None:
    if not _STUBS_AVAILABLE:
        logger.warning("EdgeControl stubs not found — run `make proto-python`")
        return
    edge_control_pb2_grpc.add_EdgeControlServicer_to_server(
        EdgeControlServicer(), server
    )
