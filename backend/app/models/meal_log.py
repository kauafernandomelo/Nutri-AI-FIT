"""Modelo de refeição registrada (resultado da análise da IA)."""
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Index,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class MealLog(Base, TimestampMixin):
    __tablename__ = "meal_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Macros totais da refeição.
    calories: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    protein_g: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    carbs_g: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    fat_g: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Lista de alimentos detectados pela IA: [{name, quantity, calories, ...}, ...]
    # JSON é flexível e suficiente para o MVP (não precisamos consultar por item).
    items: Mapped[list | None] = mapped_column(JSON, nullable=True)

    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Qual implementação de IA gerou o resultado (auditoria do desacoplamento).
    ai_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)

    consumed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", back_populates="meals")

    # Índice composto: o dashboard consulta "refeições do usuário X no dia Y".
    __table_args__ = (Index("ix_meal_logs_user_consumed", "user_id", "consumed_at"),)
