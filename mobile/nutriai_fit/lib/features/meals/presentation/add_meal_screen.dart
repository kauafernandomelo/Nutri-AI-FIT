import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';

import '../../../shared/models/meal_model.dart';
import '../../../shared/ui_helpers.dart';
import '../../home/presentation/home_controller.dart';
import '../data/meal_repository.dart';
import 'meals_controller.dart';

/// Fluxo de registrar refeição: escolher foto → enviar para a IA → ver o
/// resultado. O upload é multipart (ver MealRepository.createMeal).
class AddMealScreen extends ConsumerStatefulWidget {
  const AddMealScreen({super.key});

  @override
  ConsumerState<AddMealScreen> createState() => _AddMealScreenState();
}

class _AddMealScreenState extends ConsumerState<AddMealScreen> {
  final _picker = ImagePicker();
  File? _image;
  bool _analyzing = false;
  MealModel? _result;

  Future<void> _pick(ImageSource source) async {
    try {
      final picked = await _picker.pickImage(
        source: source,
        maxWidth: 1600, // reduz o upload sem perder detalhe relevante
        imageQuality: 85,
      );
      if (picked != null) {
        setState(() {
          _image = File(picked.path);
          _result = null;
        });
      }
    } catch (e) {
      if (mounted) showError(context, e);
    }
  }

  Future<void> _analyze() async {
    final image = _image;
    if (image == null) return;
    setState(() => _analyzing = true);
    try {
      final meal =
          await ref.read(mealRepositoryProvider).createMeal(image.path);
      // Atualiza Home (calorias/streak) e a lista de refeições.
      ref.invalidate(homeControllerProvider);
      ref.invalidate(mealsControllerProvider);
      setState(() => _result = meal);
    } catch (e) {
      if (mounted) showError(context, e);
    } finally {
      if (mounted) setState(() => _analyzing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final result = _result;
    return Scaffold(
      appBar: AppBar(title: const Text('Nova refeição')),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _ImagePreview(image: _image),
              const SizedBox(height: 16),
              if (result == null) ...[
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: _analyzing
                            ? null
                            : () => _pick(ImageSource.camera),
                        icon: const Icon(Icons.photo_camera_outlined),
                        label: const Text('Câmera'),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: _analyzing
                            ? null
                            : () => _pick(ImageSource.gallery),
                        icon: const Icon(Icons.photo_library_outlined),
                        label: const Text('Galeria'),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                FilledButton.icon(
                  onPressed: (_image == null || _analyzing) ? null : _analyze,
                  icon: _analyzing
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.auto_awesome),
                  label: Text(_analyzing ? 'Analisando…' : 'Analisar com IA'),
                ),
              ] else
                _ResultCard(meal: result),
            ],
          ),
        ),
      ),
    );
  }
}

class _ImagePreview extends StatelessWidget {
  final File? image;
  const _ImagePreview({required this.image});

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return AspectRatio(
      aspectRatio: 4 / 3,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(18),
        child: image != null
            ? Image.file(image!, fit: BoxFit.cover)
            : Container(
                color: scheme.surfaceContainerHighest,
                alignment: Alignment.center,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.add_a_photo_outlined,
                        size: 48, color: scheme.outline),
                    const SizedBox(height: 8),
                    Text('Tire uma foto do seu prato',
                        style: TextStyle(color: scheme.outline)),
                  ],
                ),
              ),
      ),
    );
  }
}

class _ResultCard extends ConsumerWidget {
  final MealModel meal;
  const _ResultCard({required this.meal});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Card(
          color: theme.colorScheme.primaryContainer,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(meal.name,
                    style: theme.textTheme.titleLarge
                        ?.copyWith(fontWeight: FontWeight.bold)),
                if (meal.description != null && meal.description!.isNotEmpty) ...[
                  const SizedBox(height: 4),
                  Text(meal.description!),
                ],
                const SizedBox(height: 12),
                Text('${fmtKcal(meal.calories)} kcal',
                    style: theme.textTheme.headlineSmall
                        ?.copyWith(fontWeight: FontWeight.bold)),
                const SizedBox(height: 4),
                Text('Proteína ${fmtG(meal.proteinG)}g  •  '
                    'Carbo ${fmtG(meal.carbsG)}g  •  '
                    'Gordura ${fmtG(meal.fatG)}g'),
              ],
            ),
          ),
        ),
        if (meal.items.isNotEmpty) ...[
          const SizedBox(height: 16),
          Text('Alimentos detectados', style: theme.textTheme.titleMedium),
          const SizedBox(height: 8),
          ...meal.items.map(
            (item) => Card(
              child: ListTile(
                title: Text(item.name),
                subtitle: item.quantity != null ? Text(item.quantity!) : null,
                trailing: Text('${fmtKcal(item.calories)} kcal'),
              ),
            ),
          ),
        ],
        const SizedBox(height: 24),
        FilledButton(
          onPressed: () => context.go('/'),
          child: const Text('Concluir'),
        ),
      ],
    );
  }
}
