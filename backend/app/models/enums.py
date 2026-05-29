"""
Enumerações do domínio.

POR QUE enums: garantem que só valores válidos entrem no banco (uma constraint
a mais contra dados inconsistentes). Herdam de `str` para serializar bem em JSON.
"""
import enum


class Sex(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class Objective(str, enum.Enum):
    lose_weight = "lose_weight"   # Emagrecer
    gain_muscle = "gain_muscle"   # Ganhar massa
    maintain = "maintain"         # Manter peso


class ActivityLevel(str, enum.Enum):
    sedentary = "sedentary"       # fator 1.2
    light = "light"               # fator 1.375
    moderate = "moderate"         # fator 1.55
    active = "active"             # fator 1.725
    very_active = "very_active"   # fator 1.9


class MessageCategory(str, enum.Enum):
    streak = "streak"
    consistency = "consistency"
    goal_progress = "goal_progress"
    generic = "generic"
