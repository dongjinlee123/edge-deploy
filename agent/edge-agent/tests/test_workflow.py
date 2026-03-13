"""Edge-agent workflow tests.

Organised by functionality:
  5. CommandHandler  — command_handler.handle() with mocked k8s_manager
  6. ConfigCache     — config_cache read/write with tmp_path fixture
"""
import json

import pytest
from unittest.mock import MagicMock

from edgedeploy.v1 import edge_control_pb2


# ===========================================================================
# Functionality 5 — Command Handler
# ===========================================================================

class TestCommandHandler:

    async def test_apply_manifests_returns_success_ack(self, mock_k8s):
        from app.services.command_handler import handle

        cmd = edge_control_pb2.EdgeCommand(
            command_id="cmd-apply",
            apply_manifests=edge_control_pb2.ApplyManifestsCommand(
                namespace="default",
                manifests="apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: cm\n",
            ),
        )
        result = await handle(cmd)

        mock_k8s.apply_manifests.assert_called_once()
        assert result.HasField("command_ack")
        assert result.command_ack.success is True
        assert result.command_ack.command_id == "cmd-apply"

    async def test_apply_manifests_k8s_error_returns_failure(self, mock_k8s):
        from app.services.command_handler import handle

        mock_k8s.apply_manifests.side_effect = Exception("k8s unavailable")
        cmd = edge_control_pb2.EdgeCommand(
            command_id="cmd-apply-fail",
            apply_manifests=edge_control_pb2.ApplyManifestsCommand(
                namespace="default",
                manifests="---",
            ),
        )
        result = await handle(cmd)

        assert result.HasField("command_ack")
        assert result.command_ack.success is False
        assert "k8s unavailable" in result.command_ack.message

    async def test_delete_resource_returns_success_ack(self, mock_k8s):
        from app.services.command_handler import handle

        cmd = edge_control_pb2.EdgeCommand(
            command_id="cmd-del",
            delete_resource=edge_control_pb2.DeleteResourceCommand(
                namespace="default",
                kind="Deployment",
                name="my-app",
            ),
        )
        result = await handle(cmd)

        mock_k8s.delete_resource.assert_called_once_with("default", "Deployment", "my-app")
        assert result.HasField("command_ack")
        assert result.command_ack.success is True

    async def test_restart_deployment_returns_success_ack(self, mock_k8s):
        from app.services.command_handler import handle

        cmd = edge_control_pb2.EdgeCommand(
            command_id="cmd-restart",
            restart_deployment=edge_control_pb2.RestartDeploymentCommand(
                namespace="default",
                name="my-app",
            ),
        )
        result = await handle(cmd)

        mock_k8s.restart_deployment.assert_called_once_with("default", "my-app")
        assert result.HasField("command_ack")
        assert result.command_ack.success is True

    async def test_get_resources_returns_resource_snapshot(self, mock_k8s):
        from app.services.command_handler import handle

        mock_k8s.get_resources.return_value = {"pods": [{"name": "pod-1"}]}
        cmd = edge_control_pb2.EdgeCommand(
            command_id="cmd-res",
            get_resources=edge_control_pb2.GetResourcesCommand(namespace="default"),
        )
        result = await handle(cmd)

        mock_k8s.get_resources.assert_called_once_with("default")
        assert result.HasField("resource_snapshot")
        snap = result.resource_snapshot
        assert snap.command_id == "cmd-res"
        parsed = json.loads(snap.resources_json)
        assert parsed["pods"][0]["name"] == "pod-1"

    async def test_get_pod_logs_returns_log_chunk_with_eof(self, mock_k8s):
        from app.services.command_handler import handle

        mock_k8s.get_pod_logs.return_value = "line1\nline2\n"
        cmd = edge_control_pb2.EdgeCommand(
            command_id="cmd-logs",
            get_pod_logs=edge_control_pb2.GetPodLogsCommand(
                namespace="default",
                pod_name="my-pod",
                tail=50,
            ),
        )
        result = await handle(cmd)

        mock_k8s.get_pod_logs.assert_called_once()
        assert result.HasField("log_chunk")
        lc = result.log_chunk
        assert lc.command_id == "cmd-logs"
        assert lc.eof is True
        assert lc.data == b"line1\nline2\n"

    async def test_config_sync_saves_cache_and_applies_all(self, mock_k8s, tmp_path):
        from app.services.command_handler import handle

        deployments = [
            {"id": 1, "namespace": "ns-a", "manifests": "---"},
            {"id": 2, "namespace": "ns-b", "manifests": "---"},
        ]
        cmd = edge_control_pb2.EdgeCommand(
            command_id="cmd-sync",
            config_sync=edge_control_pb2.ConfigSyncCommand(
                desired_config_json=json.dumps({"deployments": deployments}),
                config_version=3,
            ),
        )
        result = await handle(cmd)

        # Cache file written
        cache_file = tmp_path / "config_cache.json"
        assert cache_file.exists()
        cached = json.loads(cache_file.read_text())
        assert cached["config_version"] == 3

        # apply_manifests called for each deployment
        assert mock_k8s.apply_manifests.call_count == 2

        assert result.HasField("command_ack")
        assert result.command_ack.success is True
        assert "synced" in result.command_ack.message

    async def test_config_sync_partial_failure_returns_false(self, mock_k8s):
        from app.services.command_handler import handle

        mock_k8s.apply_manifests.side_effect = Exception("apply failed")
        cmd = edge_control_pb2.EdgeCommand(
            command_id="cmd-sync-fail",
            config_sync=edge_control_pb2.ConfigSyncCommand(
                desired_config_json=json.dumps({
                    "deployments": [{"id": 1, "namespace": "default", "manifests": "---"}],
                }),
                config_version=1,
            ),
        )
        result = await handle(cmd)

        assert result.HasField("command_ack")
        assert result.command_ack.success is False
        assert "apply failed" in result.command_ack.message

    async def test_unknown_command_returns_failure_ack(self, mock_k8s):
        from app.services.command_handler import handle

        cmd = MagicMock()
        cmd.command_id = "cmd-unknown"
        cmd.WhichOneof.return_value = "totally_unknown_field"

        result = await handle(cmd)

        assert result.HasField("command_ack")
        assert result.command_ack.success is False

    async def test_exception_returns_failure_ack(self, mock_k8s):
        from app.services.command_handler import handle

        mock_k8s.delete_resource.side_effect = RuntimeError("unexpected crash")
        cmd = edge_control_pb2.EdgeCommand(
            command_id="cmd-crash",
            delete_resource=edge_control_pb2.DeleteResourceCommand(
                namespace="default",
                kind="Pod",
                name="bad-pod",
            ),
        )
        result = await handle(cmd)

        assert result.HasField("command_ack")
        assert result.command_ack.success is False
        assert "unexpected crash" in result.command_ack.message


