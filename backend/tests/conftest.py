"""
Configuração compartilhada dos testes.

ESTRATÉGIA:
- Banco SQLite EM MEMÓRIA (rápido, isolado, não toca o Postgres).
- StaticPool + uma única conexão → todas as sessões enxergam o mesmo banco.
- Sobrescrevemos a dependência get_db do app para usar esse banco de teste.
- Rate limiting desligado (senão os limites atrapalhariam a suíte).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.rate_limit import limiter
from app.database.session import get_db
from app.main import app
from app.models.base import Base
from app.models.motivational_message import MotivationalMessage
from app.utils.seed import MESSAGES


def _build_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine


def _seed(session_factory) -> None:
    db = session_factory()
    try:
        db.add_all(
            MotivationalMessage(category=c, text=t, min_streak=m, is_active=True)
            for c, t, m in MESSAGES
        )
        db.commit()
    finally:
        db.close()


@pytest.fixture()
def session_factory():
    engine = _build_engine()
    factory = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
    )
    _seed(factory)
    yield factory
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db_session(session_factory):
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session_factory):
    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    limiter.enabled = False
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    limiter.enabled = True


# ----------------------------- Helpers ---------------------------------------
def register_and_login(client: TestClient, email: str = "ana@example.com") -> dict:
    """Cadastra, faz login e devolve o header Authorization pronto."""
    client.post(
        "/api/v1/auth/register",
        json={"name": "Ana Teste", "email": email, "password": "senha12345"},
    )
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "senha12345"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
