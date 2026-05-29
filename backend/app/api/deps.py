"""
Dependências reutilizáveis (injeção de dependência do FastAPI).

Aqui ficam os "plugues" que os endpoints pedem via Depends():
- DbDep: a sessão de banco da requisição.
- CurrentUser: o usuário autenticado (valida o JWT).
- AnalyzerDep / StorageDep: as integrações escolhidas no .env (mock/gemini, local/r2).
"""
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.database.session import get_db
from app.integrations.ai.base import AbstractNutritionAnalyzer
from app.integrations.ai.factory import get_nutrition_analyzer
from app.integrations.storage.base import AbstractStorage
from app.integrations.storage.factory import get_storage
from app.models.user import User
from app.repositories.user_repository import UserRepository

# tokenUrl: caminho onde o Swagger envia username/senha para obter o token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

DbDep = Annotated[Session, Depends(get_db)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DbDep
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
        user_id = int(subject)
    except (jwt.PyJWTError, ValueError, TypeError):
        raise credentials_exception

    user = UserRepository(db).get(user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_analyzer() -> AbstractNutritionAnalyzer:
    return get_nutrition_analyzer()


def get_storage_dep() -> AbstractStorage:
    return get_storage()


AnalyzerDep = Annotated[AbstractNutritionAnalyzer, Depends(get_analyzer)]
StorageDep = Annotated[AbstractStorage, Depends(get_storage_dep)]
