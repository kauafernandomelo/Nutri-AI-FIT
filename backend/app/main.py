"""
Ponto de entrada da API (FastAPI).

Monta, em ordem:
- CORS (quais origens podem chamar a API);
- Rate limiting (slowapi);
- Headers de segurança;
- Tradução de exceções de domínio → respostas HTTP;
- As rotas da v1 sob /api/v1.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import AppError
from app.core.rate_limit import limiter

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="API do NutriAI Fit — foto da refeição → estimativa nutricional + gamificação.",
)

# --- CORS ---------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False,  # usamos Bearer token, não cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rate limiting ------------------------------------------------------------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


# --- Headers de segurança -----------------------------------------------------
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        # HSTS só faz sentido sob HTTPS (produção).
        if settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


app.add_middleware(SecurityHeadersMiddleware)


# --- Tradução de exceções de domínio -----------------------------------------
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# --- Rotas --------------------------------------------------------------------
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "service": settings.PROJECT_NAME}


@app.get("/", tags=["health"])
def root() -> dict:
    return {"message": "NutriAI Fit API. Veja /docs para a documentação interativa."}
