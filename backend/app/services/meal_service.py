"""
Serviço de refeições — o fluxo central de "foto -> nutrição".

create_from_image() orquestra, em UMA transação:
  1) salva a imagem no storage (local/R2);
  2) chama a IA (mock/Gemini) para estimar a nutrição;
  3) persiste o meal_log;
  4) atualiza o streak.
Se algo der errado, nada é confirmado (atomicidade).

Note como NÃO sabemos QUAL IA/storage estamos usando — recebemos as interfaces
por injeção de dependência. É o desacoplamento em ação.
"""
import uuid

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import NotFoundError, ServiceUnavailableError
from app.integrations.ai.base import AbstractNutritionAnalyzer, NutritionAnalysisError
from app.integrations.storage.base import AbstractStorage, StorageError
from app.models.meal_log import MealLog
from app.repositories.meal_repository import MealRepository
from app.schemas.meal import MealRead
from app.services.streak_service import StreakService

_EXT_BY_TYPE = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}
_TYPE_BY_EXT = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
}


def to_meal_read(meal: MealLog) -> MealRead:
    """Converte o ORM em DTO, trocando a key da imagem pela URL autenticada."""
    read = MealRead.model_validate(meal)
    if meal.image_url:
        read.image_url = (
            f"{settings.PUBLIC_BASE_URL}{settings.API_V1_PREFIX}/meals/{meal.id}/image"
        )
    return read


class MealService:
    def __init__(
        self,
        db: Session,
        analyzer: AbstractNutritionAnalyzer | None = None,
        storage: AbstractStorage | None = None,
    ) -> None:
        # analyzer/storage são opcionais: endpoints de listagem não precisam deles,
        # então não construímos cliente de IA sem necessidade.
        self.db = db
        self.analyzer = analyzer
        self.storage = storage
        self.meals = MealRepository(db)
        self.streaks = StreakService(db)

    async def create_from_image(
        self, user_id: int, content: bytes, content_type: str
    ) -> MealLog:
        if self.storage is None or self.analyzer is None:
            raise ServiceUnavailableError("Serviço de imagem/IA indisponível.")
        ext = _EXT_BY_TYPE.get(content_type, "jpg")
        # Key escopada ao usuário; uuid evita colisões e não revela nada.
        key = f"meals/{user_id}/{uuid.uuid4().hex}.{ext}"

        try:
            self.storage.save(content, key, content_type)
        except StorageError as exc:
            raise ServiceUnavailableError(f"Falha ao salvar a imagem: {exc}") from exc

        try:
            analysis = await self.analyzer.analyze(content, content_type)
        except NutritionAnalysisError as exc:
            raise ServiceUnavailableError(
                f"Não foi possível analisar a imagem: {exc}"
            ) from exc

        meal = MealLog(
            user_id=user_id,
            name=analysis.name,
            description=analysis.description,
            calories=analysis.calories,
            protein_g=analysis.protein_g,
            carbs_g=analysis.carbs_g,
            fat_g=analysis.fat_g,
            items=[item.model_dump() for item in analysis.items],
            image_url=key,
            ai_provider=self.analyzer.provider_name,
        )
        self.meals.add(meal)
        # Registrar refeição alimenta o streak do dia.
        self.streaks.register_activity(user_id)

        self.db.commit()
        self.db.refresh(meal)
        return meal

    def list(self, user_id: int, *, limit: int = 50, offset: int = 0) -> list[MealLog]:
        return self.meals.list_for_user(user_id, limit=limit, offset=offset)

    def get_owned(self, user_id: int, meal_id: int) -> MealLog:
        meal = self.meals.get(meal_id)
        # Checagem de posse: um usuário NUNCA acessa refeição de outro.
        if meal is None or meal.user_id != user_id:
            raise NotFoundError("Refeição não encontrada.")
        return meal

    def load_image(self, user_id: int, meal_id: int) -> tuple[bytes, str]:
        if self.storage is None:
            raise ServiceUnavailableError("Storage indisponível.")
        meal = self.get_owned(user_id, meal_id)
        if not meal.image_url:
            raise NotFoundError("Esta refeição não possui imagem.")
        try:
            data = self.storage.load(meal.image_url)
        except StorageError as exc:
            raise NotFoundError("Imagem não encontrada.") from exc
        ext = meal.image_url.rsplit(".", 1)[-1].lower()
        return data, _TYPE_BY_EXT.get(ext, "application/octet-stream")
