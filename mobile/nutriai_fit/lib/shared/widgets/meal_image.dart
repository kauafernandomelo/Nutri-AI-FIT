import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/config/app_config.dart';
import '../../core/storage/token_storage.dart';

/// Exibe a foto de uma refeição.
///
/// DOIS cuidados importantes (confidencialidade + portabilidade):
/// 1) A imagem é servida por um endpoint AUTENTICADO — só o dono acessa
///    (GET /meals/{id}/image). Por isso anexamos o token JWT no header.
/// 2) Montamos a URL a partir do AppConfig (mesma base das outras chamadas) em
///    vez de usar o host que o backend devolve em `image_url`. Assim funciona no
///    emulador (10.0.2.2) sem depender da config PUBLIC_BASE_URL do servidor.
class MealImage extends ConsumerWidget {
  final int mealId;
  final double? width;
  final double? height;
  final BoxFit fit;
  final BorderRadius? borderRadius;

  const MealImage({
    super.key,
    required this.mealId,
    this.width,
    this.height,
    this.fit = BoxFit.cover,
    this.borderRadius,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final url = '${AppConfig.apiV1}/meals/$mealId/image';
    final tokenStorage = ref.read(tokenStorageProvider);

    final image = FutureBuilder<String?>(
      future: tokenStorage.readToken(),
      builder: (context, snapshot) {
        final token = snapshot.data;
        if (token == null || token.isEmpty) {
          return _placeholder(context, loading: !snapshot.hasData);
        }
        return Image.network(
          url,
          width: width,
          height: height,
          fit: fit,
          headers: {'Authorization': 'Bearer $token'},
          errorBuilder: (_, __, ___) => _placeholder(context),
          loadingBuilder: (context, child, progress) =>
              progress == null ? child : _placeholder(context, loading: true),
        );
      },
    );

    if (borderRadius != null) {
      return ClipRRect(borderRadius: borderRadius!, child: image);
    }
    return image;
  }

  Widget _placeholder(BuildContext context, {bool loading = false}) {
    final scheme = Theme.of(context).colorScheme;
    return Container(
      width: width,
      height: height,
      color: scheme.surfaceContainerHighest,
      alignment: Alignment.center,
      child: loading
          ? const SizedBox(
              width: 22,
              height: 22,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : Icon(Icons.restaurant, color: scheme.outline),
    );
  }
}
