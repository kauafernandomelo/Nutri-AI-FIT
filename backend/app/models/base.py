"""
Base declarativa do SQLAlchemy 2.0 + mixin de timestamps.

POR QUE um TimestampMixin:
- `created_at` e `updated_at` são úteis em quase toda tabela (auditoria, ordenação).
- Colocá-los em um mixin evita repetição (DRY) e padroniza o comportamento:
  o banco preenche os valores (server_default/onupdate), não a aplicação.
"""
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Classe base de todos os modelos ORM."""


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
