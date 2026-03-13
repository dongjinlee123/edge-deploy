from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DeploymentFormCreate(BaseModel):
    """Form mode: generate YAML from app definition."""
    app_id: int
    device_id: int
    namespace: str = "default"
    tag: Optional[str] = None
    replicas: Optional[int] = None
    port: Optional[int] = None
    env: Optional[dict] = None


class DeploymentYAMLCreate(BaseModel):
    """Raw YAML mode."""
    device_id: int
    namespace: str = "default"
    manifests: str
    app_id: Optional[int] = None


class DeploymentUpdate(BaseModel):
    status: Optional[str] = None
    status_message: Optional[str] = None


class DeploymentRead(BaseModel):
    id: int
    app_id: Optional[int]
    device_id: int
    namespace: str
    manifests: str
    status: str
    status_message: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class DeploymentLogRead(BaseModel):
    id: int
    deployment_id: int
    action: str
    detail: Optional[dict]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class BulkDeployRequest(BaseModel):
    app_id: int
    device_ids: list[int]
    namespace: str = "default"
    tag: Optional[str] = None
    replicas: Optional[int] = None
    port: Optional[int] = None
    env: Optional[dict] = None


class BulkDeployResponse(BaseModel):
    deployments: list[DeploymentRead]
    errors: list[str]
