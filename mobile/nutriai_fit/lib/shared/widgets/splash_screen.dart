import 'package:flutter/material.dart';

/// Tela exibida enquanto o AuthController verifica se há um token salvo
/// (estado `unknown`). Assim que ele decide, o redirect do router troca de tela.
class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.eco, size: 72, color: scheme.primary),
            const SizedBox(height: 24),
            const CircularProgressIndicator(),
          ],
        ),
      ),
    );
  }
}
