import Constants from 'expo-constants';

/// Descobre a URL base da API. Ordem de resolução:
///
/// 1. EXPO_PUBLIC_API_BASE — override explícito. O script `scripts/start-lan.ps1`
///    define isso com o IP da LAN para teste em celular; também serve para apontar
///    para produção. Variáveis `EXPO_PUBLIC_*` são embutidas no bundle pelo Expo.
/// 2. hostUri do Expo — com o Expo Go o app roda NO CELULAR, então `localhost`
///    apontaria para o próprio celular, não para o PC. Reaproveitamos o IP do dev
///    server (ex.: "192.168.1.4:8081") e trocamos a porta para a 8000 (a da API).
///    Cuidado no Windows: com Hyper-V/WSL o Expo pode anunciar um IP virtual
///    (ex.: 172.27.x) inalcançável pelo celular — daí o override do passo 1.
/// 3. localhost — rodando no PC (web) ou sem host detectável.
function resolveApiBase(): string {
  const explicit = process.env.EXPO_PUBLIC_API_BASE;
  if (explicit) return explicit.replace(/\/+$/, '');

  const hostUri =
    Constants.expoConfig?.hostUri ??
    // Fallbacks para campos legados em algumas versões do Expo.
    (Constants as unknown as { expoGoConfig?: { debuggerHost?: string } })
      .expoGoConfig?.debuggerHost;

  const host = hostUri?.split(':')[0];
  if (host && host !== 'localhost' && host !== '127.0.0.1') {
    return `http://${host}:8000`;
  }
  // Rodando no PC (web) ou sem host detectável.
  return 'http://localhost:8000';
}

export const API_BASE = resolveApiBase();
export const API_V1 = `${API_BASE}/api/v1`;
