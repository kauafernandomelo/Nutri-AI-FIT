"""Repositório de metas."""
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.repositories.base import BaseRepository


class GoalRepository(BaseRepository[Goal]):
    def __init__(self, db: Session) -> None:
        super().__init__(Goal, db)

    def get_active_for_user(self, user_id: int) -> Goal | None:
        stmt = (
            select(Goal)
            .where(Goal.user_id == user_id, Goal.is_active.is_(True))
            .order_by(Goal.created_at.desc())
        )
        return self.db.scalar(stmt)

    def list_for_user(self, user_id: int) -> list[Goal]:
        stmt = (
            select(Goal)
            .where(Goal.user_id == user_id)
            .order_by(Goal.created_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def deactivate_all_for_user(self, user_id: int) -> None:
        """Mantém apenas uma meta ativa: desativa as anteriores."""
        self.db.execute(
            update(Goal).where(Goal.user_id == user_id).values(is_active=False)
        )
