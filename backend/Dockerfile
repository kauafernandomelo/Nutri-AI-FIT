# Dockerfile do backend — pronto para uso FUTURO (não é necessário para testar
# localmente, já que rodamos nativo com o Postgres 18 instalado).
FROM python:3.13-slim

# Boas práticas: não gerar .pyc e log sem buffer.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# psycopg2-binary já traz o necessário; libpq fica embutido. Instala deps primeiro
# (camada cacheável) e depois o código.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Em container, aplica migrações e sobe a API.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
