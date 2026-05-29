"""
Analisador FAKE (mock) para desenvolvimento/testes.

Devolve dados nutricionais plausíveis SEM chamar nenhuma API externa, então o app
funciona ponta a ponta de graça e offline. A escolha do prato é determinística por
imagem (hash dos bytes) — a mesma foto gera sempre o mesmo resultado, o que deixa
os testes estáveis.
"""
import hashlib
import random

from app.integrations.ai.base import AbstractNutritionAnalyzer
from app.schemas.meal import MealItem, NutritionAnalysisResult

# Catálogo de pratos plausíveis: (nome do prato, [(alimento, qtd, kcal, prot, carb, gord)])
_CATALOG: list[tuple[str, list[tuple[str, str, float, float, float, float]]]] = [
    (
        "Prato de arroz, feijão e frango grelhado",
        [
            ("Arroz branco", "4 col. sopa", 205, 4, 45, 0.4),
            ("Feijão carioca", "1 concha", 115, 7, 20, 0.5),
            ("Frango grelhado", "1 filé (120g)", 195, 36, 0, 4),
            ("Salada verde", "à vontade", 35, 2, 6, 0.3),
        ],
    ),
    (
        "Salada Caesar com frango",
        [
            ("Alface", "1 prato", 15, 1, 3, 0.2),
            ("Frango em cubos", "100g", 165, 31, 0, 3.6),
            ("Croutons", "punhado", 90, 2, 14, 3),
            ("Molho Caesar", "2 col. sopa", 160, 1, 2, 17),
        ],
    ),
    (
        "Hambúrguer com batata frita",
        [
            ("Hambúrguer bovino", "1 unidade", 350, 20, 30, 17),
            ("Batata frita", "porção média", 365, 4, 48, 17),
        ],
    ),
    (
        "Tigela de aveia com frutas",
        [
            ("Aveia", "1/2 xícara", 150, 5, 27, 3),
            ("Banana", "1 unidade", 105, 1, 27, 0.4),
            ("Morangos", "punhado", 30, 0.6, 7, 0.3),
            ("Mel", "1 col. chá", 21, 0, 6, 0),
        ],
    ),
    (
        "Macarrão à bolonhesa",
        [
            ("Macarrão", "1 prato", 320, 12, 62, 2),
            ("Molho bolonhesa", "1 concha", 220, 14, 9, 13),
            ("Queijo ralado", "1 col. sopa", 40, 3, 0.4, 3),
        ],
    ),
]


class MockNutritionAnalyzer(AbstractNutritionAnalyzer):
    provider_name = "mock"

    async def analyze(self, image_bytes: bytes, mime_type: str) -> NutritionAnalysisResult:
        # Semente determinística a partir do conteúdo da imagem.
        seed = int(hashlib.sha256(image_bytes or b"empty").hexdigest(), 16)
        rng = random.Random(seed)
        name, raw_items = rng.choice(_CATALOG)

        items: list[MealItem] = []
        for food, qty, kcal, prot, carb, fat in raw_items:
            # variação leve (±8%) para parecer uma "estimativa" real
            f = 1 + rng.uniform(-0.08, 0.08)
            items.append(
                MealItem(
                    name=food,
                    quantity=qty,
                    calories=round(kcal * f, 1),
                    protein_g=round(prot * f, 1),
                    carbs_g=round(carb * f, 1),
                    fat_g=round(fat * f, 1),
                )
            )

        return NutritionAnalysisResult(
            name=name,
            description="Estimativa gerada pelo analisador de demonstração (mock).",
            calories=round(sum(i.calories for i in items), 1),
            protein_g=round(sum(i.protein_g for i in items), 1),
            carbs_g=round(sum(i.carbs_g for i in items), 1),
            fat_g=round(sum(i.fat_g for i in items), 1),
            items=items,
        )
