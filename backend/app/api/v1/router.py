"""Agrega todos os routers da v1 sob um único APIRouter."""
from fastapi import APIRouter

from app.api.v1 import auth, dashboard, goals, meals, users, weights

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(goals.router)
api_router.include_router(meals.router)
api_router.include_router(weights.router)
api_router.include_router(dashboard.router)
