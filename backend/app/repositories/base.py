"""
Repositório base genérico (Repository Pattern).

POR QUE:
- Centraliza o acesso a dados. Os serviços nunca escrevem SQL/queries cruas;
  eles pedem ao repositório. Isso isola o ORM e facilita testar/trocar.
- Usa `flush()` (não `commit()`): a TRANSAÇÃO pertence ao serviço, que decide
  quando confirmar tudo de uma vez (atomicidade em operações multi-passo).
"""
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: Session) -> None:
        self.model = model
        self.db = db

    def get(self, id_: int) -> ModelType | None:
        return self.db.get(self.model, id_)

    def add(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.flush()  # popula PKs/defaults sem confirmar a transação
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.flush()
