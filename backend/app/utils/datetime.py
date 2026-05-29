"""Helpers de data/hora centralizados (facilita testar e trocar de fuso depois)."""
from datetime import date, datetime, timezone


def utcnow() -> datetime:
    """Agora em UTC (timezone-aware)."""
    return datetime.now(timezone.utc)


def today() -> date:
    """
    Data de 'hoje' usada na lógica de streak.

    MVP: usamos a data local do servidor. Melhoria futura: receber o fuso do
    usuário para o streak respeitar a meia-noite local dele.
    """
    return date.today()
