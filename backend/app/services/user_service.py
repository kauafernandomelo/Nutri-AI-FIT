"""Serviço de usuário: leitura e atualização de perfil (onboarding)."""
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)

    def get(self, user_id: int) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise NotFoundError("Usuário não encontrado.")
        return user

    def update_profile(self, user: User, data: UserUpdate) -> User:
        # exclude_unset → atualiza só os campos enviados (PATCH parcial).
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user
