from fastapi import APIRouter, Depends
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models import App, Deployment, Device

router = APIRouter(prefix="/overview", tags=["overview"])


@router.get("")
async def overview(session: AsyncSession = Depends(get_session)):
    total_devices = (await session.execute(select(func.count(Device.id)))).scalar_one()
    online_devices = (
        await session.execute(select(func.count(Device.id)).where(Device.status == "online"))
    ).scalar_one()
    offline_devices = (
        await session.execute(select(func.count(Device.id)).where(Device.status == "offline"))
    ).scalar_one()
    total_apps = (await session.execute(select(func.count(App.id)))).scalar_one()
    total_deployments = (await session.execute(select(func.count(Deployment.id)))).scalar_one()
    failed_deployments = (
        await session.execute(select(func.count(Deployment.id)).where(Deployment.status == "failed"))
    ).scalar_one()
    running_deployments = (
        await session.execute(select(func.count(Deployment.id)).where(Deployment.status == "running"))
    ).scalar_one()

    return {
        "devices": {
            "total": total_devices,
            "online": online_devices,
            "offline": offline_devices,
        },
        "apps": {"total": total_apps},
        "deployments": {
            "total": total_deployments,
            "running": running_deployments,
            "failed": failed_deployments,
        },
    }
