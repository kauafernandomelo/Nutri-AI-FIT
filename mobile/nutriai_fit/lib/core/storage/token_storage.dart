import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Guarda o token JWT de forma SEGURA.
///
/// No Android usamos EncryptedSharedPreferences (respaldado pelo Keystore):
/// o token nunca fica em texto puro — atende ao requisito de confidencialidade.
class TokenStorage {
  static const _tokenKey = 'access_token';

  final FlutterSecureStorage _storage;

  TokenStorage([FlutterSecureStorage? storage])
      : _storage = storage ??
            const FlutterSecureStorage(
              aOptions: AndroidOptions(encryptedSharedPreferences: true),
            );

  Future<void> saveToken(String token) =>
      _storage.write(key: _tokenKey, value: token);

  Future<String?> readToken() => _storage.read(key: _tokenKey);

  Future<void> clear() => _storage.delete(key: _tokenKey);
}

final tokenStorageProvider = Provider<TokenStorage>((ref) => TokenStorage());
