import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../shared/models/dashboard_model.dart';
import '../../../shared/models/goal_model.dart';
import '../../../shared/ui_helpers.dart';
import 'home_controller.dart';

/// Home: agrega o dia em um olhar — calorias x meta, macros, streak e peso.
class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dashboard = ref.watch(homeControllerProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Hoje')),
      body: dashboard.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => _ErrorView(
          message: apiError(e),
          onRetry: () => ref.read(homeControllerProvider.notifier).refresh(),
        ),
        data: (d) => RefreshIndicator(
          onRefresh: () => ref.read(homeControllerProvider.notifier).refresh(),
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _StreakBanner(current: d.currentStreak, longest: d.longestStreak),
              const SizedBox(height: 16),
              _CalorieCard(d: d),
              const SizedBox(height: 16),
              _MacrosRow(d: d),
              const SizedBox(height: 16),
              if (d.objective != null) _GoalCard(d: d),
              if (d.motivationalMessage.isNotEmpty) ...[
                const SizedBox(height: 16),
                _MotivationCard(message: d.motivationalMessage),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class _StreakBanner extends StatelessWidget {
  final int current;
  final int longest;
  const _StreakBanner({required this.current, required this.longest});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Row(
      children: [
        const Text('🔥', style: TextStyle(fontSize: 28)),
        const SizedBox(width: 8),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('$current ${current == 1 ? 'dia' : 'dias'} de sequência',
                style: theme.textTheme.titleMedium
                    ?.copyWith(fontWeight: FontWeight.bold)),
            Text('Recorde: $longest', style: theme.textTheme.bodySmall),
          ],
        ),
      ],
    );
  }
}

class _CalorieCard extends StatelessWidget {
  final DashboardModel d;
  const _CalorieCard({required this.d});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final hasTarget = d.dailyCalorieTarget != null;
    final remaining = d.caloriesRemaining;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Stack(
              alignment: Alignment.center,
              children: [
                SizedBox(
                  height: 140,
                  width: 140,
                  child: CircularProgressIndicator(
                    value: hasTarget ? d.calorieProgress : null,
                    strokeWidth: 12,
                    backgroundColor:
                        theme.colorScheme.surfaceContainerHighest,
                  ),
                ),
                Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(fmtKcal(d.caloriesConsumed),
                        style: theme.textTheme.headlineMedium
                            ?.copyWith(fontWeight: FontWeight.bold)),
                    Text('kcal hoje', style: theme.textTheme.bodySmall),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (hasTarget)
              Text(
                remaining != null && remaining >= 0
                    ? 'Faltam ${fmtKcal(remaining)} kcal para a meta de ${d.dailyCalorieTarget}'
                    : 'Você passou ${fmtKcal(-(remaining ?? 0))} kcal da meta de ${d.dailyCalorieTarget}',
                textAlign: TextAlign.center,
                style: theme.textTheme.bodyMedium,
              )
            else
              Text('Defina uma meta no seu perfil para acompanhar.',
                  textAlign: TextAlign.center,
                  style: theme.textTheme.bodyMedium),
            const SizedBox(height: 4),
            Text('${d.mealsToday} ${d.mealsToday == 1 ? 'refeição' : 'refeições'} registradas',
                style: theme.textTheme.bodySmall),
          ],
        ),
      ),
    );
  }
}

class _MacrosRow extends StatelessWidget {
  final DashboardModel d;
  const _MacrosRow({required this.d});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(child: _MacroTile(label: 'Proteína', grams: d.proteinG, color: Colors.redAccent)),
        const SizedBox(width: 12),
        Expanded(child: _MacroTile(label: 'Carboidrato', grams: d.carbsG, color: Colors.amber)),
        const SizedBox(width: 12),
        Expanded(child: _MacroTile(label: 'Gordura', grams: d.fatG, color: Colors.blueAccent)),
      ],
    );
  }
}

class _MacroTile extends StatelessWidget {
  final String label;
  final double grams;
  final Color color;
  const _MacroTile({required this.label, required this.grams, required this.color});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 8),
        child: Column(
          children: [
            Container(width: 10, height: 10, decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
            const SizedBox(height: 8),
            Text('${fmtG(grams)} g',
                style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
            Text(label, style: theme.textTheme.bodySmall, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}

class _GoalCard extends StatelessWidget {
  final DashboardModel d;
  const _GoalCard({required this.d});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: const Icon(Icons.flag_outlined),
        title: Text(GoalModel.objectiveLabel(d.objective ?? '')),
        subtitle: Text(
          [
            if (d.currentWeightKg != null) 'Atual: ${fmtKg(d.currentWeightKg!)}',
            if (d.targetWeightKg != null) 'Meta: ${fmtKg(d.targetWeightKg!)}',
          ].join('  •  '),
        ),
      ),
    );
  }
}

class _MotivationCard extends StatelessWidget {
  final String message;
  const _MotivationCard({required this.message});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      color: theme.colorScheme.primaryContainer,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            const Text('💪', style: TextStyle(fontSize: 24)),
            const SizedBox(width: 12),
            Expanded(
              child: Text(message,
                  style: theme.textTheme.bodyMedium?.copyWith(
                      color: theme.colorScheme.onPrimaryContainer)),
            ),
          ],
        ),
      ),
    );
  }
}

/// Estado de erro reutilizável (Home/Refeições).
class _ErrorView extends StatelessWidget {
  final String message;
  final VoidCallback onRetry;
  const _ErrorView({required this.message, required this.onRetry});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.cloud_off, size: 48),
            const SizedBox(height: 12),
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 16),
            FilledButton.tonal(onPressed: onRetry, child: const Text('Tentar de novo')),
          ],
        ),
      ),
    );
  }
}
