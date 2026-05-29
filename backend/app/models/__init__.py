"""
Importa todos os modelos em um só lugar.

POR QUE: o Alembic (autogenerate) e o `Base.metadata` precisam que TODAS as
classes estejam importadas para "enxergar" as tabelas. Importar aqui garante isso
com um único `import app.models`.
"""
from app.models.base import Base
from app.models.enums import ActivityLevel, MessageCategory, Objective, Sex
from app.models.goal import Goal
from app.models.meal_log import MealLog
from app.models.motivational_message import MotivationalMessage
from app.models.streak import Streak
from app.models.user import User
from app.models.weight import Weight

__all__ = [
    "Base",
    "User",
    "Goal",
    "MealLog",
    "Streak",
    "Weight",
    "MotivationalMessage",
    "Sex",
    "Objective",
    "ActivityLevel",
    "MessageCategory",
]
