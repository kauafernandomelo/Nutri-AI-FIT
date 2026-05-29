"""
Rotas de refeição:
- POST /meals          → envia a foto (multipart), roda IA, salva e atualiza streak
- GET  /meals          → lista as refeições do usuário
- GET  /meals/{id}/image → serve a imagem APENAS para o dono (autenticado)
"""
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Request, Response, UploadFile, status

from app.api.deps import AnalyzerDep, CurrentUser, DbDep, StorageDep
from app.core.config import settings
from app.core.rate_limit import limiter
from app.schemas.meal import MealRead
from app.services.meal_service import MealService, to_meal_read

router = APIRouter(prefix="/meals", tags=["meals"])

_ALLOWED_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}


@router.post("", response_model=MealRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")  # análise de imagem é cara — limitamos por IP
async def create_meal(
    request: Request,
    current_user: CurrentUser,
    db: DbDep,
    analyzer: AnalyzerDep,
    storage: StorageDep,
    file: Annotated[UploadFile, File(description="Foto da refeição")],
) -> MealRead:
    # Validação de entrada (tipo + tamanho) ANTES de processar.
    if file.content_type not in _ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Envie uma imagem JPEG, PNG ou WEBP.",
        )
    content = await file.read()
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Imagem maior que {settings.MAX_UPLOAD_MB} MB.",
        )

    service = MealService(db, analyzer=analyzer, storage=storage)
    meal = await service.create_from_image(current_user.id, content, file.content_type)
    return to_meal_read(meal)


@router.get("", response_model=list[MealRead])
def list_meals(
    current_user: CurrentUser,
    db: DbDep,
    limit: int = 50,
    offset: int = 0,
) -> list[MealRead]:
    service = MealService(db)  # listagem não precisa de IA/storage
    meals = service.list(current_user.id, limit=min(limit, 100), offset=max(offset, 0))
    return [to_meal_read(m) for m in meals]


@router.get("/{meal_id}/image")
def meal_image(
    meal_id: int,
    current_user: CurrentUser,
    db: DbDep,
    storage: StorageDep,
) -> Response:
    service = MealService(db, storage=storage)
    data, content_type = service.load_image(current_user.id, meal_id)
    # Cache privado: o navegador/app pode guardar, mas não caches compartilhados.
    return Response(
        content=data,
        media_type=content_type,
        headers={"Cache-Control": "private, max-age=3600"},
    )
