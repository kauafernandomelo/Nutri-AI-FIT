/// Configuração de ambiente do app.
///
/// IMPORTANTE (ponto que confunde muita gente):
/// - No EMULADOR Android, "localhost" do PC é acessível por 10.0.2.2.
/// - Em um CELULAR FÍSICO, use o IP da sua máquina na rede Wi-Fi e rode o
///   backend com --host 0.0.0.0. Passe via:
///     flutter run --dart-define=API_BASE_URL=http://192.168.0.10:8000
class AppConfig {
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );

  static const String apiPrefix = '/api/v1';

  static String get apiV1 => '$apiBaseUrl$apiPrefix';
}
