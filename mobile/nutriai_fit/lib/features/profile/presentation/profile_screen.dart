import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../shared/models/goal_model.dart';
import '../../../shared/models/weight_model.dart';
import '../../../shared/ui_helpers.dart';
import '../../auth/presentation/auth_controller.dart';
import '../../home/presentation/home_controller.dart';
import '../data/profile_repository.dart';

/// Metas do usuário (a ativa fica em primeiro lugar na lista do backend).
final _goalsProvider = FutureProvider.autoDispose<List<GoalModel>>(
  (ref) => ref.read(profileRepositoryProvider).listGoals(),
);

/// Histórico de pesos, do mais recente para o mais antigo.
final _weightsProvider = FutureProvider.autoDispose<List<WeightModel>>(
  (ref) => ref.read(profileRepositoryProvider).listWeights(),
);

/// Perfil: dados do usuário, meta ativa, histórico de peso e logout.
class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authControllerProvider).user;
    final goals = ref.watch(_goalsProvider);
    final weights = ref.watch(_weightsProvider);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Perfil'),
        actions: [
          IconButton(
            tooltip: 'Sair',
            icon: const Icon(Icons.logout),
            onPressed: () => _confirmLogout(context, ref),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(_goalsProvider);
          ref.invalidate(_weightsProvider);
        },
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if (user != null) ...[
              CircleAvatar(
                radius: 36,
                child: Text(
                  user.name.isNotEmpty ? user.name[0].toUpperCase() : '?',
                  style: theme.textTheme.headlineMedium,
                ),
              ),
              const SizedBox(height: 12),
              Center(
                child: Text(user.name,
                    style: theme.textTheme.titleLarge
                        ?.copyWith(fontWeight: FontWeight.bold)),
              ),
              Center(child: Text(user.email, style: theme.textTheme.bodyMedium)),
              const SizedBox(height: 16),
              Card(
                child: Column(
                  children: [
                    _InfoTile(
                      icon: Icons.wc,
                      label: 'Sexo',
                      value: _sexLabel(user.sex),
                    ),
                    _InfoTile(
                      icon: Icons.cake_outlined,
                      label: 'Idade',
                      value: user.age != null ? '${user.age} anos' : '—',
                    ),
                    _InfoTile(
                      icon: Icons.height,
                      label: 'Altura',
                      value: user.heightCm != null
                          ? '${fmtG(user.heightCm!)} cm'
                          : '—',
                    ),
                  ],
                ),
              ),
            ],
            const SizedBox(height: 24),
            Text('Minha meta', style: theme.textTheme.titleMedium),
            const SizedBox(height: 8),
            goals.when(
              loading: () => const _CardLoader(),
              error: (e, _) => _CardError(message: apiError(e)),
              data: (list) => list.isEmpty
                  ? const Card(
                      child: ListTile(title: Text('Nenhuma meta definida.')))
                  : _GoalTile(goal: list.first),
            ),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Histórico de peso', style: theme.textTheme.titleMedium),
                TextButton.icon(
                  onPressed: () => _addWeight(context, ref),
                  icon: const Icon(Icons.add),
                  label: const Text('Registrar'),
                ),
              ],
            ),
            const SizedBox(height: 8),
            weights.when(
              loading: () => const _CardLoader(),
              error: (e, _) => _CardError(message: apiError(e)),
              data: (list) => list.isEmpty
                  ? const Card(
                      child: ListTile(
                          title: Text('Nenhum peso registrado ainda.')))
                  : Card(
                      child: Column(
                        children: [
                          for (final w in list.take(10))
                            ListTile(
                              leading: const Icon(Icons.monitor_weight_outlined),
                              title: Text(fmtKg(w.weightKg)),
                              trailing: Text(fmtDayMonth(w.recordedAt)),
                            ),
                        ],
                      ),
                    ),
            ),
          ],
        ),
      ),
    );
  }

  static String _sexLabel(String? sex) => switch (sex) {
        'male' => 'Masculino',
        'female' => 'Feminino',
        'other' => 'Outro',
        _ => '—',
      };

  Future<void> _confirmLogout(BuildContext context, WidgetRef ref) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Sair da conta?'),
        content: const Text('Você precisará entrar novamente.'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(ctx, false),
              child: const Text('Cancelar')),
          FilledButton(
              onPressed: () => Navigator.pop(ctx, true),
              child: const Text('Sair')),
        ],
      ),
    );
    if (ok == true) {
      await ref.read(authControllerProvider.notifier).logout();
    }
  }

  Future<void> _addWeight(BuildContext context, WidgetRef ref) async {
    final controller = TextEditingController();
    final value = await showDialog<double>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Registrar peso'),
        content: TextField(
          controller: controller,
          autofocus: true,
          keyboardType: const TextInputType.numberWithOptions(decimal: true),
          decoration: const InputDecoration(labelText: 'Peso', suffixText: 'kg'),
        ),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('Cancelar')),
          FilledButton(
            onPressed: () {
              final n = double.tryParse(controller.text.replaceAll(',', '.'));
              Navigator.pop(ctx, (n != null && n > 0 && n <= 500) ? n : null);
            },
            child: const Text('Salvar'),
          ),
        ],
      ),
    );
    if (value == null) return;
    try {
      await ref.read(profileRepositoryProvider).createWeight(weightKg: value);
      ref.invalidate(_weightsProvider);
      ref.invalidate(homeControllerProvider); // peso atual aparece na Home
    } catch (e) {
      if (context.mounted) showError(context, e);
    }
  }
}

class _InfoTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  const _InfoTile({required this.icon, required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon),
      title: Text(label),
      trailing: Text(value, style: Theme.of(context).textTheme.bodyLarge),
    );
  }
}

class _GoalTile extends StatelessWidget {
  final GoalModel goal;
  const _GoalTile({required this.goal});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        children: [
          ListTile(
            leading: const Icon(Icons.flag_outlined),
            title: Text(GoalModel.objectiveLabel(goal.objective)),
            subtitle: Text(
                'De ${fmtKg(goal.startWeightKg)} para ${fmtKg(goal.targetWeightKg)}'),
          ),
          const Divider(height: 1),
          ListTile(
            leading: const Icon(Icons.local_fire_department_outlined),
            title: const Text('Meta diária de calorias'),
            trailing: Text('${goal.dailyCalorieTarget} kcal',
                style: Theme.of(context).textTheme.bodyLarge),
          ),
        ],
      ),
    );
  }
}

class _CardLoader extends StatelessWidget {
  const _CardLoader();
  @override
  Widget build(BuildContext context) => const Card(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Center(child: CircularProgressIndicator()),
        ),
      );
}

class _CardError extends StatelessWidget {
  final String message;
  const _CardError({required this.message});
  @override
  Widget build(BuildContext context) =>
      Card(child: ListTile(leading: const Icon(Icons.error_outline), title: Text(message)));
}
