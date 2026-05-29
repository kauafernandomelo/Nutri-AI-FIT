"""Modelo de usuário."""
from sqlalchemy import Boolean, Enum as SAEnum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import Sex


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    # email é único e indexado: busca rápida no login + impede duplicatas.
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Dados de perfil (preenchidos no onboarding, por isso nullable).
    sex: Mapped[Sex | None] = mapped_column(SAEnum(Sex, name="sex_enum"), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relacionamentos. cascade="all, delete-orphan" → apagar o usuário apaga os
    # dados dependentes (consistência + LGPD/privacidade: nada órfão fica para trás).
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    meals = relationship("MealLog", back_populates="user", cascade="all, delete-orphan")
    weights = relationship("Weight", back_populates="user", cascade="all, delete-orphan")
    streak = relationship(
        "Streak", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
