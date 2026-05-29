"""Rotas de metas: criar e listar."""
from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbDep
from app.schemas.goal import GoalCreate, GoalRead
from app.services.goal_service import GoalService

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("", response_model=GoalRead, status_code=status.HTTP_201_CREATED)
def create_goal(payload: GoalCreate, current_user: CurrentUser, db: DbDep) -> GoalRead:
    goal = GoalService(db).create(current_user, payload)
    return GoalRead.model_validate(goal)


@router.get("", response_model=list[GoalRead])
def list_goals(current_user: CurrentUser, db: DbDep) -> list[GoalRead]:
    goals = GoalService(db).list(current_user.id)
    return [GoalRead.model_validate(g) for g in goals]
