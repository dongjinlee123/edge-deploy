from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DeviceCreate(BaseModel):
    name: str
    address: str
    agent_port: int = 30080
    labels: Optional[dict] = None


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    agent_port: Optional[int] = None
    labels: Optional[dict] = None


class DeviceRead(BaseModel):
    id: int
    name: str
    address: str
    agent_port: int
    status: str
    last_seen: Optional[datetime]
    labels: Optional[dict]
    created_at: datetime

    model_config = {"from_attributes": True}
