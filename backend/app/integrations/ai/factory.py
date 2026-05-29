"""
Factory: decide qual analisador usar com base no .env (AI_PROVIDER).

Quem precisa de um analisador chama get_nutrition_analyzer() e recebe a
implementação certa, sem saber qual é. Adicionar um novo provedor no futuro =
mais um `if` aqui, nada mais.
"""
from app.core.config import settings
from app.integrations.ai.base import AbstractNutritionAnalyzer
from app.integrations.ai.mock_analyzer import MockNutritionAnalyzer


def get_nutrition_analyzer() -> AbstractNutritionAnalyzer:
    provider = (settings.AI_PROVIDER or "mock").lower()
    if provider == "gemini":
        # Import preguiçoso: só carrega o SDK do Gemini se realmente for usado.
        from app.integrations.ai.gemini_analyzer import GeminiNutritionAnalyzer

        return GeminiNutritionAnalyzer()
    return MockNutritionAnalyzer()
