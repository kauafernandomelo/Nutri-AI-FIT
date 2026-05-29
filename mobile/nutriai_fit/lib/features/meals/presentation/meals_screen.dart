import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../shared/models/meal_model.dart';
import '../../../shared/ui_helpers.dart';
import '../../../shared/widgets/meal_image.dart';
import 'meals_controller.dart';

/// Histórico de refeições registradas.
class MealsScreen extends ConsumerWidget {
  const MealsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final meals = ref.watch(mealsControllerProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Refeições')),
      body: meals.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.cloud_off, size: 48),
                const SizedBox(height: 12),
                Text(apiError(e), textAlign: TextAlign.center),
                const SizedBox(height: 16),
                FilledButton.tonal(
                  onPressed: () =>
                      ref.read(mealsControllerProvider.notifier).refresh(),
                  child: const Text('Tentar de novo'),
                ),
              ],
            ),
          ),
        ),
        data: (list) {
          if (list.isEmpty) {
            return const _EmptyMeals();
          }
          return RefreshIndicator(
            onRefresh: () =>
                ref.read(mealsControllerProvider.notifier).refresh(),
            child: ListView.separated(
              padding: const EdgeInsets.all(16),
              itemCount: list.length,
              separatorBuilder: (_, __) => const SizedBox(height: 12),
              itemBuilder: (_, i) => _MealCard(meal: list[i]),
            ),
          );
        },
      ),
    );
  }
}

class _MealCard extends StatelessWidget {
  final MealModel meal;
  const _MealCard({required this.meal});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      clipBehavior: Clip.antiAlias,
      child: Row(
        children: [
          if (meal.imageUrl != null)
            MealImage(mealId: meal.id, width: 88, height: 88)
          else
            Container(
              width: 88,
              height: 88,
              color: theme.colorScheme.surfaceContainerHighest,
              child: Icon(Icons.restaurant, color: theme.colorScheme.outline),
            ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(meal.name,
                      style: theme.textTheme.titleMedium
                          ?.copyWith(fontWeight: FontWeight.w600),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis),
                  const SizedBox(height: 4),
                  Text(
                    '${fmtKcal(meal.calories)} kcal  •  '
                    'P ${fmtG(meal.proteinG)}g  C ${fmtG(meal.carbsG)}g  G ${fmtG(meal.fatG)}g',
                    style: theme.textTheme.bodySmall,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${fmtDayMonth(meal.consumedAt)} às ${fmtTime(meal.consumedAt)}',
                    style: theme.textTheme.bodySmall
                        ?.copyWith(color: theme.colorScheme.outline),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _EmptyMeals extends StatelessWidget {
  const _EmptyMeals();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('🍽️', style: TextStyle(fontSize: 48)),
            const SizedBox(height: 12),
            Text('Nenhuma refeição ainda',
                style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 4),
            const Text(
              'Toque no botão da câmera para registrar sua primeira refeição.',
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
