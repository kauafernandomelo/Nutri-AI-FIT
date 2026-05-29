"""
Storage no Cloudflare R2 (API compatível com S3, via boto3).

Implementado, porém INATIVO por padrão (STORAGE_PROVIDER=local). Para ligar:
  1) preencha R2_* no .env
  2) mude STORAGE_PROVIDER=r2

Os objetos são PRIVADOS (sem ACL pública). O app só os acessa pelo endpoint
autenticado, que lê os bytes via load() — nada de URL pública permanente.
boto3 é importado de forma preguiçosa.
"""
from app.core.config import settings
from app.integrations.storage.base import AbstractStorage, StorageError


class R2Storage(AbstractStorage):
    backend_name = "r2"

    def __init__(self) -> None:
        missing = [
            k
            for k in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET")
            if not getattr(settings, k)
        ]
        if missing:
            raise StorageError(f"Configuração R2 incompleta: {', '.join(missing)}")

        try:
            import boto3
        except ImportError as exc:  # pragma: no cover
            raise StorageError("Pacote 'boto3' não instalado.") from exc

        self._bucket = settings.R2_BUCKET
        self._client = boto3.client(
            "s3",
            endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name="auto",
        )

    def save(self, content: bytes, key: str, content_type: str) -> str:
        try:
            self._client.put_object(
                Bucket=self._bucket, Key=key, Body=content, ContentType=content_type
            )
            return key
        except Exception as exc:  # noqa: BLE001
            raise StorageError(f"Falha ao enviar para o R2: {exc}") from exc

    def load(self, key: str) -> bytes:
        try:
            obj = self._client.get_object(Bucket=self._bucket, Key=key)
            return obj["Body"].read()
        except Exception as exc:  # noqa: BLE001
            raise StorageError(f"Falha ao ler do R2: {exc}") from exc
