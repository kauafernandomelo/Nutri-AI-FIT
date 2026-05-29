import { Stack } from 'expo-router';
import * as SplashScreen from 'expo-splash-screen';
import { useEffect } from 'react';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

import { SessionProvider, useSession } from '@/lib/session';

// Mantém a splash até sabermos se há sessão (evita "piscar" telas).
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SessionProvider>
        <RootNavigator />
      </SessionProvider>
    </GestureHandlerRootView>
  );
}

/**
 * Navegação guiada pelo estado da sessão usando `Stack.Protected`:
 * só o grupo cujo `guard` é verdadeiro fica acessível, e o router redireciona
 * automaticamente para a rota âncora desse grupo quando o estado muda.
 */
function RootNavigator() {
  const { isLoading, status, needsOnboarding } = useSession();

  useEffect(() => {
    if (!isLoading) {
      SplashScreen.hideAsync();
    }
  }, [isLoading]);

  if (isLoading) {
    return null; // splash continua visível
  }

  const authed = status === 'authenticated';

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Protected guard={!authed}>
        <Stack.Screen name="sign-in" />
        <Stack.Screen name="register" options={{ headerShown: true, title: 'Criar conta' }} />
      </Stack.Protected>

      <Stack.Protected guard={authed && needsOnboarding}>
        <Stack.Screen name="onboarding" options={{ headerShown: true, title: 'Seu plano' }} />
      </Stack.Protected>

      <Stack.Protected guard={authed && !needsOnboarding}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen
          name="add-meal"
          options={{
            headerShown: true,
            presentation: 'modal',
            title: 'Nova refeição',
          }}
        />
      </Stack.Protected>
    </Stack>
  );
}
