/// Espelha o schema UserRead do backend.
class UserModel {
  final int id;
  final String name;
  final String email;
  final String? sex; // 'male' | 'female' | 'other'
  final int? age;
  final double? heightCm;
  final bool isActive;

  const UserModel({
    required this.id,
    required this.name,
    required this.email,
    this.sex,
    this.age,
    this.heightCm,
    required this.isActive,
  });

  /// True quando o onboarding (sexo/idade/altura) já foi preenchido.
  bool get hasProfile => sex != null && age != null && heightCm != null;

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as int,
      name: json['name'] as String,
      email: json['email'] as String,
      sex: json['sex'] as String?,
      age: json['age'] as int?,
      heightCm: (json['height_cm'] as num?)?.toDouble(),
      isActive: json['is_active'] as bool? ?? true,
    );
  }
}
