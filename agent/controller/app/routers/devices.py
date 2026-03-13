from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models import Device
from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from app.services import agent_client

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("", response_model=list[DeviceRead])
async def list_devices(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Device))
    return result.scalars().all()


@router.post("", response_model=DeviceRead, status_code=201)
async def create_device(body: DeviceCreate, session: AsyncSession = Depends(get_session)):
    device = Device(**body.model_dump())
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


@router.get("/{device_id}", response_model=DeviceRead)
async def get_device(device_id: int, session: AsyncSession = Depends(get_session)):
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    return device


@router.put("/{device_id}", response_model=DeviceRead)
async def update_device(device_id: int, body: DeviceUpdate, session: AsyncSession = Depends(get_session)):
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    for k, v in body.model_dump(exclude_none=True).items():
        setattr(device, k, v)
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


@router.delete("/{device_id}", status_code=204)
async def delete_device(device_id: int, session: AsyncSession = Depends(get_session)):
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    await session.delete(device)
    await session.commit()


@router.post("/{device_id}/ping", response_model=DeviceRead)
async def ping_device(device_id: int, session: AsyncSession = Depends(get_session)):
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    try:
        await agent_client.get_health(device)
        device.status = "online"
        device.last_seen = datetime.utcnow()
    except Exception as exc:
        device.status = "offline"
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device
