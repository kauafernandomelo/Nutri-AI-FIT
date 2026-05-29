"""
Funções de segurança: hash de senha (bcrypt) e tokens JWT.

DECISÕES (confidencialidade):
- Senha é guardada SOMENTE como hash bcrypt (com "sal" aleatório embutido).
  bcrypt é lento de propósito → dificulta ataques de força bruta.
- O JWT carrega APENAS o id do usuário em `sub`. Nada de e-mail, peso ou dados
  de saúde no token (se o token vazar, não vaza PII).
- Limite de 72 bytes do bcrypt é tratado validando o tamanho da senha no schema.
"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


# --------------------------- Senhas (bcrypt) ---------------------------------
def hash_password(plain_password: str) -> str:
    """Gera o hash bcrypt de uma senha em texto puro."""
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara senha em texto puro com o hash salvo (em tempo constante)."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except ValueError:
        # Hash malformado no banco — falha de forma segura.
        return False


# ----------------------------- JWT (acesso) ----------------------------------
def create_access_token(subject: str | int, expires_minutes: int | None = None) -> str:
    """Cria um JWT assinado contendo apenas o id do usuário (`sub`)."""
    now = datetime.now(timezone.utc)
    expire = now + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Valida assinatura + expiração e devolve o payload. Lança jwt.PyJWTError se inválido."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
