import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react';

import * as api from './api';
import type { User } from './api';

type Status = 'loading' | 'authenticated' | 'unauthenticated';

interface SessionValue {
  status: Status;
  isLoading: boolean;
  user: User | null;
  /** True quando falta completar perfil ou criar a primeira meta. */
  needsOnboarding: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (name: string, email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  /** Reavalia o estado do usuário (ex.: ao concluir o onboarding). */
  refresh: () => Promise<void>;
}

const SessionContext = createContext<SessionValue | undefined>(undefined);

export function useSession(): SessionValue {
  const ctx = useContext(SessionContext);
  if (!ctx) {
    throw new Error('useSession deve ser usado dentro de <SessionProvider>');
  }
  return ctx;
}

export function SessionProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<Status>('loading');
  const [user, setUser] = useState<User | null>(null);
  const [needsOnboarding, setNeedsOnboarding] = useState(false);

  // Busca usuário + metas para decidir se o onboarding está completo.
  async function loadUserState(): Promise<void> {
    try {
      const me = await api.getMe();
      const goals = await api.listGoals();
      const hasProfile =
        me.sex != null && me.age != null && me.height_cm != null;
      setUser(me);
      setNeedsOnboarding(!hasProfile || goals.length === 0);
      setStatus('authenticated');
    } catch {
      await api.clearToken();
      setUser(null);
      setStatus('unauthenticated');
    }
  }

  useEffect(() => {
    // Se o axios receber 401, volta para a tela de login.
    api.setUnauthorizedHandler(() => {
      setUser(null);
      setStatus('unauthenticated');
    });

    (async () => {
      const token = await api.loadToken();
      if (!token) {
        setStatus('unauthenticated');
        return;
      }
      await loadUserState();
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const value: SessionValue = {
    status,
    isLoading: status === 'loading',
    user,
    needsOnboarding,
    signIn: async (email, password) => {
      await api.login(email, password);
      await loadUserState();
    },
    signUp: async (name, email, password) => {
      await api.register(name, email, password);
      await api.login(email, password);
      await loadUserState();
    },
    signOut: async () => {
      await api.clearToken();
      setUser(null);
      setStatus('unauthenticated');
    },
    refresh: loadUserState,
  };

  return (
    <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
  );
}
