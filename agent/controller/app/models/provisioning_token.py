import secrets
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ProvisioningToken(SQLModel, table=True):
    __tablename__ = "provisioning_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True)
    device_name: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(default=None)
    used_at: Optional[datetime] = Field(default=None)  # None = not yet used

    @staticmethod
    def generate_token() -> str:
        return secrets.token_hex(32)

    @property
    def is_valid(self) -> bool:
        if self.used_at is not None:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True
