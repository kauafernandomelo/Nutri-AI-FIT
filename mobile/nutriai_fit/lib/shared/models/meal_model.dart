/// Espelham MealRead / MealItem do backend.
class MealItemModel {
  final String name;
  final String? quantity;
  final double calories;
  final double proteinG;
  final double carbsG;
  final double fatG;

  const MealItemModel({
    required this.name,
    this.quantity,
    required this.calories,
    required this.proteinG,
    required this.carbsG,
    required this.fatG,
  });

  factory MealItemModel.fromJson(Map<String, dynamic> json) {
    return MealItemModel(
      name: json['name'] as String? ?? 'Alimento',
      quantity: json['quantity'] as String?,
      calories: (json['calories'] as num?)?.toDouble() ?? 0,
      proteinG: (json['protein_g'] as num?)?.toDouble() ?? 0,
      carbsG: (json['carbs_g'] as num?)?.toDouble() ?? 0,
      fatG: (json['fat_g'] as num?)?.toDouble() ?? 0,
    );
  }
}

class MealModel {
  final int id;
  final String name;
  final String? description;
  final double calories;
  final double proteinG;
  final double carbsG;
  final double fatG;
  final List<MealItemModel> items;
  final String? imageUrl;
  final String? aiProvider;
  final DateTime consumedAt;

  const MealModel({
    required this.id,
    required this.name,
    this.description,
    required this.calories,
    required this.proteinG,
    required this.carbsG,
    required this.fatG,
    required this.items,
    this.imageUrl,
    this.aiProvider,
    required this.consumedAt,
  });

  factory MealModel.fromJson(Map<String, dynamic> json) {
    final rawItems = (json['items'] as List?) ?? const [];
    return MealModel(
      id: json['id'] as int,
      name: json['name'] as String,
      description: json['description'] as String?,
      calories: (json['calories'] as num?)?.toDouble() ?? 0,
      proteinG: (json['protein_g'] as num?)?.toDouble() ?? 0,
      carbsG: (json['carbs_g'] as num?)?.toDouble() ?? 0,
      fatG: (json['fat_g'] as num?)?.toDouble() ?? 0,
      items: rawItems
          .map((e) => MealItemModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      imageUrl: json['image_url'] as String?,
      aiProvider: json['ai_provider'] as String?,
      consumedAt: DateTime.parse(json['consumed_at'] as String),
    );
  }
}
