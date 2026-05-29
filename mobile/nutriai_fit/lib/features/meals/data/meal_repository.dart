import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/dio_client.dart';
import '../../../shared/models/meal_model.dart';

class MealRepository {
  final Dio _dio;

  MealRepository(this._dio);

  /// Envia a foto (multipart) para análise da IA e salva a refeição.
  Future<MealModel> createMeal(String imagePath) async {
    final ext = imagePath.split('.').last.toLowerCase();
    final subtype = switch (ext) {
      'png' => 'png',
      'webp' => 'webp',
      _ => 'jpeg',
    };
    final form = FormData.fromMap({
      'file': await MultipartFile.fromFile(
        imagePath,
        filename: 'meal.$ext',
        contentType: DioMediaType('image', subtype),
      ),
    });
    final resp = await _dio.post('/meals', data: form);
    return MealModel.fromJson(resp.data as Map<String, dynamic>);
  }

  Future<List<MealModel>> listMeals({int limit = 50, int offset = 0}) async {
    final resp = await _dio.get(
      '/meals',
      queryParameters: {'limit': limit, 'offset': offset},
    );
    return (resp.data as List)
        .map((e) => MealModel.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}

final mealRepositoryProvider = Provider<MealRepository>(
  (ref) => MealRepository(ref.read(dioProvider)),
);
