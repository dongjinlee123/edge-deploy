import sys
from pathlib import Path

# Must be at the very top so all subsequent imports see the correct paths.
# Expose `app.*` (edge-agent package root).
sys.path.insert(0, str(Path(__file__).parent.parent))
# Expose `edgedeploy.v1.*` (generated protobuf stubs).
sys.path.insert(0, str(Path(__file__).parent.parent / "app" / "generated"))

import pytest
from unittest.mock import MagicMock


@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path, monkeypatch):
    """Redirect config_cache writes to a temporary directory."""
    import app.config

    monkeypatch.setattr(app.config.settings, "data_dir", str(tmp_path))


@pytest.fixture
def mock_k8s(monkeypatch):
    """Replace k8s_manager with a MagicMock before any call to handle()."""
    mock = MagicMock()
    # Default return values that are JSON-serialisable.
    mock.apply_manifests.return_value = []
    mock.get_resources.return_value = {}
    mock.get_pod_logs.return_value = ""

    # Patch in sys.modules so the lazy `from app.services import k8s_manager`
    # inside command_handler.handle() picks up the mock.
    monkeypatch.setitem(sys.modules, "app.services.k8s_manager", mock)
    import app.services
    monkeypatch.setattr(app.services, "k8s_manager", mock, raising=False)

    return mock
