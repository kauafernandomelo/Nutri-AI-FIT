import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { Button, Input, Screen } from '@/components/ui';
import {
  createGoal,
  updateProfile,
  type ActivityLevel,
  type Objective,
  type Sex,
} from '@/lib/api';
import { apiError } from '@/lib/format';
import { useSession } from '@/lib/session';
import { colors, radius, sp } from '@/lib/theme';

const SEX: { value: Sex; label: string }[] = [
  { value: 'male', label: 'Masculino' },
  { value: 'female', label: 'Feminino' },
  { value: 'other', label: 'Outro' },
];

const OBJECTIVES: { value: Objective; label: string }[] = [
  { value: 'lose_weight', label: 'Emagrecer' },
  { value: 'gain_muscle', label: 'Ganhar massa' },
  { value: 'maintain', label: 'Manter peso' },
];

const ACTIVITY: { value: ActivityLevel; label: string }[] = [
  { value: 'sedentary', label: 'Sedentário' },
  { value: 'light', label: 'Leve' },
  { value: 'moderate', label: 'Moderado' },
  { value: 'active', label: 'Ativo' },
  { value: 'very_active', label: 'Muito ativo' },
];

function Chips<T extends string>({
  options,
  selected,
  onSelect,
}: {
  options: { value: T; label: string }[];
  selected: T;
  onSelect: (v: T) => void;
}) {
  return (
    <View style={styles.chips}>
      {options.map((o) => {
        const active = o.value === selected;
        return (
          <Pressable
            key={o.value}
            onPress={() => onSelect(o.value)}
            style={[styles.chip, active && styles.chipActive]}>
            <Text style={[styles.chipText, active && styles.chipTextActive]}>
              {o.label}
            </Text>
          </Pressable>
        );
      })}
    </View>
  );
}

const num = (s: string): number => Number(s.replace(',', '.'));

export default function Onboarding() {
  const { refresh } = useSession();
  const [sex, setSex] = useState<Sex>('male');
  const [age, setAge] = useState('');
  const [height, setHeight] = useState('');
  const [objective, setObjective] = useState<Objective>('lose_weight');
  const [activity, setActivity] = useState<ActivityLevel>('moderate');
  const [startWeight, setStartWeight] = useState('');
  const [targetWeight, setTargetWeight] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function validate(): string | null {
    const a = num(age);
    if (!Number.isFinite(a) || a < 10 || a > 120) return 'Idade deve estar entre 10 e 120.';
    const h = num(height);
    if (!Number.isFinite(h) || h < 50 || h > 260) return 'Altura (cm) deve estar entre 50 e 260.';
    const sw = num(startWeight);
    if (!Number.isFinite(sw) || sw <= 0 || sw > 500) return 'Peso atual inválido.';
    const tw = num(targetWeight);
    if (!Number.isFinite(tw) || tw <= 0 || tw > 500) return 'Peso alvo inválido.';
    return null;
  }

  async function submit() {
    const v = validate();
    if (v) {
      setError(v);
      return;
    }
    setError(null);
    setLoading(true);
    try {
      await updateProfile({ sex, age: Math.round(num(age)), height_cm: num(height) });
      await createGoal({
        objective,
        activity_level: activity,
        start_weight_kg: num(startWeight),
        target_weight_kg: num(targetWeight),
      });
      await refresh(); // sai do onboarding
    } catch (e) {
      setError(apiError(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <Screen scroll>
      <Text style={styles.section}>Sobre você</Text>
      <Text style={styles.label}>Sexo</Text>
      <Chips options={SEX} selected={sex} onSelect={setSex} />
      <View style={styles.row}>
        <View style={styles.col}>
          <Input
            label="Idade"
            value={age}
            onChangeText={setAge}
            keyboardType="number-pad"
            placeholder="anos"
          />
        </View>
        <View style={styles.col}>
          <Input
            label="Altura (cm)"
            value={height}
            onChangeText={setHeight}
            keyboardType="decimal-pad"
            placeholder="cm"
          />
        </View>
      </View>

      <Text style={styles.section}>Sua meta</Text>
      <Text style={styles.label}>Objetivo</Text>
      <Chips options={OBJECTIVES} selected={objective} onSelect={setObjective} />
      <Text style={styles.label}>Nível de atividade</Text>
      <Chips options={ACTIVITY} selected={activity} onSelect={setActivity} />
      <View style={styles.row}>
        <View style={styles.col}>
          <Input
            label="Peso atual (kg)"
            value={startWeight}
            onChangeText={setStartWeight}
            keyboardType="decimal-pad"
            placeholder="kg"
          />
        </View>
        <View style={styles.col}>
          <Input
            label="Peso alvo (kg)"
            value={targetWeight}
            onChangeText={setTargetWeight}
            keyboardType="decimal-pad"
            placeholder="kg"
          />
        </View>
      </View>

      {error ? <Text style={styles.error}>{error}</Text> : null}

      <View style={{ height: sp(2) }} />
      <Button title="Concluir" onPress={submit} loading={loading} />
      <View style={{ height: sp(6) }} />
    </Screen>
  );
}

const styles = StyleSheet.create({
  section: {
    fontSize: 18,
    fontWeight: '700',
    color: colors.text,
    marginTop: sp(4),
    marginBottom: sp(2),
  },
  label: { fontSize: 13, color: colors.textMuted, marginBottom: sp(2) },
  row: { flexDirection: 'row', gap: sp(3) },
  col: { flex: 1 },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: sp(2), marginBottom: sp(3) },
  chip: {
    paddingHorizontal: sp(3.5),
    paddingVertical: sp(2.5),
    borderRadius: radius.pill,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.surface,
  },
  chipActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  chipText: { color: colors.text, fontSize: 14 },
  chipTextActive: { color: colors.white, fontWeight: '600' },
  error: { color: colors.danger, marginTop: sp(2) },
});
