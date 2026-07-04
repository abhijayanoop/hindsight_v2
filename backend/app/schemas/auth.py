"""Request/response models for authentication (api/v1/routers/auth.py).

Shapes are settled; the logic behind them (`services/auth_service.py`,
`dependencies.py`) is stubbed until Day 1.
"""

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str | None = None
    tenant_name: str = Field(..., description="Tenant to create or join.")


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None
    tenant_id: UUID
    is_active: bool
    roles: list[str] = []

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
