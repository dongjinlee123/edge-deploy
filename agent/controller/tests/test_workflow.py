"""Controller workflow tests.

Organised by functionality:
  1. StreamManager  — pure in-process, no mocking needed
  2. ConfigStore    — in-memory SQLite via config_store_env fixture
  3. ConfigSync     — _maybe_sync_config with mocked config_store + ctx.queue
  4. HeartbeatHandling — EdgeControlServicer.CommandStream with mocked helpers
"""
import asyncio
import json

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.stream_manager import StreamManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _add_device(factory, config_version=0, device_uuid=None):
    from app.models.device import Device

    async with factory() as session:
        device = Device(
            name="test-device",
            address="127.0.0.1",
            config_version=config_version,
            device_uuid=device_uuid,
        )
        session.add(device)
        await session.commit()
        await session.refresh(device)
        return device


async def _add_deployment(factory, device_id, status="running", namespace="default", manifests="---"):
    from app.models.deployment import Deployment

    async with factory() as session:
        dep = Deployment(
            device_id=device_id,
            namespace=namespace,
            manifests=manifests,
            status=status,
        )
        session.add(dep)
        await session.commit()
        await session.refresh(dep)
        return dep


def _make_grpc_context():
    ctx = MagicMock()
    ctx.write = AsyncMock()
    return ctx


async def _run_stream(monkeypatch, sm, reports, *, lookup_return=1):
    """Run EdgeControlServicer.CommandStream with a sequence of mocked reports."""
    monkeypatch.setattr("app.grpc_services.edge_control_servicer.stream_manager", sm)
    monkeypatch.setattr(
        "app.grpc_services.edge_control_servicer._lookup_device_id",
        AsyncMock(return_value=lookup_return),
    )
    monkeypatch.setattr(
        "app.grpc_services.edge_control_servicer._update_device_status",
        AsyncMock(),
    )
    monkeypatch.setattr(
        "app.grpc_services.edge_control_servicer._maybe_sync_config",
        AsyncMock(),
    )

    from app.grpc_services.edge_control_servicer import EdgeControlServicer

    async def gen():
        for r in reports:
            yield r

    servicer = EdgeControlServicer()
    await servicer.CommandStream(gen(), _make_grpc_context())


def _hb_report(device_uuid="test-uuid", config_version=0):
    r = MagicMock()
    r.HasField.side_effect = lambda f: f == "heartbeat"
    r.device_uuid = device_uuid
    r.heartbeat.config_version = config_version
    return r


# ===========================================================================
# Functionality 1 — StreamManager
# ===========================================================================

class TestStreamManager:

    def test_register_creates_context(self, sm):
        ctx = sm.register("uuid-1", 10)
        assert ctx.device_uuid == "uuid-1"
        assert ctx.device_id == 10
        assert sm.get_by_uuid("uuid-1") is ctx

    def test_unregister_removes_context(self, sm):
        sm.register("uuid-1", 10)
        sm.unregister("uuid-1")
        assert sm.get_by_uuid("uuid-1") is None
        assert sm.get_by_device_id(10) is None

    async def test_unregister_cancels_pending_futures(self, sm):
        ctx = sm.register("uuid-1", 10)
        fut = asyncio.get_running_loop().create_future()
        ctx.pending["cmd1"] = fut
        sm.unregister("uuid-1")
        assert fut.cancelled()

    def test_get_by_uuid(self, sm):
        sm.register("uuid-1", 10)
        assert sm.get_by_uuid("uuid-1") is not None
        assert sm.get_by_uuid("nonexistent") is None

    def test_get_by_device_id(self, sm):
        ctx = sm.register("uuid-1", 10)
        assert sm.get_by_device_id(10) is ctx
        assert sm.get_by_device_id(999) is None

    def test_is_connected_true_and_false(self, sm):
        sm.register("uuid-1", 10)
        assert sm.is_connected(10) is True
        sm.unregister("uuid-1")
        assert sm.is_connected(10) is False

    async def test_send_command_and_resolve_ack(self, sm):
        sm.register("uuid-1", 1)
        cmd = MagicMock()
        cmd.command_id = "cmd1"
        task = asyncio.create_task(sm.send_command(1, cmd, timeout=5.0))
        await asyncio.sleep(0)  # yield so send_command can register the future
        sm.resolve_ack("uuid-1", "cmd1", True, "ok", '{"k": "v"}')
        result = await task
        assert result == {"k": "v"}

    async def test_send_command_failure_ack(self, sm):
        sm.register("uuid-1", 1)
        cmd = MagicMock()
        cmd.command_id = "cmd1"
        task = asyncio.create_task(sm.send_command(1, cmd, timeout=5.0))
        await asyncio.sleep(0)
        sm.resolve_ack("uuid-1", "cmd1", False, "boom", "")
        with pytest.raises(RuntimeError, match="boom"):
            await task

    async def test_send_command_timeout(self, sm):
        sm.register("uuid-1", 1)
        cmd = MagicMock()
        cmd.command_id = "cmd1"
        with pytest.raises(TimeoutError):
            await sm.send_command(1, cmd, timeout=0.05)

    async def test_resolve_ack_json_result(self, sm):
        sm.register("uuid-1", 1)
        cmd = MagicMock()
        cmd.command_id = "cmd1"
        task = asyncio.create_task(sm.send_command(1, cmd, timeout=5.0))
        await asyncio.sleep(0)
        sm.resolve_ack("uuid-1", "cmd1", True, "", '{"status": "ok"}')
        result = await task
        assert result["status"] == "ok"

    async def test_buffer_log_chunk_accumulation(self, sm):
        ctx = sm.register("uuid-1", 1)
        fut = asyncio.get_running_loop().create_future()
        ctx.pending["cmd1"] = fut

        sm.buffer_log_chunk("uuid-1", "cmd1", b"hello ", False)
        sm.buffer_log_chunk("uuid-1", "cmd1", b"world", False)
        sm.buffer_log_chunk("uuid-1", "cmd1", b"", True)  # eof

        result = await fut
        assert result == "hello world"

    async def test_buffer_log_chunk_eof_empty(self, sm):
        ctx = sm.register("uuid-1", 1)
        fut = asyncio.get_running_loop().create_future()
        ctx.pending["cmd1"] = fut

        sm.buffer_log_chunk("uuid-1", "cmd1", b"", True)  # eof with no data

        result = await fut
        assert result == ""


