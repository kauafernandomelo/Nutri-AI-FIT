"""
Analisador real com Gemini Vision (Google).

Implementado, porém INATIVO por padrão (AI_PROVIDER=mock). Para ligar:
  1) coloque GEMINI_API_KEY no .env
  2) mude AI_PROVIDER=gemini

O import do SDK é PREGUIÇOSO (dentro do método) para que a ausência do pacote
ou da chave nunca atrapalhe quem está rodando no modo mock.
"""
import json

from app.core.config import settings
from app.integrations.ai.base import AbstractNutritionAnalyzer, NutritionAnalysisError
from app.schemas.meal import NutritionAnalysisResult

# Pedimos ao modelo um JSON estrito que casa com o nosso schema.
_PROMPT = """Você é um nutricionista. Analise a foto da refeição e responda
APENAS com um JSON válido (sem texto extra, sem markdown) neste formato:
{
  "name": "nome curto do prato",
  "description": "descrição breve",
  "calories": número (kcal totais),
  "protein_g": número, "carbs_g": número, "fat_g": número,
  "items": [
    {"name": "alimento", "quantity": "porção estimada",
     "calories": número, "protein_g": número, "carbs_g": número, "fat_g": número}
  ]
}
Os totais devem ser a soma dos itens. Estime quantidades de forma realista."""


class GeminiNutritionAnalyzer(AbstractNutritionAnalyzer):
    provider_name = "gemini"

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise NutritionAnalysisError("GEMINI_API_KEY não configurada no .env.")

    async def analyze(self, image_bytes: bytes, mime_type: str) -> NutritionAnalysisResult:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:  # pragma: no cover - só importa se ativado
            raise NutritionAnalysisError(
                "Pacote 'google-genai' não instalado. Rode: pip install google-genai"
            ) from exc

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    _PROMPT,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
            data = json.loads(response.text)
            # Pydantic valida o formato; se a IA fugir do contrato, levanta erro claro.
            return NutritionAnalysisResult.model_validate(data)
        except Exception as exc:  # noqa: BLE001
            raise NutritionAnalysisError(f"Falha ao analisar com Gemini: {exc}") from exc
