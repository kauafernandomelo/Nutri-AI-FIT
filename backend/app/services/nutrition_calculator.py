"""
Cálculo da meta diária de calorias.

TEORIA (explicada para aprender):
1) BMR (Taxa Metabólica Basal) = energia que o corpo gasta em repouso.
   Fórmula de Mifflin-St Jeor (uma das mais aceitas):
     BMR = 10*peso(kg) + 6.25*altura(cm) - 5*idade + s
     onde s = +5 (homem), -161 (mulher), -78 (média, p/ 'outro').
2) TDEE (Gasto Energético Total Diário) = BMR * fator de atividade.
3) Meta por objetivo:
     - Emagrecer  -> déficit de ~500 kcal/dia (~0,5 kg/semana)
     - Ganhar massa -> superávit de ~300 kcal/dia
     - Manter -> TDEE
Aplicamos um piso de segurança de 1200 kcal.
"""
from app.models.enums import ActivityLevel, Objective, Sex

_ACTIVITY_FACTOR: dict[ActivityLevel, float] = {
    ActivityLevel.sedentary: 1.2,
    ActivityLevel.light: 1.375,
    ActivityLevel.moderate: 1.55,
    ActivityLevel.active: 1.725,
    ActivityLevel.very_active: 1.9,
}

_OBJECTIVE_DELTA: dict[Objective, int] = {
    Objective.lose_weight: -500,
    Objective.gain_muscle: +300,
    Objective.maintain: 0,
}

_MIN_CALORIES = 1200


def bmr_mifflin_st_jeor(sex: Sex, weight_kg: float, height_cm: float, age: int) -> float:
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    if sex == Sex.male:
        return base + 5
    if sex == Sex.female:
        return base - 161
    return base - 78  # 'other' → média dos dois


def daily_calorie_target(
    *,
    sex: Sex,
    weight_kg: float,
    height_cm: float,
    age: int,
    activity: ActivityLevel,
    objective: Objective,
) -> int:
    bmr = bmr_mifflin_st_jeor(sex, weight_kg, height_cm, age)
    tdee = bmr * _ACTIVITY_FACTOR[activity]
    target = tdee + _OBJECTIVE_DELTA[objective]
    return max(_MIN_CALORIES, round(target))
