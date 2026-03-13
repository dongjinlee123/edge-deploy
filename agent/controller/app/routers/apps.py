from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models import App
from app.schemas.app import AppCreate, AppRead, AppUpdate

router = APIRouter(prefix="/apps", tags=["apps"])


@router.get("", response_model=list[AppRead])
async def list_apps(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(App))
    return result.scalars().all()


@router.post("", response_model=AppRead, status_code=201)
async def create_app(body: AppCreate, session: AsyncSession = Depends(get_session)):
    app = App(**body.model_dump())
    session.add(app)
    await session.commit()
    await session.refresh(app)
    return app


@router.get("/{app_id}", response_model=AppRead)
async def get_app(app_id: int, session: AsyncSession = Depends(get_session)):
    app = await session.get(App, app_id)
    if not app:
        raise HTTPException(404, "App not found")
    return app


@router.put("/{app_id}", response_model=AppRead)
async def update_app(app_id: int, body: AppUpdate, session: AsyncSession = Depends(get_session)):
    app = await session.get(App, app_id)
    if not app:
        raise HTTPException(404, "App not found")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(app, k, v)
    session.add(app)
    await session.commit()
    await session.refresh(app)
    return app


@router.delete("/{app_id}", status_code=204)
async def delete_app(app_id: int, session: AsyncSession = Depends(get_session)):
    app = await session.get(App, app_id)
    if not app:
        raise HTTPException(404, "App not found")
    await session.delete(app)
    await session.commit()
