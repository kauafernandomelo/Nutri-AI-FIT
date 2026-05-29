import axios from 'axios';

/// Extrai uma mensagem amigável de um erro da API.
/// O backend devolve `{ "detail": "..." }` nos erros de domínio.
export function apiError(
  e: unknown,
  fallback = 'Algo deu errado. Tente novamente.',
): string {
  if (axios.isAxiosError(e)) {
    const detail = (e.response?.data as { detail?: unknown } | undefined)?.detail;
    if (typeof detail === 'string') return detail;
    if (e.code === 'ECONNABORTED' || e.message === 'Network Error') {
      return 'Sem conexão com o servidor. A API está rodando e o celular está na mesma rede?';
    }
  }
  return fallback;
}

/// Calorias como inteiro: "532".
export const fmtKcal = (v: number): string => Math.round(v).toString();

/// Gramas com no máximo 1 casa, vírgula decimal: "12" ou "12,5".
export const fmtG = (v: number): string =>
  (Number.isInteger(v) ? v.toString() : v.toFixed(1)).replace('.', ',');

/// Peso com 1 casa e sufixo: "72,5 kg".
export const fmtKg = (v: number): string =>
  `${v.toFixed(1).replace('.', ',')} kg`;

/// Data curta dd/MM a partir de um ISO string.
export const fmtDayMonth = (iso: string): string => {
  const d = new Date(iso);
  return `${String(d.getDate()).padStart(2, '0')}/${String(
    d.getMonth() + 1,
  ).padStart(2, '0')}`;
};

/// Hora HH:mm a partir de um ISO string.
export const fmtTime = (iso: string): string => {
  const d = new Date(iso);
  return `${String(d.getHours()).padStart(2, '0')}:${String(
    d.getMinutes(),
  ).padStart(2, '0')}`;
};
