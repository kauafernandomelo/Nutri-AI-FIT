import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/dio_client.dart';
import '../../../shared/models/user_model.dart';
import '../../profile/data/profile_repository.dart';
import '../data/auth_repository.dart';

enum AuthStatus { unknown, unauthenticated, authenticated }

/// Estado de autenticação observado pelo roteador.
class AuthState {
  final AuthStatus status;
  final bool needsOnboarding;
  final UserModel? user;

  const AuthState({
    required this.status,
    this.needsOnboarding = false,
    this.user,
  });
}

/// Controla login/cadastro/logout e decide se o onboarding é necessário.
class AuthController extends Notifier<AuthState> {
  AuthRepository get _auth => ref.read(authRepositoryProvider);
  ProfileRepository get _profile => ref.read(profileRepositoryProvider);

  @override
  AuthState build() {
    // Se o Dio receber 401 (token expirado), volta para a tela de login.
    setUnauthorizedHandler(() {
      state = const AuthState(status: AuthStatus.unauthenticated);
    });
    _bootstrap();
    return const AuthState(status: AuthStatus.unknown);
  }

  Future<void> _bootstrap() async {
    final token = await _auth.currentToken();
    if (token == null || token.isEmpty) {
      state = const AuthState(status: AuthStatus.unauthenticated);
      return;
    }
    await _loadUserState();
  }

  /// Busca o usuário + metas para decidir se o onboarding está completo.
  Future<void> _loadUserState() async {
    try {
      final user = await _profile.getMe();
      final goals = await _profile.listGoals();
      final needsOnboarding = !user.hasProfile || goals.isEmpty;
      state = AuthState(
        status: AuthStatus.authenticated,
        needsOnboarding: needsOnboarding,
        user: user,
      );
    } on DioException {
      await _auth.logout();
      state = const AuthState(status: AuthStatus.unauthenticated);
    }
  }

  Future<void> login(String email, String password) async {
    await _auth.login(email: email, password: password);
    await _loadUserState();
  }

  Future<void> register(String name, String email, String password) async {
    await _auth.register(name: name, email: email, password: password);
    await _auth.login(email: email, password: password);
    await _loadUserState();
  }

  /// Chamado ao concluir o onboarding (re-busca o estado do usuário).
  Future<void> refreshUser() => _loadUserState();

  Future<void> logout() async {
    await _auth.logout();
    state = const AuthState(status: AuthStatus.unauthenticated);
  }
}

final authControllerProvider =
    NotifierProvider<AuthController, AuthState>(AuthController.new);
