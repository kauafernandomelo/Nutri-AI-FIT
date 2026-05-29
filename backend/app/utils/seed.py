"""
Popula o catálogo de mensagens motivacionais.

Rode uma vez (após as migrações):  python -m app.utils.seed
É idempotente: se já houver mensagens, não duplica.
"""
from app.database.session import SessionLocal
from app.models import MessageCategory, MotivationalMessage

# (categoria, texto, min_streak)
MESSAGES: list[tuple[MessageCategory, str, int | None]] = [
    # Genéricas — sempre elegíveis.
    (MessageCategory.generic, "Continue registrando suas refeições.", None),
    (MessageCategory.generic, "Cada registro te aproxima da sua meta.", None),
    (MessageCategory.generic, "Pequenos passos consistentes geram grandes resultados.", None),
    # Streak — só aparecem quando o streak atinge o limite.
    (MessageCategory.streak, "Você começou! O primeiro dia é o mais importante.", 1),
    (MessageCategory.streak, "3 dias seguidos! Você está pegando o ritmo.", 3),
    (MessageCategory.streak, "7 dias de sequência! Excelente consistência esta semana.", 7),
    (MessageCategory.streak, "Duas semanas firmes! Isso é disciplina de verdade.", 14),
    (MessageCategory.streak, "30 dias! Você transformou o registro em hábito.", 30),
    # Consistência.
    (MessageCategory.consistency, "Excelente consistência esta semana.", None),
    (MessageCategory.consistency, "Sua dedicação está aparecendo nos números.", None),
    # Progresso em direção à meta.
    (MessageCategory.goal_progress, "Você está mais próximo da sua meta.", None),
    (MessageCategory.goal_progress, "Seu esforço está valendo a pena. Siga firme!", None),
]


def seed_messages() -> None:
    db = SessionLocal()
    try:
        existing = db.query(MotivationalMessage).count()
        if existing:
            print(f"[seed] Já existem {existing} mensagens. Nada a fazer.")
            return
        db.add_all(
            MotivationalMessage(category=cat, text=text, min_streak=ms, is_active=True)
            for cat, text, ms in MESSAGES
        )
        db.commit()
        print(f"[seed] {len(MESSAGES)} mensagens motivacionais inseridas.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_messages()
