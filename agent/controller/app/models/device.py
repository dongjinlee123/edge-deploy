from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON


class Device(SQLModel, table=True):
    __tablename__ = "devices"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str  # IP or hostname
    agent_port: int = Field(default=30080)
    status: str = Field(default="unknown")  # online/offline/unknown
    last_seen: Optional[datetime] = Field(default=None)
    labels: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # UUID sent by the agent in its first heartbeat; used to look up the stream.
    device_uuid: Optional[str] = Field(default=None, index=True)
    # Monotonically increasing desired-state version.  Bumped on every deploy/stop.
    # Agent sends its cached version in the heartbeat; controller pushes a
    # ConfigSyncCommand when the agent is stale.
    config_version: int = Field(default=0)