# ===========================================================================
# Functionality 2 — Config Versioning (config_store)
# ===========================================================================

class TestConfigStore:

    async def test_get_config_version_default_zero(self, config_store_env):
        from app.services import config_store

        result = await config_store.get_config_version(9999)
        assert result == 0

    async def test_bump_config_version_increments(self, config_store_env):
        from app.services import config_store

        device = await _add_device(config_store_env)
        await config_store.bump_config_version(device.id)
        await config_store.bump_config_version(device.id)
        version = await config_store.get_config_version(device.id)
        assert version == 2

    async def test_bump_config_version_returns_new(self, config_store_env):
        from app.services import config_store

        device = await _add_device(config_store_env)
        v1 = await config_store.bump_config_version(device.id)
        v2 = await config_store.bump_config_version(device.id)
        assert v1 == 1
        assert v2 == 2

    async def test_get_desired_config_empty(self, config_store_env):
        from app.services import config_store

        device = await _add_device(config_store_env)
        result = await config_store.get_desired_config(device.id)
        assert result == {"deployments": []}

    async def test_get_desired_config_running_only(self, config_store_env):
        from app.services import config_store

        device = await _add_device(config_store_env)
        await _add_deployment(config_store_env, device.id, status="running")
        await _add_deployment(config_store_env, device.id, status="stopped")
        await _add_deployment(config_store_env, device.id, status="failed")
        result = await config_store.get_desired_config(device.id)
        assert len(result["deployments"]) == 1

    async def test_get_desired_config_fields(self, config_store_env):
        from app.services import config_store

        device = await _add_device(config_store_env)
        dep = await _add_deployment(
            config_store_env, device.id,
            status="running",
            namespace="prod",
            manifests="apiVersion: v1\nkind: ConfigMap",
        )
        result = await config_store.get_desired_config(device.id)
        item = result["deployments"][0]
        assert item["id"] == dep.id
        assert item["namespace"] == "prod"
        assert item["manifests"] == "apiVersion: v1\nkind: ConfigMap"


# ===========================================================================
# Functionality 3 — Config Sync Decision (_maybe_sync_config)
# ===========================================================================

