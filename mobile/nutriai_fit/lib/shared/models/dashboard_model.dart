/// Espelha o schema DashboardResponse do backend.
class DashboardModel {
  final DateTime date;
  final double caloriesConsumed;
  final int? dailyCalorieTarget;
  final int? caloriesRemaining;
  final double proteinG;
  final double carbsG;
  final double fatG;
  final int mealsToday;
  final int currentStreak;
  final int longestStreak;
  final double? currentWeightKg;
  final double? targetWeightKg;
  final String? objective;
  final String motivationalMessage;

  const DashboardModel({
    required this.date,
    required this.caloriesConsumed,
    this.dailyCalorieTarget,
    this.caloriesRemaining,
    required this.proteinG,
    required this.carbsG,
    required this.fatG,
    required this.mealsToday,
    required this.currentStreak,
    required this.longestStreak,
    this.currentWeightKg,
    this.targetWeightKg,
    this.objective,
    required this.motivationalMessage,
  });

  /// Progresso de calorias (0..1) para a barra na Home.
  double get calorieProgress {
    if (dailyCalorieTarget == null || dailyCalorieTarget == 0) return 0;
    return (caloriesConsumed / dailyCalorieTarget!).clamp(0.0, 1.0);
  }

  factory DashboardModel.fromJson(Map<String, dynamic> json) {
    final macros = (json['macros_today'] as Map<String, dynamic>?) ?? const {};
    return DashboardModel(
      date: DateTime.parse(json['date'] as String),
      caloriesConsumed: (json['calories_consumed'] as num?)?.toDouble() ?? 0,
      dailyCalorieTarget: json['daily_calorie_target'] as int?,
      caloriesRemaining: json['calories_remaining'] as int?,
      proteinG: (macros['protein_g'] as num?)?.toDouble() ?? 0,
      carbsG: (macros['carbs_g'] as num?)?.toDouble() ?? 0,
      fatG: (macros['fat_g'] as num?)?.toDouble() ?? 0,
      mealsToday: json['meals_today'] as int? ?? 0,
      currentStreak: json['current_streak'] as int? ?? 0,
      longestStreak: json['longest_streak'] as int? ?? 0,
      currentWeightKg: (json['current_weight_kg'] as num?)?.toDouble(),
      targetWeightKg: (json['target_weight_kg'] as num?)?.toDouble(),
      objective: json['objective'] as String?,
      motivationalMessage: json['motivational_message'] as String? ?? '',
    );
  }
}
