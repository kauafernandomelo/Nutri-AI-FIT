"""
Regra de negócio do STREAK (dias consecutivos com registro de refeição).

Duas operações:
- register_activity(): chamada quando o usuário registra uma refeição. Incrementa
  ou reinicia o streak conforme o último dia registrado.
- effective_streak(): chamada na LEITURA (dashboard). Se o usuário passou um dia
  inteiro sem registrar, o streak "quebrou" → mostramos (e persistimos) 0.

Os métodos fazem flush; o COMMIT é responsabilidade do serviço que orquestra
(meal_service ao registrar, dashboard_service ao ler).
"""
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.streak import Streak
from app.repositories.streak_repository import StreakRepository
from app.utils.datetime import today


class StreakService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = StreakRepository(db)

    def get_or_create(self, user_id: int) -> Streak:
        streak = self.repo.get_by_user(user_id)
        if streak is None:
            streak = Streak(
                user_id=user_id, current_streak=0, longest_streak=0, last_logged_date=None
            )
            self.repo.add(streak)
        return streak

    def register_activity(self, user_id: int, day: date | None = None) -> Streak:
        day = day or today()
        streak = self.get_or_create(user_id)
        last = streak.last_logged_date

        if last == day:
            pass  # já registrou hoje — streak não muda
        elif last == day - timedelta(days=1):
            streak.current_streak += 1  # dia consecutivo
        else:
            streak.current_streak = 1  # primeiro registro ou houve um buraco

        # Avança a data apenas para frente (ignora registros retroativos).
        if last is None or day > last:
            streak.last_logged_date = day

        streak.longest_streak = max(streak.longest_streak, streak.current_streak)
        self.db.flush()
        return streak

    def effective_streak(self, user_id: int, day: date | None = None) -> Streak:
        day = day or today()
        streak = self.repo.get_by_user(user_id)
        if streak is None:
            return self.get_or_create(user_id)

        # Quebrou se o último registro foi anteontem ou antes (ontem ainda vale).
        broken = streak.last_logged_date is None or streak.last_logged_date < day - timedelta(days=1)
        if broken and streak.current_streak != 0:
            streak.current_streak = 0
            self.db.flush()
        return streak