# ===========================================================================
# Functionality 6 — Config Cache (offline resilience)
# ===========================================================================

class TestConfigCache:

    def test_save_creates_json_file(self, tmp_path):
        from app.services import config_cache

        config_cache.save({"config_version": 1, "deployments": []})

        cache_file = tmp_path / "config_cache.json"
        assert cache_file.exists()

    def test_load_round_trip(self, tmp_path):
        from app.services import config_cache

        original = {"config_version": 4, "deployments": [{"id": 1}]}
        config_cache.save(original)
        loaded = config_cache.load()

        assert loaded == original

    def test_load_returns_none_when_missing(self, tmp_path):
        from app.services import config_cache

        result = config_cache.load()
        assert result is None

    def test_load_returns_none_on_corrupt_json(self, tmp_path):
        from app.services import config_cache

        (tmp_path / "config_cache.json").write_text("not valid json {{{")
        result = config_cache.load()
        assert result is None

    def test_get_config_version_returns_zero_when_missing(self, tmp_path):
        from app.services import config_cache

        assert config_cache.get_config_version() == 0

    def test_get_config_version_returns_cached_value(self, tmp_path):
        from app.services import config_cache

        config_cache.save({"config_version": 5, "deployments": []})
        assert config_cache.get_config_version() == 5

    def test_save_overwrites_previous(self, tmp_path):
        from app.services import config_cache

        config_cache.save({"config_version": 1, "deployments": []})
        config_cache.save({"config_version": 9, "deployments": [{"id": 2}]})

        loaded = config_cache.load()
        assert loaded["config_version"] == 9
        assert len(loaded["deployments"]) == 1
