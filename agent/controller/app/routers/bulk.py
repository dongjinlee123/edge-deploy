from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.schemas.deployment import BulkDeployRequest, BulkDeployResponse, DeploymentRead
from app.services import deployment_service

router = APIRouter(prefix="/bulk", tags=["bulk"])


@router.post("/deploy", response_model=BulkDeployResponse)
async def bulk_deploy(body: BulkDeployRequest, session: AsyncSession = Depends(get_session)):
    results = []
    errors = []
    for device_id in body.device_ids:
        try:
            d = await deployment_service.create_form_deployment(
                session,
                app_id=body.app_id,
                device_id=device_id,
                namespace=body.namespace,
                tag=body.tag,
                replicas=body.replicas,
                port=body.port,
                env=body.env,
            )
            results.append(d)
        except Exception as exc:
            errors.append(f"Device {device_id}: {exc}")

    if errors and not results:
        raise HTTPException(500, detail="\n".join(errors))

    return BulkDeployResponse(deployments=results, errors=errors)
