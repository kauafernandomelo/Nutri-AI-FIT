"""Schemas de meta."""
from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ActivityLevel, Objective


class GoalCreate(BaseModel):
    objective: Objective
    start_weight_kg: float = Field(gt=0, le=500)
    target_weight_kg: float = Field(gt=0, le=500)
    activity_level: ActivityLevel = ActivityLevel.moderate


class GoalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    objective: Objective
    start_weight_kg: float
    target_weight_kg: float
    activity_level: ActivityLevel
    daily_calorie_target: int
    is_active: bool