class TestConfigSync:

    async def test_no_sync_when_versions_equal(self, monkeypatch):
        import app.services.config_store as cs

        monkeypatch.setattr(cs, "get_config_version", AsyncMock(return_value=5))
        monkeypatch.setattr(cs, "get_desired_config", AsyncMock(return_value={"deployments": []}))

        from app.grpc_services.edge_control_servicer import _maybe_sync_config
        from app.services.stream_manager import StreamContext

        ctx = StreamContext(device_uuid="uuid-1", device_id=1, queue=asyncio.Queue())
        await _maybe_sync_config(ctx, 1, agent_version=5)

        assert ctx.queue.empty()
        cs.get_desired_config.assert_not_called()

    async def test_sync_pushed_when_agent_behind(self, monkeypatch):
        import app.services.config_store as cs

        monkeypatch.setattr(cs, "get_config_version", AsyncMock(return_value=5))
        monkeypatch.setattr(cs, "get_desired_config", AsyncMock(return_value={"deployments": []}))

        from app.grpc_services.edge_control_servicer import _maybe_sync_config
        from app.services.stream_manager import StreamContext

        ctx = StreamContext(device_uuid="uuid-1", device_id=1, queue=asyncio.Queue())
        await _maybe_sync_config(ctx, 1, agent_version=3)

        assert not ctx.queue.empty()

    async def test_sync_payload_contains_desired_config(self, monkeypatch):
        import app.services.config_store as cs
        from edgedeploy.v1 import edge_control_pb2

        desired = {"deployments": [{"id": 1, "namespace": "default", "manifests": "---"}]}
        monkeypatch.setattr(cs, "get_config_version", AsyncMock(return_value=7))
        monkeypatch.setattr(cs, "get_desired_config", AsyncMock(return_value=desired))

        from app.grpc_services.edge_control_servicer import _maybe_sync_config
        from app.services.stream_manager import StreamContext

        ctx = StreamContext(device_uuid="uuid-1", device_id=1, queue=asyncio.Queue())
        await _maybe_sync_config(ctx, 1, agent_version=0)

        cmd = ctx.queue.get_nowait()
        assert cmd.HasField("config_sync")
        payload = json.loads(cmd.config_sync.desired_config_json)
        assert payload["deployments"][0]["id"] == 1
        assert cmd.config_sync.config_version == 7


# ===========================================================================
# Functionality 4 — Heartbeat Handling (EdgeControlServicer.CommandStream)
# ===========================================================================

class TestHeartbeatHandling:

    async def test_first_heartbeat_registers_stream(self, sm, monkeypatch):
        with patch.object(sm, "register", wraps=sm.register) as mock_register:
            await _run_stream(monkeypatch, sm, [_hb_report()])
            mock_register.assert_called_once_with("test-uuid", 1)

    async def test_device_status_updated_to_online(self, sm, monkeypatch):
        mock_update = AsyncMock()
        monkeypatch.setattr("app.grpc_services.edge_control_servicer.stream_manager", sm)
        monkeypatch.setattr(
            "app.grpc_services.edge_control_servicer._lookup_device_id",
            AsyncMock(return_value=1),
        )
        monkeypatch.setattr(
            "app.grpc_services.edge_control_servicer._update_device_status",
            mock_update,
        )
        monkeypatch.setattr(
            "app.grpc_services.edge_control_servicer._maybe_sync_config",
            AsyncMock(),
        )

        from app.grpc_services.edge_control_servicer import EdgeControlServicer

        async def gen():
            yield _hb_report()

        await EdgeControlServicer().CommandStream(gen(), _make_grpc_context())
        mock_update.assert_any_call("test-uuid", "online")

    async def test_command_ack_routed_to_resolve_ack(self, sm, monkeypatch):
        ack_report = MagicMock()
        ack_report.HasField.side_effect = lambda f: f == "command_ack"
        ack_report.device_uuid = "test-uuid"
        ack_report.command_ack.command_id = "cmd-1"
        ack_report.command_ack.success = True
        ack_report.command_ack.message = "done"
        ack_report.command_ack.result_json = "{}"

        with patch.object(sm, "resolve_ack", wraps=sm.resolve_ack) as mock_resolve:
            await _run_stream(monkeypatch, sm, [_hb_report(), ack_report])
            mock_resolve.assert_called_once_with("test-uuid", "cmd-1", True, "done", "{}")

    async def test_status_report_updates_device(self, sm, monkeypatch):
        mock_update = AsyncMock()
        monkeypatch.setattr("app.grpc_services.edge_control_servicer.stream_manager", sm)
        monkeypatch.setattr(
            "app.grpc_services.edge_control_servicer._lookup_device_id",
            AsyncMock(return_value=1),
        )
        monkeypatch.setattr(
            "app.grpc_services.edge_control_servicer._update_device_status",
            mock_update,
        )
        monkeypatch.setattr(
            "app.grpc_services.edge_control_servicer._maybe_sync_config",
            AsyncMock(),
        )

        sr_report = MagicMock()
        sr_report.HasField.side_effect = lambda f: f == "status_report"
        sr_report.device_uuid = "test-uuid"
        sr_report.status_report.status = "degraded"

        from app.grpc_services.edge_control_servicer import EdgeControlServicer

        async def gen():
            yield _hb_report()
            yield sr_report

        await EdgeControlServicer().CommandStream(gen(), _make_grpc_context())
        mock_update.assert_any_call("test-uuid", "degraded")
