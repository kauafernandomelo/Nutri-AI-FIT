"""Rotas de autenticação: /auth/register e /auth/login."""
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import DbDep
from app.core.rate_limit import limiter
from app.core.security import create_access_token
from app.schemas.auth import RegisterRequest
from app.schemas.token import Token
from app.schemas.user import UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # limite rígido: anti-abuso no cadastro
def register(request: Request, payload: RegisterRequest, db: DbDep) -> UserRead:
    user = AuthService(db).register(payload)
    return UserRead.model_validate(user)


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")  # anti força-bruta
def login(
    request: Request,
    db: DbDep,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # No formulário OAuth2, o campo "username" carrega o e-mail.
    user = AuthService(db).authenticate(form.username, form.password)
    access_token = create_access_token(user.id)
    return Token(access_token=access_token)
