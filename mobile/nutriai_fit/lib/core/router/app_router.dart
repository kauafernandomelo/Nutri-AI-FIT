import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/presentation/auth_controller.dart';
import '../../features/auth/presentation/login_screen.dart';
import '../../features/auth/presentation/register_screen.dart';
import '../../features/meals/presentation/add_meal_screen.dart';
import '../../features/onboarding/presentation/onboarding_screen.dart';
import '../../shared/widgets/app_shell.dart';
import '../../shared/widgets/splash_screen.dart';

/// Roteamento declarativo guiado pelo AuthState.
///
/// COMO o guard funciona: uma ponte Riverpod→Listenable (`ValueNotifier`) alimenta
/// o `refreshListenable` do go_router. Sempre que o AuthController emite um novo
/// estado, o router reavalia o `redirect` e leva o usuário à tela certa —
/// sem `Navigator.push` espalhado pelas telas.
final routerProvider = Provider<GoRouter>((ref) {
  final authNotifier = ValueNotifier<AuthState>(
    const AuthState(status: AuthStatus.unknown),
  );
  ref.listen<AuthState>(
    authControllerProvider,
    (_, next) => authNotifier.value = next,
    fireImmediately: true,
  );
  ref.onDispose(authNotifier.dispose);

  return GoRouter(
    initialLocation: '/',
    refreshListenable: authNotifier,
    redirect: (context, state) {
      final auth = authNotifier.value;
      final loc = state.matchedLocation;
      final atAuthScreen = loc == '/login' || loc == '/register';

      switch (auth.status) {
        case AuthStatus.unknown:
          // Ainda verificando o token salvo → mostra a splash.
          return loc == '/splash' ? null : '/splash';
        case AuthStatus.unauthenticated:
          return atAuthScreen ? null : '/login';
        case AuthStatus.authenticated:
          // Logado mas sem perfil/meta → completa o onboarding.
          if (auth.needsOnboarding) {
            return loc == '/onboarding' ? null : '/onboarding';
          }
          // Já dentro do app: sai de telas de "antessala".
          if (atAuthScreen || loc == '/splash' || loc == '/onboarding') {
            return '/';
          }
          return null;
      }
    },
    routes: [
      GoRoute(path: '/splash', builder: (_, __) => const SplashScreen()),
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/register', builder: (_, __) => const RegisterScreen()),
      GoRoute(path: '/onboarding', builder: (_, __) => const OnboardingScreen()),
      GoRoute(path: '/', builder: (_, __) => const AppShell()),
      GoRoute(path: '/add-meal', builder: (_, __) => const AddMealScreen()),
    ],
  );
});
