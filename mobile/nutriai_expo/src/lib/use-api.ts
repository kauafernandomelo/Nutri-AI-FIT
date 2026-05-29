import { useFocusEffect } from 'expo-router';
import { useCallback, useState } from 'react';

/// Hook de leitura de API: carrega ao focar a tela e expõe loading/erro/refresh.
/// Recarregar ao focar faz a Home/Refeições refletirem mudanças feitas em outras
/// telas (ex.: registrar uma refeição) sem precisar de estado global.
export function useApi<T>(fn: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async (isRefresh: boolean) => {
    if (isRefresh) setRefreshing(true);
    else setLoading(true);
    setError(null);
    try {
      setData(await fn());
    } catch (e) {
      setError(e);
    } finally {
      if (isRefresh) setRefreshing(false);
      else setLoading(false);
    }
    // fn é estável no nosso uso (sem parâmetros que mudam).
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useFocusEffect(
    useCallback(() => {
      load(false);
    }, [load]),
  );

  return {
    data,
    loading,
    error,
    refreshing,
    refresh: () => load(true),
  };
}
