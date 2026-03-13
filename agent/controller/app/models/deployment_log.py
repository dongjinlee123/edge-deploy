from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON


class DeploymentLog(SQLModel, table=True):
    __tablename__ = "deployment_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    deployment_id: int = Field(foreign_key="deployments.id")
    action: str
    detail: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    status: str  # success/failure
    created_at: datetime = Field(default_factory=datetime.utcnow)
