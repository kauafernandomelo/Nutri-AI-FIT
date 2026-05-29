"""Rotas de peso: registrar e listar histórico."""
from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbDep
from app.schemas.weight import WeightCreate, WeightRead
from app.services.weight_service import WeightService

router = APIRouter(prefix="/weights", tags=["weights"])


@router.post("", response_model=WeightRead, status_code=status.HTTP_201_CREATED)
def create_weight(payload: WeightCreate, current_user: CurrentUser, db: DbDep) -> WeightRead:
    record = WeightService(db).create(current_user.id, payload)
    return WeightRead.model_validate(record)


@router.get("", response_model=list[WeightRead])
def list_weights(current_user: CurrentUser, db: DbDep) -> list[WeightRead]:
    records = WeightService(db).list(current_user.id)
    return [WeightRead.model_validate(w) for w in records]
