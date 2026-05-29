import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../shared/models/meal_model.dart';
import '../data/meal_repository.dart';

/// Lista as refeições do usuário. AsyncNotifier expõe loading/erro/dados de forma
/// idiomática para a UI (AsyncValue.when).
class MealsController extends AsyncNotifier<List<MealModel>> {
  @override
  Future<List<MealModel>> build() {
    return ref.read(mealRepositoryProvider).listMeals();
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(
      () => ref.read(mealRepositoryProvider).listMeals(),
    );
  }
}

final mealsControllerProvider =
    AsyncNotifierProvider<MealsController, List<MealModel>>(MealsController.new);
