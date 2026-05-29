"""
Conexão com o banco e fábrica de sessões SQLAlchemy 2.0.

POR QUE assim:
- `create_engine` lê a URL do .env → o código é AGNÓSTICO ao banco. Hoje aponta
  para PostgreSQL; trocar para SQLite (testes) é só mudar a DATABASE_URL.
- `pool_pre_ping=True` evita usar conexões mortas (boa prática em produção).
- `get_db()` é uma dependência do FastAPI: abre uma sessão por requisição e
  SEMPRE a fecha no final (mesmo se der erro) — sem vazamento de conexões.
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# SQLite precisa deste argumento extra quando usado com múltiplas threads (testes).
_connect_args: dict = {}
if settings.DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    connect_args=_connect_args,
    echo=False,  # mude para True para ver o SQL gerado (debug/aprendizado)
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,  # objetos seguem utilizáveis após o commit
)


def get_db() -> Generator[Session, None, None]:
    """Dependência: fornece uma sessão e garante o fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
