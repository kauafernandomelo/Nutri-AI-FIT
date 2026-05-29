/// Paleta e medidas do app (tema claro, acento verde — clima fitness/saúde).
export const colors = {
  primary: '#1DB954',
  primaryDark: '#179443',
  primaryContainer: '#E6F8EC',
  onPrimaryContainer: '#0B3D1E',
  bg: '#FFFFFF',
  surface: '#F5F6F8',
  surfaceAlt: '#ECEEF1',
  text: '#1A1C1E',
  textMuted: '#6B7280',
  border: '#E2E5EA',
  danger: '#E53935',
  white: '#FFFFFF',
  // Macros
  protein: '#E5484D',
  carbs: '#F5A623',
  fat: '#3B82F6',
} as const;

export const radius = { sm: 8, md: 14, lg: 18, pill: 999 } as const;

/// Espaçamento em múltiplos de 4 (sp(2) = 8).
export const sp = (n: number): number => n * 4;
