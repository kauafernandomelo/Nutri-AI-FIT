# Sobe o Expo para testar no CELULAR FÍSICO (Expo Go), na MESMA rede Wi-Fi do PC.
#
# Por que este script existe: máquinas Windows com Hyper-V/WSL têm adaptadores
# virtuais (ex.: 172.27.x) que competem com a LAN real. O Expo às vezes anuncia o
# IP virtual e o celular nunca alcança o Metro/backend. Aqui detectamos o IP da
# interface que TEM gateway (a que está de fato na rede) e o fixamos, tanto para o
# Metro (REACT_NATIVE_PACKAGER_HOSTNAME) quanto para a API (EXPO_PUBLIC_API_BASE).
#
# Pré-requisitos (uma vez, como ADMIN): scripts\allow-firewall.ps1
# E o backend rodando (backend\scripts\run_dev.ps1 — já escuta em 0.0.0.0:8000).
#
# Uso:  powershell -ExecutionPolicy Bypass -File mobile\nutriai_expo\scripts\start-lan.ps1
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

$cfg = Get-NetIPConfiguration |
  Where-Object { $_.IPv4DefaultGateway -ne $null -and $_.NetAdapter.Status -eq 'Up' } |
  Sort-Object { $_.NetAdapter.InterfaceMetric } | Select-Object -First 1
if (-not $cfg) {
  throw "Nenhuma interface de rede com gateway. Conecte-se ao Wi-Fi/Ethernet primeiro."
}
$ip = $cfg.IPv4Address.IPAddress

Write-Host "IP da LAN: $ip ($($cfg.InterfaceAlias))" -ForegroundColor Green
Write-Host "Garanta que o CELULAR esta na MESMA rede Wi-Fi ($ip)." -ForegroundColor Cyan

$env:REACT_NATIVE_PACKAGER_HOSTNAME = $ip
$env:EXPO_PUBLIC_API_BASE = "http://${ip}:8000"

npx expo start --host lan
