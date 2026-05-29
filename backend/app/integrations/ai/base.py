"""
Contrato (interface) de qualquer analisador nutricional de imagem.

Este é o coração do desacoplamento da IA. O resto do sistema depende SOMENTE
desta interface e do schema NutritionAnalysisResult — nunca do Gemini diretamente
(princípio da Inversão de Dependência). Trocar de IA = nova classe que implementa
isto, sem tocar em services/endpoints.
"""
from abc import ABC, abstractmethod

from app.schemas.meal import NutritionAnalysisResult


class AbstractNutritionAnalyzer(ABC):
    #: identificador salvo em meal_logs.ai_provider (auditoria)
    provider_name: str = "abstract"

    @abstractmethod
    async def analyze(self, image_bytes: bytes, mime_type: str) -> NutritionAnalysisResult:
        """Recebe a imagem e devolve a estimativa nutricional padronizada."""
        raise NotImplementedError


class NutritionAnalysisError(Exception):
    """Erro ao analisar a imagem (problema com o provedor de IA)."""
