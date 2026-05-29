"""Factory de storage: escolhe local vs R2 conforme STORAGE_PROVIDER no .env."""
from app.core.config import settings
from app.integrations.storage.base import AbstractStorage
from app.integrations.storage.local_storage import LocalStorage


def get_storage() -> AbstractStorage:
    provider = (settings.STORAGE_PROVIDER or "local").lower()
    if provider == "r2":
        from app.integrations.storage.r2_storage import R2Storage

        return R2Storage()
    return LocalStorage()
