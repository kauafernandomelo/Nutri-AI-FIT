import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../shared/models/goal_model.dart';
import '../../../shared/ui_helpers.dart';
import '../../auth/presentation/auth_controller.dart';
import '../../profile/data/profile_repository.dart';

/// Onboarding em um único formulário: dados corporais (perfil) + primeira meta.
///
/// Ao concluir, o backend calcula a meta diária de calorias (Mifflin-St Jeor)
/// e o `refreshUser()` reavalia o AuthState — o redirect do router leva à Home.
class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  final _formKey = GlobalKey<FormState>();
  final _age = TextEditingController();
  final _height = TextEditingController();
  final _startWeight = TextEditingController();
  final _targetWeight = TextEditingController();

  String _sex = 'male';
  String _objective = 'lose_weight';
  String _activity = 'moderate';
  bool _loading = false;

  // Rótulos em PT-BR para os enums do backend.
  static const _activityLabels = {
    'sedentary': 'Sedentário (pouco ou nenhum exercício)',
    'light': 'Leve (1–3x/semana)',
    'moderate': 'Moderado (3–5x/semana)',
    'active': 'Ativo (6–7x/semana)',
    'very_active': 'Muito ativo (treino intenso/diário)',
  };

  @override
  void dispose() {
    _age.dispose();
    _height.dispose();
    _startWeight.dispose();
    _targetWeight.dispose();
    super.dispose();
  }

  String? _validateRange(String? v, double min, double max, String label) {
    if (v == null || v.trim().isEmpty) return 'Informe $label';
    final n = double.tryParse(v.replaceAll(',', '.'));
    if (n == null) return 'Valor inválido';
    if (n < min || n > max) return '$label deve estar entre ${min.toStringAsFixed(0)} e ${max.toStringAsFixed(0)}';
    return null;
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      final profile = ref.read(profileRepositoryProvider);
      // 1) Completa o perfil (sexo/idade/altura).
      await profile.updateProfile(
        sex: _sex,
        age: int.parse(_age.text.trim()),
        heightCm: double.parse(_height.text.replaceAll(',', '.')),
      );
      // 2) Cria a meta — aqui o backend calcula daily_calorie_target.
      await profile.createGoal(
        objective: _objective,
        startWeightKg: double.parse(_startWeight.text.replaceAll(',', '.')),
        targetWeightKg: double.parse(_targetWeight.text.replaceAll(',', '.')),
        activityLevel: _activity,
      );
      // 3) Reavalia o estado de autenticação → sai do onboarding.
      await ref.read(authControllerProvider.notifier).refreshUser();
    } catch (e) {
      if (mounted) showError(context, e);
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Vamos montar seu plano')),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text('Sobre você', style: theme.textTheme.titleMedium),
                const SizedBox(height: 12),
                SegmentedButton<String>(
                  segments: const [
                    ButtonSegment(value: 'male', label: Text('Masculino')),
                    ButtonSegment(value: 'female', label: Text('Feminino')),
                    ButtonSegment(value: 'other', label: Text('Outro')),
                  ],
                  selected: {_sex},
                  onSelectionChanged: (s) => setState(() => _sex = s.first),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _age,
                        keyboardType: TextInputType.number,
                        decoration: const InputDecoration(
                          labelText: 'Idade',
                          suffixText: 'anos',
                        ),
                        validator: (v) => _validateRange(v, 10, 120, 'a idade'),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: TextFormField(
                        controller: _height,
                        keyboardType: const TextInputType.numberWithOptions(decimal: true),
                        decoration: const InputDecoration(
                          labelText: 'Altura',
                          suffixText: 'cm',
                        ),
                        validator: (v) => _validateRange(v, 50, 260, 'a altura'),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 28),
                Text('Sua meta', style: theme.textTheme.titleMedium),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                  value: _objective,
                  decoration: const InputDecoration(labelText: 'Objetivo'),
                  items: const ['lose_weight', 'gain_muscle', 'maintain']
                      .map((o) => DropdownMenuItem(
                            value: o,
                            child: Text(GoalModel.objectiveLabel(o)),
                          ))
                      .toList(),
                  onChanged: (v) => setState(() => _objective = v ?? _objective),
                ),
                const SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  value: _activity,
                  isExpanded: true,
                  decoration: const InputDecoration(labelText: 'Nível de atividade'),
                  items: _activityLabels.entries
                      .map((e) => DropdownMenuItem(
                            value: e.key,
                            child: Text(e.value, overflow: TextOverflow.ellipsis),
                          ))
                      .toList(),
                  onChanged: (v) => setState(() => _activity = v ?? _activity),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _startWeight,
                        keyboardType: const TextInputType.numberWithOptions(decimal: true),
                        decoration: const InputDecoration(
                          labelText: 'Peso atual',
                          suffixText: 'kg',
                        ),
                        validator: (v) => _validateRange(v, 1, 500, 'o peso'),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: TextFormField(
                        controller: _targetWeight,
                        keyboardType: const TextInputType.numberWithOptions(decimal: true),
                        decoration: const InputDecoration(
                          labelText: 'Peso alvo',
                          suffixText: 'kg',
                        ),
                        validator: (v) => _validateRange(v, 1, 500, 'o peso alvo'),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 28),
                FilledButton(
                  onPressed: _loading ? null : _submit,
                  child: _loading
                      ? const SizedBox(
                          height: 22,
                          width: 22,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Concluir'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
