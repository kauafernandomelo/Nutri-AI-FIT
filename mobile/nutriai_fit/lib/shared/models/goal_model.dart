/// Espelha o schema GoalRead do backend.
class GoalModel {
  final int id;
  final String objective; // 'lose_weight' | 'gain_muscle' | 'maintain'
  final double startWeightKg;
  final double targetWeightKg;
  final String activityLevel;
  final int dailyCalorieTarget;
  final bool isActive;

  const GoalModel({
    required this.id,
    required this.objective,
    required this.startWeightKg,
    required this.targetWeightKg,
    required this.activityLevel,
    required this.dailyCalorieTarget,
    required this.isActive,
  });

  factory GoalModel.fromJson(Map<String, dynamic> json) {
    return GoalModel(
      id: json['id'] as int,
      objective: json['objective'] as String,
      startWeightKg: (json['start_weight_kg'] as num).toDouble(),
      targetWeightKg: (json['target_weight_kg'] as num).toDouble(),
      activityLevel: json['activity_level'] as String,
      dailyCalorieTarget: json['daily_calorie_target'] as int,
      isActive: json['is_active'] as bool? ?? true,
    );
  }

  static String objectiveLabel(String objective) {
    switch (objective) {
      case 'lose_weight':
        return 'Emagrecer';
      case 'gain_muscle':
        return 'Ganhar massa';
      case 'maintain':
        return 'Manter peso';
      default:
        return objective;
    }
  }
}
