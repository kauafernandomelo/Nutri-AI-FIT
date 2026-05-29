"""Schemas de usuário (saída + atualização de perfil no onboarding)."""
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import Sex


class UserRead(BaseModel):
    # from_attributes → permite criar o schema direto de um objeto ORM.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    sex: Sex | None = None
    age: int | None = None
    height_cm: float | None = None
    is_active: bool


class UserUpdate(BaseModel):
    """Onboarding/edição de perfil. Todos opcionais (atualização parcial)."""
    name: str | None = Field(default=None, min_length=2, max_length=120)
    sex: Sex | None = None
    age: int | None = Field(default=None, ge=10, le=120)
    height_cm: float | None = Field(default=None, ge=50, le=260)
