"""Testes do fluxo de refeição (upload → IA mock → salvar → listar)."""
from tests.conftest import register_and_login

_FAKE_IMAGE = ("meal.jpg", b"conteudo-falso-de-imagem", "image/jpeg")


def test_create_meal_with_mock_ai(client):
    headers = register_and_login(client, email="meal@example.com")
    resp = client.post("/api/v1/meals", headers=headers, files={"file": _FAKE_IMAGE})
    assert resp.status_code == 201
    body = resp.json()
    assert body["calories"] > 0
    assert body["ai_provider"] == "mock"
    assert len(body["items"]) >= 1
    # A URL da imagem aponta para o endpoint autenticado, não para o disco.
    assert body["image_url"].endswith("/image")


def test_list_meals(client):
    headers = register_and_login(client, email="meal2@example.com")
    client.post("/api/v1/meals", headers=headers, files={"file": _FAKE_IMAGE})
    resp = client.get("/api/v1/meals", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_rejects_non_image(client):
    headers = register_and_login(client, email="meal3@example.com")
    resp = client.post(
        "/api/v1/meals",
        headers=headers,
        files={"file": ("doc.txt", b"texto", "text/plain")},
    )
    assert resp.status_code == 415


def test_cannot_see_other_users_meal_image(client):
    h1 = register_and_login(client, email="owner@example.com")
    meal_id = client.post("/api/v1/meals", headers=h1, files={"file": _FAKE_IMAGE}).json()["id"]
    h2 = register_and_login(client, email="intruder@example.com")
    resp = client.get(f"/api/v1/meals/{meal_id}/image", headers=h2)
    assert resp.status_code == 404  # não vaza imagem de outro usuário
