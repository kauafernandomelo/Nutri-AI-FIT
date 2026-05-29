// Smoke test do app: sem token salvo, o usuário deve cair na tela de login.
//
// Trocamos o TokenStorage real (que usa o Keystore via canal de plataforma,
// indisponível em teste) por um falso em memória.
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:nutriai_fit/core/storage/token_storage.dart';
import 'package:nutriai_fit/main.dart';

class _FakeTokenStorage extends TokenStorage {
  String? _token;

  @override
  Future<String?> readToken() async => _token;

  @override
  Future<void> saveToken(String token) async => _token = token;

  @override
  Future<void> clear() async => _token = null;
}

void main() {
  testWidgets('Sem token salvo, o app cai na tela de login', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          tokenStorageProvider.overrideWithValue(_FakeTokenStorage()),
        ],
        child: const NutriAIApp(),
      ),
    );

    // Deixa o AuthController verificar o token e o router redirecionar.
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 50));

    expect(find.text('Entrar'), findsOneWidget);
  });
}
