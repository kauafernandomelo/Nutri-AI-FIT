import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/dio_client.dart';
import '../../../shared/models/goal_model.dart';
import '../../../shared/models/user_model.dart';
import '../../../shared/models/weight_model.dart';

/// Agrega as chamadas relacionadas a perfil/onboarding:
/// usuário (GET/PATCH /users/me), metas (/goals) e pesos (/weights).
class ProfileRepository {
  final Dio _dio;

  ProfileRepository(this._dio);

  Future<UserModel> getMe() async {
    final resp = await _dio.get('/users/me');
    return UserModel.fromJson(resp.data as Map<String, dynamic>);
  }

  Future<UserModel> updateProfile({
    String? name,
    String? sex,
    int? age,
    double? heightCm,
  }) async {
    final body = <String, dynamic>{};
    if (name != null) body['name'] = name;
    if (sex != null) body['sex'] = sex;
    if (age != null) body['age'] = age;
    if (heightCm != null) body['height_cm'] = heightCm;
    final resp = await _dio.patch('/users/me', data: body);
    return UserModel.fromJson(resp.data as Map<String, dynamic>);
  }

  Future<GoalModel> createGoal({
    required String objective,
    required double startWeightKg,
    required double targetWeightKg,
    String activityLevel = 'moderate',
  }) async {
    final resp = await _dio.post('/goals', data: {
      'objective': objective,
      'start_weight_kg': startWeightKg,
      'target_weight_kg': targetWeightKg,
      'activity_level': activityLevel,
    });
    return GoalModel.fromJson(resp.data as Map<String, dynamic>);
  }

  Future<List<GoalModel>> listGoals() async {
    final resp = await _dio.get('/goals');
    return (resp.data as List)
        .map((e) => GoalModel.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<WeightModel> createWeight({
    required double weightKg,
    DateTime? recordedAt,
  }) async {
    final resp = await _dio.post('/weights', data: {
      'weight_kg': weightKg,
      if (recordedAt != null)
        'recorded_at': recordedAt.toIso8601String().split('T').first,
    });
    return WeightModel.fromJson(resp.data as Map<String, dynamic>);
  }

  Future<List<WeightModel>> listWeights() async {
    final resp = await _dio.get('/weights');
    return (resp.data as List)
        .map((e) => WeightModel.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}

final profileRepositoryProvider = Provider<ProfileRepository>(
  (ref) => ProfileRepository(ref.read(dioProvider)),
);
