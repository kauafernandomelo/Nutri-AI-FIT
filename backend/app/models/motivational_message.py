"""
Catálogo de mensagens motivacionais.

Em vez de chumbar frases no código, guardamos um catálogo no banco. O
`motivation_service` escolhe a frase certa conforme o contexto (streak,
consistência, progresso). `min_streak` é uma condição opcional de exibição.
"""
from sqlalchemy import Boolean, Enum as SAEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
from app.models.enums import MessageCategory


class MotivationalMessage(Base, TimestampMixin):
    __tablename__ = "motivational_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[MessageCategory] = mapped_column(
        SAEnum(MessageCategory, name="message_category_enum"), index=True, nullable=False
    )
    text: Mapped[str] = mapped_column(String(300), nullable=False)
    # Se preenchido, a mensagem só é elegível quando o streak atual >= min_streak.
    min_streak: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
