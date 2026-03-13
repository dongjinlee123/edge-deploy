"""Local desired-config cache for offline resilience.

Persists the controller's desired state to disk so the agent can re-apply
it on startup when the controller is unreachable, and run a periodic
reconciliation loop.

Cache file: /app/data/config_cache.json (override via settings.data_dir)
Format:
    {
        "config_version": <int>,
        "deployments": [
            {"id": <int>, "namespace": "<str>", "manifests": "<yaml str>"}
        ]
    }
"""
import json
import logging
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

_CACHE_FILENAME = "config_cache.json"


def _cache_path() -> Path:
    data_dir = Path(getattr(settings, "data_dir", "/app/data"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / _CACHE_FILENAME


def save(config: dict) -> None:
    """Persist the desired config dict (from ConfigSyncCommand) to disk."""
    path = _cache_path()
    try:
        path.write_text(json.dumps(config, indent=2))
        logger.debug("Config cache saved (v=%s) → %s", config.get("config_version"), path)
    except Exception as exc:
        logger.error("Failed to save config cache: %s", exc)


def load() -> dict | None:
    """Return cached config dict or None if not present / corrupt."""
    path = _cache_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        logger.info("Loaded config cache v=%s from %s", data.get("config_version"), path)
        return data
    except Exception as exc:
        logger.warning("Failed to load config cache: %s", exc)
        return None


def get_config_version() -> int:
    """Return the cached config_version (0 if no cache)."""
    config = load()
    if config is None:
        return 0
    return int(config.get("config_version", 0))
