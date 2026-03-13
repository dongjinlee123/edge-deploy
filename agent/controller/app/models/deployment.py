from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Column, Text


class Deployment(SQLModel, table=True):
    __tablename__ = "deployments"

    id: Optional[int] = Field(default=None, primary_key=True)
    app_id: Optional[int] = Field(default=None, foreign_key="apps.id")
    device_id: int = Field(foreign_key="devices.id")
    namespace: str = Field(default="default")
    manifests: str = Field(sa_column=Column(Text))  # stored YAML
    status: str = Field(default="pending")  # pending/deploying/running/failed/stopped
    status_message: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
