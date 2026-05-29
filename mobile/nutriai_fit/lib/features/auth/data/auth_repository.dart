import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/dio_client.dart';
import '../../../core/storage/token_storage.dart';
import '../../../shared/models/user_model.dart';

/// Operações de autenticação contra a API.
class AuthRepository {
  final Dio _dio;
  final TokenStorage _tokenStorage;

  AuthRepository(this._dio, this._tokenStorage);

  Future<UserModel> register({
    required String name,
    required String email,
    required String password,
  }) async {
    final resp = await _dio.post(
      '/auth/register',
      data: {'name': name, 'email': email, 'password': password},
    );
    return UserModel.fromJson(resp.data as Map<String, dynamic>);
  }

  /// Login no formato OAuth2 (campo "username" leva o e-mail).
  Future<void> login({required String email, required String password}) async {
    final resp = await _dio.post(
      '/auth/login',
      data: {'username': email, 'password': password},
      options: Options(contentType: Headers.formUrlEncodedContentType),
    );
    final token = (resp.data as Map<String, dynamic>)['access_token'] as String;
    await _tokenStorage.saveToken(token);
  }

  Future<void> logout() => _tokenStorage.clear();

  Future<String?> currentToken() => _tokenStorage.readToken();
}

final authRepositoryProvider = Provider<AuthRepository>(
  (ref) => AuthRepository(ref.read(dioProvider), ref.read(tokenStorageProvider)),
);
