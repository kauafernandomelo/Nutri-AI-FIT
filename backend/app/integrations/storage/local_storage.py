"""
Storage em disco local (desenvolvimento).

Salva os arquivos em UPLOAD_DIR. O diretório está no .gitignore e NÃO é exposto
como estático público — o acesso passa sempre pelo endpoint autenticado de imagem.
"""
from pathlib import Path

from app.core.config import settings
from app.integrations.storage.base import AbstractStorage, StorageError


class LocalStorage(AbstractStorage):
    backend_name = "local"

    def __init__(self) -> None:
        self.base_path = Path(settings.UPLOAD_DIR).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, key: str) -> Path:
        # Resolve e garante que o caminho final continua DENTRO de base_path
        # (defesa contra path traversal, ex.: key = "../../etc/passwd").
        target = (self.base_path / key).resolve()
        if not str(target).startswith(str(self.base_path)):
            raise StorageError("Caminho de arquivo inválido.")
        return target

    def save(self, content: bytes, key: str, content_type: str) -> str:
        target = self._safe_path(key)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return key

    def load(self, key: str) -> bytes:
        target = self._safe_path(key)
        if not target.exists():
            raise StorageError(f"Arquivo não encontrado: {key}")
        return target.read_bytes()
