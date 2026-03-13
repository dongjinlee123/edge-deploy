import sys
from pathlib import Path

# Must be at the very top so all subsequent imports see the correct paths.
# Expose `app.*` (controller package root).
sys.path.insert(0, str(Path(__file__).parent.parent))
# Expose `edgedeploy.v1.*` (generated protobuf stubs).
sys.path.insert(0, str(Path(__file__).parent.parent / "app" / "generated"))

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# Import all models so they register in SQLModel.metadata before create_all.
import app.models  # noqa: F401
from app.services.stream_manager import StreamManager


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def config_store_env(db_engine, monkeypatch):
    """Return a sessionmaker wired to an in-memory DB and patch config_store."""
    import app.services.config_store as cs

    factory = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    monkeypatch.setattr(cs, "async_session_factory", factory)
    return factory


@pytest.fixture
def sm():
    """Fresh StreamManager per test — no singleton state pollution."""
    return StreamManager()
