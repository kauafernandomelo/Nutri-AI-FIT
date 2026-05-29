"""Serviço de metas: cria a meta calculando o alvo calórico."""
from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError
from app.models.goal import Goal
from app.models.user import User
from app.repositories.goal_repository import GoalRepository
from app.schemas.goal import GoalCreate
from app.services.nutrition_calculator import daily_calorie_target


class GoalService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.goals = GoalRepository(db)

    def create(self, user: User, data: GoalCreate) -> Goal:
        # O cálculo de calorias precisa do perfil — exigimos onboarding completo.
        if user.sex is None or user.age is None or user.height_cm is None:
            raise BadRequestError(
                "Complete seu perfil (sexo, idade e altura) antes de definir a meta."
            )

        target = daily_calorie_target(
            sex=user.sex,
            weight_kg=data.start_weight_kg,
            height_cm=user.height_cm,
            age=user.age,
            activity=data.activity_level,
            objective=data.objective,
        )

        # Garante uma única meta ativa por usuário.
        self.goals.deactivate_all_for_user(user.id)
        goal = Goal(
            user_id=user.id,
            objective=data.objective,
            start_weight_kg=data.start_weight_kg,
            target_weight_kg=data.target_weight_kg,
            activity_level=data.activity_level,
            daily_calorie_target=target,
            is_active=True,
        )
        self.goals.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def list(self, user_id: int) -> list[Goal]:
        return self.goals.list_for_user(user_id)

    def get_active(self, user_id: int) -> Goal | None:
        return self.goals.get_active_for_user(user_id)
