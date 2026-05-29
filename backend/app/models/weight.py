"""Modelo de registro de peso (histórico para acompanhar a evolução)."""
from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Weight(Base, TimestampMixin):
    __tablename__ = "weights"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[date] = mapped_column(Date, nullable=False)

    user = relationship("User", back_populates="weights")

    # Índice para buscar/ordenar o histórico de peso de um usuário por data.
    __table_args__ = (Index("ix_weights_user_recorded", "user_id", "recorded_at"),)
