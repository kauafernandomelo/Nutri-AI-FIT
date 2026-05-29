/// Espelha o schema WeightRead do backend.
class WeightModel {
  final int id;
  final double weightKg;
  final DateTime recordedAt;

  const WeightModel({
    required this.id,
    required this.weightKg,
    required this.recordedAt,
  });

  factory WeightModel.fromJson(Map<String, dynamic> json) {
    return WeightModel(
      id: json['id'] as int,
      weightKg: (json['weight_kg'] as num).toDouble(),
      recordedAt: DateTime.parse(json['recorded_at'] as String),
    );
  }
}
