import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config/app_config.dart';
import '../storage/token_storage.dart';

/// Dio configurado com:
/// - baseUrl da API;
/// - interceptor que ANEXA o token JWT a cada requisição;
/// - tratamento de 401 (token expirado/inválido) → desloga.
///
/// O callback de 401 é injetado depois (setUnauthorizedHandler) para evitar
/// dependência circular entre o Dio e o controlador de autenticação.
final dioProvider = Provider<Dio>((ref) {
  final tokenStorage = ref.read(tokenStorageProvider);

  final dio = Dio(
    BaseOptions(
      baseUrl: AppConfig.apiV1,
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 30),
    ),
  );

  dio.interceptors.add(
    InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await tokenStorage.readToken();
        if (token != null && token.isNotEmpty) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          // Token inválido/expirado → limpa e avisa quem registrou o handler.
          await tokenStorage.clear();
          _onUnauthorized?.call();
        }
        handler.next(error);
      },
    ),
  );

  return dio;
});

// Callback global simples para reagir a 401 (definido pelo AuthController).
void Function()? _onUnauthorized;

void setUnauthorizedHandler(void Function() handler) {
  _onUnauthorized = handler;
}
