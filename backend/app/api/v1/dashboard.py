"""Rota do dashboard: resumo diário para a tela Home."""
from fastapi import APIRouter

from app.api.deps import CurrentUser, DbDep
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(current_user: CurrentUser, db: DbDep) -> DashboardResponse:
    return DashboardService(db).get(current_user)
