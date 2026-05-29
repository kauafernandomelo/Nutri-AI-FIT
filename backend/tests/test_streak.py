"""Testes unitários da lógica de streak (com datas controladas)."""
from datetime import date, timedelta

from app.models.user import User
from app.services.streak_service import StreakService


def _make_user(db) -> int:
    user = User(name="S", email="s@example.com", hashed_password="x")
    db.add(user)
    db.commit()
    return user.id


def test_consecutive_days_increment(db_session):
    uid = _make_user(db_session)
    svc = StreakService(db_session)
    d0 = date(2026, 1, 1)
    assert svc.register_activity(uid, d0).current_streak == 1
    assert svc.register_activity(uid, d0 + timedelta(days=1)).current_streak == 2
    assert svc.register_activity(uid, d0 + timedelta(days=2)).current_streak == 3


def test_same_day_does_not_increment(db_session):
    uid = _make_user(db_session)
    svc = StreakService(db_session)
    d0 = date(2026, 1, 1)
    svc.register_activity(uid, d0)
    assert svc.register_activity(uid, d0).current_streak == 1  # mesmo dia


def test_gap_resets_to_one(db_session):
    uid = _make_user(db_session)
    svc = StreakService(db_session)
    d0 = date(2026, 1, 1)
    svc.register_activity(uid, d0)
    svc.register_activity(uid, d0 + timedelta(days=1))  # streak 2
    # pula um dia inteiro → reinicia em 1
    assert svc.register_activity(uid, d0 + timedelta(days=3)).current_streak == 1


def test_longest_streak_is_kept(db_session):
    uid = _make_user(db_session)
    svc = StreakService(db_session)
    d0 = date(2026, 1, 1)
    svc.register_activity(uid, d0)
    svc.register_activity(uid, d0 + timedelta(days=1))
    svc.register_activity(uid, d0 + timedelta(days=2))  # streak 3
    streak = svc.register_activity(uid, d0 + timedelta(days=10))  # quebra → 1
    assert streak.current_streak == 1
    assert streak.longest_streak == 3


def test_effective_streak_breaks_after_missing_day(db_session):
    uid = _make_user(db_session)
    svc = StreakService(db_session)
    today = date(2026, 1, 10)
    svc.register_activity(uid, today - timedelta(days=3))  # último registro: 3 dias atrás
    eff = svc.effective_streak(uid, today)
    assert eff.current_streak == 0  # quebrou
