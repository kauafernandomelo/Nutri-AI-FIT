"""Repositório de pesos."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.weight import Weight
from app.repositories.base import BaseRepository


class WeightRepository(BaseRepository[Weight]):
    def __init__(self, db: Session) -> None:
        super().__init__(Weight, db)

    def list_for_user(self, user_id: int) -> list[Weight]:
        stmt = (
            select(Weight)
            .where(Weight.user_id == user_id)
            .order_by(Weight.recorded_at.desc(), Weight.id.desc())
        )
        return list(self.db.scalars(stmt).all())

    def get_latest(self, user_id: int) -> Weight | None:
        stmt = (
            select(Weight)
            .where(Weight.user_id == user_id)
            .order_by(Weight.recorded_at.desc(), Weight.id.desc())
            .limit(1)
        )
        return self.db.scalar(stmt)
