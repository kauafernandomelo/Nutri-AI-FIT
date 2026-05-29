"""Schemas de refeição + o CONTRATO de análise nutricional da IA."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MealItem(BaseModel):
    """Um alimento individual detectado na foto."""
    name: str
    quantity: str | None = None  # ex.: "1 prato", "150 g"
    calories: float = 0.0
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0


class NutritionAnalysisResult(BaseModel):
    """
    CONTRATO de saída de qualquer analyzer de IA (mock, Gemini, futuros).

    Manter este formato fixo é o que torna a troca de IA transparente para o
    resto do sistema (princípio de inversão de dependência — SOLID 'D').
    """
    name: str
    description: str | None = None
    calories: float = Field(ge=0)
    protein_g: float = Field(ge=0)
    carbs_g: float = Field(ge=0)
    fat_g: float = Field(ge=0)
    items: list[MealItem] = []


class MealRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    items: list | None
    image_url: str | None
    ai_provider: str | None
    consumed_at: datetime
