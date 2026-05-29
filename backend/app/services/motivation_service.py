"""
Seleciona uma mensagem motivacional conforme o contexto do usuário.

Regra simples e automática (sem IA):
- Se o streak atingiu um marco (min_streak), mostra a mensagem do MAIOR marco
  alcançado (a mais "impressionante").
- Caso contrário, escolhe uma mensagem genérica/consistência/progresso.
"""
import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import MessageCategory
from app.models.motivational_message import MotivationalMessage

_FALLBACK = "Continue registrando suas refeições. Você consegue!"


class MotivationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def pick(self, *, current_streak: int) -> str:
        messages = list(
            self.db.scalars(
                select(MotivationalMessage).where(MotivationalMessage.is_active.is_(True))
            ).all()
        )
        if not messages:
            return _FALLBACK

        # 1) Marcos de streak alcançados.
        reached = [
            m
            for m in messages
            if m.category == MessageCategory.streak
            and m.min_streak is not None
            and current_streak >= m.min_streak
        ]
        if reached:
            best = max(reached, key=lambda m: m.min_streak or 0)
            return best.text

        # 2) Mensagens "sempre elegíveis".
        general = [
            m
            for m in messages
            if m.category
            in (MessageCategory.generic, MessageCategory.consistency, MessageCategory.goal_progress)
            and m.min_streak is None
        ]
        if general:
            return random.choice(general).text

        return _FALLBACK
