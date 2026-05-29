"""Repositório de streak."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.streak import Streak
from app.repositories.base import BaseRepository


class StreakRepository(BaseRepository[Streak]):
    def __init__(self, db: Session) -> None:
        super().__init__(Streak, db)

    def get_by_user(self, user_id: int) -> Streak | None:
        stmt = select(Streak).where(Streak.user_id == user_id)
        return self.db.scalar(stmt)
