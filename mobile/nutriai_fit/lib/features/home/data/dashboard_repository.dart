import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/dio_client.dart';
import '../../../shared/models/dashboard_model.dart';

class DashboardRepository {
  final Dio _dio;

  DashboardRepository(this._dio);

  Future<DashboardModel> getDashboard() async {
    final resp = await _dio.get('/dashboard');
    return DashboardModel.fromJson(resp.data as Map<String, dynamic>);
  }
}

final dashboardRepositoryProvider = Provider<DashboardRepository>(
  (ref) => DashboardRepository(ref.read(dioProvider)),
);
