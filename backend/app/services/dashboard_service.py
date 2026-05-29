"""
Serviço do dashboard: agrega os dados da tela Home em uma única resposta.

Junta: calorias/macros de hoje, meta diária, streak (já validado), peso atual e
uma mensagem motivacional contextual.
"""
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.goal_repository import GoalRepository
from app.repositories.meal_repository import MealRepository
from app.repositories.weight_repository import WeightRepository
from app.schemas.dashboard import DashboardResponse, MacroSummary
from app.services.motivation_service import MotivationService
from app.services.streak_service import StreakService
from app.utils.datetime import today


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.meals = MealRepository(db)
        self.goals = GoalRepository(db)
        self.weights = WeightRepository(db)
        self.streaks = StreakService(db)
        self.motivation = MotivationService(db)

    def get(self, user: User) -> DashboardResponse:
        day = today()
        totals = self.meals.day_totals(user.id, day)
        goal = self.goals.get_active_for_user(user.id)
        streak = self.streaks.effective_streak(user.id, day)
        latest_weight = self.weights.get_latest(user.id)

        # Peso atual: último registrado; senão, o peso inicial da meta.
        current_weight = (
            latest_weight.weight_kg
            if latest_weight is not None
            else (goal.start_weight_kg if goal else None)
        )
        target = goal.daily_calorie_target if goal else None
        remaining = (
            target - round(totals["calories"]) if target is not None else None
        )

        message = self.motivation.pick(current_streak=streak.current_streak)

        # effective_streak pode ter zerado e dado flush — confirmamos aqui.
        self.db.commit()

        return DashboardResponse(
            date=day,
            calories_consumed=round(totals["calories"], 1),
            daily_calorie_target=target,
            calories_remaining=remaining,
            macros_today=MacroSummary(
                protein_g=round(totals["protein_g"], 1),
                carbs_g=round(totals["carbs_g"], 1),
                fat_g=round(totals["fat_g"], 1),
            ),
            meals_today=int(totals["count"]),
            current_streak=streak.current_streak,
            longest_streak=streak.longest_streak,
            current_weight_kg=current_weight,
            target_weight_kg=goal.target_weight_kg if goal else None,
            objective=goal.objective.value if goal else None,
            motivational_message=message,
        )
