from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AppCreate(BaseModel):
    name: str
    image: str
    default_tag: str = "latest"
    default_replicas: int = 1
    default_port: Optional[int] = None
    default_env: Optional[dict] = None
    yaml_template: Optional[str] = None


class AppUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    default_tag: Optional[str] = None
    default_replicas: Optional[int] = None
    default_port: Optional[int] = None
    default_env: Optional[dict] = None
    yaml_template: Optional[str] = None


class AppRead(BaseModel):
    id: int
    name: str
    image: str
    default_tag: str
    default_replicas: int
    default_port: Optional[int]
    default_env: Optional[dict]
    yaml_template: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
