import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

/// Helpers de UI compartilhados: tradução de erros da API e formatação de números.
///
/// Centralizar isto evita repetir o mesmo `try/catch` e os mesmos
/// `toStringAsFixed` espalhados pelas telas (DRY).

/// Extrai uma mensagem amigável de um erro vindo da API (Dio).
///
/// O backend devolve `{"detail": "..."}` nos erros de domínio (ver
/// app/core/exceptions.py). Aproveitamos isso; se não houver detail, caímos
/// num texto genérico — nunca vazamos stack trace para o usuário.
String apiError(Object e, [String fallback = 'Algo deu errado. Tente novamente.']) {
  if (e is DioException) {
    final data = e.response?.data;
    if (data is Map && data['detail'] is String) {
      return data['detail'] as String;
    }
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.connectionError:
        return 'Sem conexão com o servidor. A API está rodando?';
      default:
        break;
    }
  }
  return fallback;
}

/// Mostra um SnackBar de erro padronizado.
void showError(BuildContext context, Object e) {
  final messenger = ScaffoldMessenger.of(context);
  messenger
    ..hideCurrentSnackBar()
    ..showSnackBar(SnackBar(content: Text(apiError(e))));
}

/// Calorias sempre como inteiro ("532 kcal").
String fmtKcal(num v) => v.round().toString();

/// Gramas com no máximo uma casa, sem ".0" desnecessário ("12" ou "12,5").
String fmtG(num v) =>
    (v % 1 == 0 ? v.toStringAsFixed(0) : v.toStringAsFixed(1)).replaceAll('.', ',');

/// Peso com uma casa decimal e sufixo ("72,5 kg").
String fmtKg(num v) => '${v.toStringAsFixed(1).replaceAll('.', ',')} kg';

/// Data curta dd/MM (sem depender de locale do intl).
String fmtDayMonth(DateTime d) =>
    '${d.day.toString().padLeft(2, '0')}/${d.month.toString().padLeft(2, '0')}';

/// Hora HH:mm.
String fmtTime(DateTime d) =>
    '${d.hour.toString().padLeft(2, '0')}:${d.minute.toString().padLeft(2, '0')}';
