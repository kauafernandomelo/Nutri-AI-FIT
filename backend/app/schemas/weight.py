"""Schemas de peso."""
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class WeightCreate(BaseModel):
    weight_kg: float = Field(gt=0, le=500)
    recorded_at: date | None = None  # se None, o serviço usa a data de hoje


class WeightRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    weight_kg: float
    recorded_at: date
