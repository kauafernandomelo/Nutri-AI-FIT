"""Teste de ponta a ponta do dashboard (onboarding → meta → refeição → resumo)."""
from tests.conftest import register_and_login

_FAKE_IMAGE = ("meal.jpg", b"imagem-fake", "image/jpeg")


def test_full_flow_dashboard(client):
    headers = register_and_login(client, email="dash@example.com")

    # Onboarding: completa o perfil.
    client.patch(
        "/api/v1/users/me",
        headers=headers,
        json={"sex": "male", "age": 30, "height_cm": 178},
    )

    # Define a meta (calcula a meta calórica).
    goal = client.post(
        "/api/v1/goals",
        headers=headers,
        json={
            "objective": "lose_weight",
            "start_weight_kg": 85,
            "target_weight_kg": 78,
            "activity_level": "moderate",
        },
    ).json()
    assert goal["daily_calorie_target"] > 1200

    # Registra peso.
    client.post("/api/v1/weights", headers=headers, json={"weight_kg": 85})

    # Registra uma refeição.
    client.post("/api/v1/meals", headers=headers, files={"file": _FAKE_IMAGE})

    # Dashboard agrega tudo.
    resp = client.get("/api/v1/dashboard", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["calories_consumed"] > 0
    assert body["daily_calorie_target"] == goal["daily_calorie_target"]
    assert body["meals_today"] == 1
    assert body["current_streak"] == 1
    assert body["current_weight_kg"] == 85
    assert body["objective"] == "lose_weight"
    assert body["motivational_message"]  # não vazio


def test_goal_requires_profile(client):
    headers = register_and_login(client, email="noprofile@example.com")
    resp = client.post(
        "/api/v1/goals",
        headers=headers,
        json={
            "objective": "maintain",
            "start_weight_kg": 70,
            "target_weight_kg": 70,
            "activity_level": "moderate",
        },
    )
    assert resp.status_code == 400  # perfil incompleto
