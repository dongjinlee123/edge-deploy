"""Per-device bidi-stream registry and command dispatcher.

One StreamContext is held per connected edge agent.  Callers enqueue an
EdgeCommand, await the correlated Future, and get back the decoded result.
"""
import asyncio
import json
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class StreamContext:
    device_uuid: str
    device_id: int | None
    # Commands waiting to be written to the stream
    queue: asyncio.Queue
    # command_id → Future resolved when the agent acks
    pending: dict[str, asyncio.Future] = field(default_factory=dict)
    # Accumulated log bytes per command_id (resolved on eof=True)
    log_buffers: dict[str, list[bytes]] = field(default_factory=dict)


class StreamManager:
    def __init__(self) -> None:
        self._streams: dict[str, StreamContext] = {}   # device_uuid → ctx
        self._id_to_uuid: dict[int, str] = {}          # device_id  → device_uuid

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, device_uuid: str, device_id: int | None) -> StreamContext:
        ctx = StreamContext(
            device_uuid=device_uuid,
            device_id=device_id,
            queue=asyncio.Queue(),
        )
        self._streams[device_uuid] = ctx
        if device_id is not None:
            self._id_to_uuid[device_id] = device_uuid
        logger.info("Stream registered: device_uuid=%s device_id=%s", device_uuid, device_id)
        return ctx

    def unregister(self, device_uuid: str) -> None:
        ctx = self._streams.pop(device_uuid, None)
        if ctx and ctx.device_id is not None:
            self._id_to_uuid.pop(ctx.device_id, None)
        # Cancel any pending futures
        if ctx:
            for fut in ctx.pending.values():
                if not fut.done():
                    fut.cancel()
        logger.info("Stream unregistered: device_uuid=%s", device_uuid)

    # ------------------------------------------------------------------
    # Lookup helpers
    # ------------------------------------------------------------------

    def get_by_uuid(self, device_uuid: str) -> StreamContext | None:
        return self._streams.get(device_uuid)

    def get_by_device_id(self, device_id: int) -> StreamContext | None:
        uuid = self._id_to_uuid.get(device_id)
        return self._streams.get(uuid) if uuid else None

    def is_connected(self, device_id: int) -> bool:
        uuid = self._id_to_uuid.get(device_id)
        return bool(uuid and uuid in self._streams)

    # ------------------------------------------------------------------
    # Command dispatch
    # ------------------------------------------------------------------

    async def send_command(self, device_id: int, command, timeout: float = 30.0):
        """Queue command, await ack Future, return decoded result or raise."""
        ctx = self.get_by_device_id(device_id)
        if ctx is None:
            raise RuntimeError(f"No active gRPC stream for device_id={device_id}")

        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()
        ctx.pending[command.command_id] = future

        try:
            await ctx.queue.put(command)
            return await asyncio.wait_for(asyncio.shield(future), timeout=timeout)
        except asyncio.TimeoutError:
            ctx.pending.pop(command.command_id, None)
            raise TimeoutError(f"Command {command.command_id} timed out ({timeout}s)")

    # ------------------------------------------------------------------
    # Ack resolution (called by EdgeControlServicer)
    # ------------------------------------------------------------------

    def resolve_ack(
        self,
        device_uuid: str,
        command_id: str,
        success: bool,
        message: str,
        result_json: str,
    ) -> None:
        """Resolve a pending Future for a CommandAck or ResourceSnapshot."""
        ctx = self._streams.get(device_uuid)
        if ctx is None:
            return
        future = ctx.pending.pop(command_id, None)
        if future is None or future.done():
            return
        if success:
            try:
                future.set_result(json.loads(result_json) if result_json else {})
            except Exception:
                future.set_result({"message": message})
        else:
            future.set_exception(RuntimeError(message or "command failed"))

    def buffer_log_chunk(
        self, device_uuid: str, command_id: str, data: bytes, eof: bool
    ) -> None:
        """Accumulate log bytes; resolve Future on EOF."""
        ctx = self._streams.get(device_uuid)
        if ctx is None:
            return
        buf = ctx.log_buffers.setdefault(command_id, [])
        if data:
            buf.append(data)
        if eof:
            ctx.log_buffers.pop(command_id, None)
            text = b"".join(buf).decode("utf-8", errors="replace")
            future = ctx.pending.pop(command_id, None)
            if future and not future.done():
                future.set_result(text)


# Module-level singleton — imported everywhere by name.
stream_manager = StreamManager()
