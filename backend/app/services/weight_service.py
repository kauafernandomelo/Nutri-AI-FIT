"""Serviço de pesos."""
from sqlalchemy.orm import Session

from app.models.weight import Weight
from app.repositories.weight_repository import WeightRepository
from app.schemas.weight import WeightCreate
from app.utils.datetime import today


class WeightService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = WeightRepository(db)

    def create(self, user_id: int, data: WeightCreate) -> Weight:
        record = Weight(
            user_id=user_id,
            weight_kg=data.weight_kg,
            recorded_at=data.recorded_at or today(),
        )
        self.repo.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list(self, user_id: int) -> list[Weight]:
        return self.repo.list_for_user(user_id)

    def latest(self, user_id: int) -> Weight | None:
        return self.repo.get_latest(user_id)
