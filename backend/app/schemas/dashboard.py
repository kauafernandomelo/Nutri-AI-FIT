"""Schema da resposta agregada do dashboard (a tela Home consome isto)."""
from datetime import date

from pydantic import BaseModel


class MacroSummary(BaseModel):
    protein_g: float
    carbs_g: float
    fat_g: float


class DashboardResponse(BaseModel):
    date: date
    calories_consumed: float
    daily_calorie_target: int | None
    calories_remaining: int | None
    macros_today: MacroSummary
    meals_today: int
    current_streak: int
    longest_streak: int
    current_weight_kg: float | None
    target_weight_kg: float | None
    objective: str | None
    motivational_message: str
