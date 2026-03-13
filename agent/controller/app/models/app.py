from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Column, Text
from sqlalchemy import JSON


class App(SQLModel, table=True):
    __tablename__ = "apps"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    image: str
    default_tag: str = Field(default="latest")
    default_replicas: int = Field(default=1)
    default_port: Optional[int] = Field(default=None)
    default_env: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    yaml_template: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow)
