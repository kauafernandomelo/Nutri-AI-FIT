"""
Contrato de armazenamento de arquivos.

Trabalhamos com KEYS (caminhos lógicos), não com URLs públicas. As imagens são
sempre servidas por um endpoint autenticado que confere a posse — então, mesmo no
R2, o objeto é PRIVADO. Isso atende ao requisito de confidencialidade.
"""
from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    backend_name: str = "abstract"

    @abstractmethod
    def save(self, content: bytes, key: str, content_type: str) -> str:
        """Salva o conteúdo sob `key` e devolve a própria `key`."""
        raise NotImplementedError

    @abstractmethod
    def load(self, key: str) -> bytes:
        """Lê e devolve os bytes salvos em `key`."""
        raise NotImplementedError


class StorageError(Exception):
    """Erro de leitura/gravação no storage."""
