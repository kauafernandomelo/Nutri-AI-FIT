# Permite que o CELULAR alcance o PC durante o desenvolvimento.
# RODE COMO ADMINISTRADOR, uma única vez (ou quando trocar de rede).
#   PowerShell (Admin):
#   powershell -ExecutionPolicy Bypass -File mobile\nutriai_expo\scripts\allow-firewall.ps1
#
# Faz duas coisas, ambas necessárias e reversíveis:
#   1) Marca a sua rede como "Privada" — em "Pública" o Windows bloqueia conexões
#      de entrada (era o seu caso). Mexe SÓ na interface com gateway (a LAN real),
#      nunca nos adaptadores virtuais do Hyper-V/WSL.
#   2) Libera TCP 8000 (API) e 8081 (Metro) APENAS para a sub-rede local — não
#      expõe nada para a internet (defesa em profundidade).
$ErrorActionPreference = "Stop"

$cfg = Get-NetIPConfiguration |
  Where-Object { $_.IPv4DefaultGateway -ne $null -and $_.NetAdapter.Status -eq 'Up' } |
  Sort-Object { $_.NetAdapter.InterfaceMetric } | Select-Object -First 1
if ($cfg) {
  Set-NetConnectionProfile -InterfaceAlias $cfg.InterfaceAlias -NetworkCategory Private
  Write-Host "Rede '$($cfg.InterfaceAlias)' marcada como Privada." -ForegroundColor Green
}

$name = "NutriAI dev (Expo+API)"
Get-NetFirewallRule -DisplayName $name -ErrorAction SilentlyContinue | Remove-NetFirewallRule
New-NetFirewallRule -DisplayName $name -Direction Inbound -Protocol TCP `
  -LocalPort 8000, 8081 -RemoteAddress LocalSubnet -Profile Private -Action Allow | Out-Null
Write-Host "Firewall: TCP 8000 e 8081 liberados para a sub-rede local (perfil Privado)." -ForegroundColor Green
