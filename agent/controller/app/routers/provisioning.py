"""Admin API for provisioning token management."""
import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.models.provisioning_token import ProvisioningToken

router = APIRouter(prefix="/provisioning-tokens", tags=["provisioning"])


class TokenCreate(BaseModel):
    device_name: str | None = None
    notes: str | None = None
    expires_in_hours: int | None = 24


class TokenRead(BaseModel):
    id: int
    token: str
    device_name: str | None
    notes: str | None
    created_at: datetime.datetime
    expires_at: datetime.datetime | None
    used_at: datetime.datetime | None
    valid: bool

    model_config = {"from_attributes": True}


@router.post("", response_model=TokenRead, status_code=201)
async def create_token(body: TokenCreate, session: AsyncSession = Depends(get_session)):
    expires_at = None
    if body.expires_in_hours is not None:
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=body.expires_in_hours)

    token = ProvisioningToken(
        token=ProvisioningToken.generate_token(),
        device_name=body.device_name,
        notes=body.notes,
        expires_at=expires_at,
    )
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return TokenRead(
        id=token.id,
        token=token.token,
        device_name=token.device_name,
        notes=token.notes,
        created_at=token.created_at,
        expires_at=token.expires_at,
        used_at=token.used_at,
        valid=token.is_valid,
    )


@router.get("", response_model=list[TokenRead])
async def list_tokens(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(ProvisioningToken).order_by(ProvisioningToken.created_at.desc())
    )
    tokens = result.scalars().all()
    return [
        TokenRead(
            id=t.id,
            token=t.token,
            device_name=t.device_name,
            notes=t.notes,
            created_at=t.created_at,
            expires_at=t.expires_at,
            used_at=t.used_at,
            valid=t.is_valid,
        )
        for t in tokens
    ]


@router.delete("/{token_id}", status_code=204)
async def delete_token(token_id: int, session: AsyncSession = Depends(get_session)):
    token = await session.get(ProvisioningToken, token_id)
    if not token:
        raise HTTPException(404, "Token not found")
    await session.delete(token)
    await session.commit()
