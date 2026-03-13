from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models import Deployment, DeploymentLog, Device
from app.schemas.deployment import (
    DeploymentFormCreate,
    DeploymentLogRead,
    DeploymentRead,
    DeploymentUpdate,
    DeploymentYAMLCreate,
)
from app.services import agent_client, deployment_service

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/deployments", tags=["deployments"])


@router.get("", response_model=list[DeploymentRead])
async def list_deployments(
    device_id: int | None = None,
    app_id: int | None = None,
    status: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    q = select(Deployment)
    if device_id:
        q = q.where(Deployment.device_id == device_id)
    if app_id:
        q = q.where(Deployment.app_id == app_id)
    if status:
        q = q.where(Deployment.status == status)
    result = await session.execute(q.order_by(Deployment.created_at.desc()))
    return result.scalars().all()


@router.post("/form", response_model=DeploymentRead, status_code=201)
async def create_form_deployment(
    body: DeploymentFormCreate, session: AsyncSession = Depends(get_session)
):
    try:
        return await deployment_service.create_form_deployment(
            session,
            app_id=body.app_id,
            device_id=body.device_id,
            namespace=body.namespace,
            tag=body.tag,
            replicas=body.replicas,
            port=body.port,
            env=body.env,
        )
    except ValueError as exc:
        raise HTTPException(404, str(exc))
    except Exception as exc:
        raise HTTPException(500, str(exc))


@router.post("/yaml", response_model=DeploymentRead, status_code=201)
async def create_yaml_deployment(
    body: DeploymentYAMLCreate, session: AsyncSession = Depends(get_session)
):
    try:
        return await deployment_service.create_yaml_deployment(
            session,
            device_id=body.device_id,
            namespace=body.namespace,
            manifests=body.manifests,
            app_id=body.app_id,
        )
    except ValueError as exc:
        raise HTTPException(404, str(exc))
    except Exception as exc:
        raise HTTPException(500, str(exc))


@router.get("/{deployment_id}", response_model=DeploymentRead)
async def get_deployment(deployment_id: int, session: AsyncSession = Depends(get_session)):
    d = await session.get(Deployment, deployment_id)
    if not d:
        raise HTTPException(404, "Deployment not found")
    return d


@router.put("/{deployment_id}", response_model=DeploymentRead)
async def update_deployment(
    deployment_id: int,
    body: DeploymentUpdate,
    session: AsyncSession = Depends(get_session),
):
    d = await session.get(Deployment, deployment_id)
    if not d:
        raise HTTPException(404, "Deployment not found")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(d, k, v)
    session.add(d)
    await session.commit()
    await session.refresh(d)
    return d


@router.delete("/{deployment_id}", status_code=204)
async def stop_and_delete_deployment(deployment_id: int, session: AsyncSession = Depends(get_session)):
    try:
        await deployment_service.stop_deployment(session, deployment_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc))
    except Exception as exc:
        logger.warning("Best-effort stop failed for deployment %d: %s", deployment_id, exc)

    # Delete logs then the deployment record
    logs_result = await session.execute(
        select(DeploymentLog).where(DeploymentLog.deployment_id == deployment_id)
    )
    for log in logs_result.scalars().all():
        await session.delete(log)

    d = await session.get(Deployment, deployment_id)
    if d:
        await session.delete(d)

    await session.commit()


@router.post("/{deployment_id}/restart", response_model=DeploymentRead)
async def restart_deployment(deployment_id: int, session: AsyncSession = Depends(get_session)):
    d = await session.get(Deployment, deployment_id)
    if not d:
        raise HTTPException(404, "Deployment not found")
    device = await session.get(Device, d.device_id)
    if not device:
        raise HTTPException(404, "Device not found")

    import yaml as pyyaml
    errors = []
    for doc in pyyaml.safe_load_all(d.manifests):
        if doc and doc.get("kind", "").lower() == "deployment":
            name = doc.get("metadata", {}).get("name", "")
            try:
                await agent_client.restart_deployment(device, d.namespace, name)
            except Exception as exc:
                errors.append(str(exc))

    if errors:
        d.status_message = "; ".join(errors)
        session.add(d)
        await session.commit()
        await session.refresh(d)

    return d


@router.get("/{deployment_id}/logs", response_model=list[DeploymentLogRead])
async def deployment_logs(deployment_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(DeploymentLog)
        .where(DeploymentLog.deployment_id == deployment_id)
        .order_by(DeploymentLog.created_at.desc())
    )
    return result.scalars().all()
