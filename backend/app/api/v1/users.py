"""Rotas de usuário: /users/me (ler e atualizar perfil do onboarding)."""
from fastapi import APIRouter

from app.api.deps import CurrentUser, DbDep
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def read_me(current_user: CurrentUser) -> UserRead:
    return UserRead.model_validate(current_user)


@router.patch("/me", response_model=UserRead)
def update_me(payload: UserUpdate, current_user: CurrentUser, db: DbDep) -> UserRead:
    user = UserService(db).update_profile(current_user, payload)
    return UserRead.model_validate(user)
