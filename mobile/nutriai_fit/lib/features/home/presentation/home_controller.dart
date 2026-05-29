import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../shared/models/dashboard_model.dart';
import '../data/dashboard_repository.dart';

/// Carrega o dashboard (tela Home). AsyncNotifier expõe loading/erro/dados.
class HomeController extends AsyncNotifier<DashboardModel> {
  @override
  Future<DashboardModel> build() {
    return ref.read(dashboardRepositoryProvider).getDashboard();
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(
      () => ref.read(dashboardRepositoryProvider).getDashboard(),
    );
  }
}

final homeControllerProvider =
    AsyncNotifierProvider<HomeController, DashboardModel>(HomeController.new);
