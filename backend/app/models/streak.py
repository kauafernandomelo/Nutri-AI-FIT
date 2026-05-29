"""Modelo de streak (dias consecutivos com registro de refeição)."""
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Streak(Base, TimestampMixin):
    __tablename__ = "streaks"

    id: Mapped[int] = mapped_column(primary_key=True)
    # unique → exatamente UM registro de streak por usuário (relação 1-1).
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False
    )

    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # Último dia em que o usuário registrou alguma refeição (base do cálculo).
    last_logged_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    user = relationship("User", back_populates="streak")
