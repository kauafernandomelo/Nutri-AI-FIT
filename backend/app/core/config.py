"""
Configuração central da aplicação.

POR QUE assim:
- Usamos `pydantic-settings` para ler variáveis de ambiente (de um arquivo .env).
  Isso mantém SEGREDOS FORA DO CÓDIGO (princípio de confidencialidade) e permite
  trocar comportamento (banco, IA, storage) sem mexer em uma linha de código.
- Tudo é tipado e validado na inicialização: se faltar SECRET_KEY ou DATABASE_URL,
  o app falha rápido e com uma mensagem clara, em vez de quebrar no meio de um request.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Lê o .env que está ao lado da pasta do backend. `extra="ignore"` evita que
    # variáveis extras no ambiente derrubem a aplicação.
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- Identidade da API ---
    PROJECT_NAME: str = "NutriAI Fit"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # --- Banco de dados ---
    DATABASE_URL: str

    # --- Segurança / JWT ---
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias (pragmático para MVP)
    BCRYPT_ROUNDS: int = 12

    # --- CORS (string separada por vírgula; "*" libera tudo — restrinja em prod) ---
    CORS_ORIGINS: str = "*"

    # --- Seleção de integrações desacopladas ---
    AI_PROVIDER: str = "mock"        # mock | gemini
    STORAGE_PROVIDER: str = "local"  # local | r2

    # --- Storage local ---
    UPLOAD_DIR: str = "uploads"
    PUBLIC_BASE_URL: str = "http://localhost:8000"
    MAX_UPLOAD_MB: int = 10

    # --- Gemini Vision ---
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # --- Cloudflare R2 (compatível com S3) ---
    R2_ACCOUNT_ID: str | None = None
    R2_ACCESS_KEY_ID: str | None = None
    R2_SECRET_ACCESS_KEY: str | None = None
    R2_BUCKET: str | None = None
    R2_PUBLIC_URL: str | None = None

    @property
    def cors_origins_list(self) -> list[str]:
        """Converte a string de CORS em lista para o middleware."""
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def max_upload_bytes(self) -> int:
        return self.MAX_UPLOAD_MB * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    """Singleton em cache — evita reler o .env a cada chamada."""
    return Settings()


# Instância global de conveniência.
settings = get_settings()
