"""Testes de cadastro, login e proteção de rotas."""
from tests.conftest import register_and_login


def test_register_returns_user(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"name": "João", "email": "joao@example.com", "password": "senha12345"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "joao@example.com"
    assert "hashed_password" not in body  # nunca expomos o hash


def test_duplicate_email_conflicts(client):
    payload = {"name": "Maria", "email": "dup@example.com", "password": "senha12345"}
    client.post("/api/v1/auth/register", json=payload)
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_and_access_me(client):
    headers = register_and_login(client, email="login@example.com")
    resp = client.get("/api/v1/users/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "login@example.com"


def test_wrong_password_unauthorized(client):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Y", "email": "y@example.com", "password": "senha12345"},
    )
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "y@example.com", "password": "errada"},
    )
    assert resp.status_code == 401


def test_me_requires_token(client):
    assert client.get("/api/v1/users/me").status_code == 401
