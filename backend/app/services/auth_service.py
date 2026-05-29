"""Serviço de autenticação: cadastro e login."""
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import hash_password, verify_password
from app.models.streak import Streak
from app.models.user import User
from app.repositories.streak_repository import StreakRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.streaks = StreakRepository(db)

    def register(self, data: RegisterRequest) -> User:
        if self.users.get_by_email(data.email):
            # Mensagem neutra — não confirma/nega de forma exploitável.
            raise ConflictError("Não foi possível concluir o cadastro com esses dados.")

        user = User(
            name=data.name,
            email=str(data.email),
            hashed_password=hash_password(data.password),
        )
        self.users.add(user)
        # Já cria o registro de streak zerado (relação 1-1).
        self.streaks.add(Streak(user_id=user.id, current_streak=0, longest_streak=0))
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> User:
        user = self.users.get_by_email(email)
        # Mesmo erro para "email não existe" e "senha errada" → não vaza quais
        # emails estão cadastrados.
        if user is None or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("E-mail ou senha inválidos.")
        if not user.is_active:
            raise UnauthorizedError("Conta inativa.")
        return user
