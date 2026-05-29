# Sobe o backend em modo desenvolvimento, em UM comando:
#   1) garante a venv e as dependências
#   2) aplica as migrações (cria as tabelas no Postgres)
#   3) popula as mensagens motivacionais
#   4) inicia a API com auto-reload
#
# PRÉ-REQUISITO: rodar antes (uma única vez) o provisionamento do banco:
#   & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -f backend\scripts\provision_db.sql
#
# Uso:  powershell -ExecutionPolicy Bypass -File backend\scripts\run_dev.ps1
$ErrorActionPreference = "Stop"
$backend = Split-Path -Parent $PSScriptRoot
Set-Location $backend

if (-not (Test-Path ".\.venv")) {
    Write-Host "Criando venv..." -ForegroundColor Cyan
    py -m venv .venv
}

Write-Host "Instalando dependencias..." -ForegroundColor Cyan
& ".\.venv\Scripts\python.exe" -m pip install -q -r requirements.txt

Write-Host "Aplicando migracoes..." -ForegroundColor Cyan
& ".\.venv\Scripts\alembic.exe" upgrade head

Write-Host "Populando mensagens motivacionais..." -ForegroundColor Cyan
& ".\.venv\Scripts\python.exe" -m app.utils.seed

Write-Host "Iniciando API em http://localhost:8000/docs" -ForegroundColor Green
& ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
