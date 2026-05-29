"""Modelo de meta (objetivo + peso-alvo + meta calórica calculada)."""
from sqlalchemy import Boolean, Enum as SAEnum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ActivityLevel, Objective


class Goal(Base, TimestampMixin):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    objective: Mapped[Objective] = mapped_column(
        SAEnum(Objective, name="objective_enum"), nullable=False
    )
    start_weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    target_weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    activity_level: Mapped[ActivityLevel] = mapped_column(
        SAEnum(ActivityLevel, name="activity_level_enum"),
        default=ActivityLevel.moderate,
        nullable=False,
    )
    # Calculada pelo nutrition_calculator a partir do perfil + objetivo.
    daily_calorie_target: Mapped[int] = mapped_column(Integer, nullable=False)

    # Permitimos histórico de metas; apenas uma fica is_active=True por usuário
    # (regra garantida na camada de serviço).
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="goals")
