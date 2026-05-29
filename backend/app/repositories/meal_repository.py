"""Repositório de refeições."""
from datetime import date, datetime, time, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.meal_log import MealLog
from app.repositories.base import BaseRepository


class MealRepository(BaseRepository[MealLog]):
    def __init__(self, db: Session) -> None:
        super().__init__(MealLog, db)

    @staticmethod
    def _day_bounds(day: date) -> tuple[datetime, datetime]:
        """Intervalo [00:00, 24:00) do dia, em UTC (consumed_at é timezone-aware)."""
        start = datetime.combine(day, time.min, tzinfo=timezone.utc)
        end = datetime.combine(day, time.max, tzinfo=timezone.utc)
        return start, end

    def list_for_user(
        self, user_id: int, *, limit: int = 50, offset: int = 0
    ) -> list[MealLog]:
        stmt = (
            select(MealLog)
            .where(MealLog.user_id == user_id)
            .order_by(MealLog.consumed_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    def list_for_day(self, user_id: int, day: date) -> list[MealLog]:
        start, end = self._day_bounds(day)
        stmt = (
            select(MealLog)
            .where(
                MealLog.user_id == user_id,
                MealLog.consumed_at >= start,
                MealLog.consumed_at <= end,
            )
            .order_by(MealLog.consumed_at.asc())
        )
        return list(self.db.scalars(stmt).all())

    def day_totals(self, user_id: int, day: date) -> dict[str, float]:
        """Soma de calorias e macros do dia (agregação no banco — eficiente)."""
        start, end = self._day_bounds(day)
        stmt = select(
            func.coalesce(func.sum(MealLog.calories), 0.0),
            func.coalesce(func.sum(MealLog.protein_g), 0.0),
            func.coalesce(func.sum(MealLog.carbs_g), 0.0),
            func.coalesce(func.sum(MealLog.fat_g), 0.0),
            func.count(MealLog.id),
        ).where(
            MealLog.user_id == user_id,
            MealLog.consumed_at >= start,
            MealLog.consumed_at <= end,
        )
        calories, protein, carbs, fat, count = self.db.execute(stmt).one()
        return {
            "calories": float(calories),
            "protein_g": float(protein),
            "carbs_g": float(carbs),
            "fat_g": float(fat),
            "count": int(count),
        }
