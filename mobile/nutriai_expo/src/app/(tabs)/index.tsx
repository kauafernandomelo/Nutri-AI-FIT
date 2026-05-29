import { useRouter } from 'expo-router';
import {
  RefreshControl,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { Button, Card, ErrorView, Loading } from '@/components/ui';
import { getDashboard, type Objective } from '@/lib/api';
import { apiError, fmtG, fmtKcal, fmtKg } from '@/lib/format';
import { useApi } from '@/lib/use-api';
import { colors, radius, sp } from '@/lib/theme';

const OBJECTIVE_LABEL: Record<Objective, string> = {
  lose_weight: 'Emagrecer',
  gain_muscle: 'Ganhar massa',
  maintain: 'Manter peso',
};

export default function HomeScreen() {
  const router = useRouter();
  const { data, loading, error, refreshing, refresh } = useApi(getDashboard);

  if (loading) return <Loading />;
  if (error || !data) {
    return <ErrorView message={apiError(error)} onRetry={refresh} />;
  }
  const d = data;

  const hasTarget = d.daily_calorie_target != null;
  const progress = hasTarget
    ? Math.min(Math.max(d.calories_consumed / d.daily_calorie_target!, 0), 1)
    : 0;
  const remaining = d.calories_remaining;

  return (
    <ScrollView
      style={{ backgroundColor: colors.bg }}
      contentContainerStyle={{ padding: sp(4) }}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={refresh} />
      }>
      {/* Streak */}
      <View style={styles.streakRow}>
        <Text style={{ fontSize: 28 }}>🔥</Text>
        <View>
          <Text style={styles.streakNum}>
            {d.current_streak} {d.current_streak === 1 ? 'dia' : 'dias'} de sequência
          </Text>
          <Text style={styles.muted}>Recorde: {d.longest_streak}</Text>
        </View>
      </View>

      {/* Calorias */}
      <Card style={{ marginTop: sp(4), alignItems: 'center' }}>
        <Text style={styles.kcalBig}>{fmtKcal(d.calories_consumed)}</Text>
        <Text style={styles.muted}>kcal consumidas hoje</Text>
        {hasTarget ? (
          <>
            <View style={styles.track}>
              <View style={[styles.fill, { width: `${progress * 100}%` }]} />
            </View>
            <Text style={[styles.muted, { marginTop: sp(2), textAlign: 'center' }]}>
              {remaining != null && remaining >= 0
                ? `Faltam ${fmtKcal(remaining)} kcal para a meta de ${d.daily_calorie_target}`
                : `Você passou ${fmtKcal(Math.abs(remaining ?? 0))} kcal da meta de ${d.daily_calorie_target}`}
            </Text>
          </>
        ) : (
          <Text style={[styles.muted, { marginTop: sp(2) }]}>
            Defina uma meta no seu perfil.
          </Text>
        )}
        <Text style={[styles.muted, { marginTop: sp(1) }]}>
          {d.meals_today} {d.meals_today === 1 ? 'refeição' : 'refeições'} hoje
        </Text>
      </Card>

      {/* Macros */}
      <View style={styles.macros}>
        <MacroTile label="Proteína" grams={d.macros_today.protein_g} color={colors.protein} />
        <MacroTile label="Carbo" grams={d.macros_today.carbs_g} color={colors.carbs} />
        <MacroTile label="Gordura" grams={d.macros_today.fat_g} color={colors.fat} />
      </View>

      {/* Meta */}
      {d.objective ? (
        <Card style={{ marginTop: sp(4) }}>
          <Text style={styles.cardTitle}>🎯 {OBJECTIVE_LABEL[d.objective]}</Text>
          <Text style={[styles.muted, { marginTop: sp(1) }]}>
            {[
              d.current_weight_kg != null ? `Atual: ${fmtKg(d.current_weight_kg)}` : null,
              d.target_weight_kg != null ? `Meta: ${fmtKg(d.target_weight_kg)}` : null,
            ]
              .filter(Boolean)
              .join('   •   ')}
          </Text>
        </Card>
      ) : null}

      {/* Motivação */}
      {d.motivational_message ? (
        <Card style={styles.motivation}>
          <Text style={styles.motivationText}>💪 {d.motivational_message}</Text>
        </Card>
      ) : null}

      <View style={{ height: sp(4) }} />
      <Button
        title="📷  Registrar refeição"
        onPress={() => router.push('/add-meal')}
      />
      <View style={{ height: sp(6) }} />
    </ScrollView>
  );
}

function MacroTile({
  label,
  grams,
  color,
}: {
  label: string;
  grams: number;
  color: string;
}) {
  return (
    <Card style={styles.macroTile}>
      <View style={[styles.dot, { backgroundColor: color }]} />
      <Text style={styles.macroValue}>{fmtG(grams)} g</Text>
      <Text style={styles.muted}>{label}</Text>
    </Card>
  );
}

const styles = StyleSheet.create({
  streakRow: { flexDirection: 'row', alignItems: 'center', gap: sp(3) },
  streakNum: { fontSize: 17, fontWeight: '700', color: colors.text },
  muted: { color: colors.textMuted, fontSize: 13 },
  kcalBig: { fontSize: 44, fontWeight: '800', color: colors.text },
  track: {
    height: 10,
    borderRadius: radius.pill,
    backgroundColor: colors.surfaceAlt,
    width: '100%',
    marginTop: sp(3),
    overflow: 'hidden',
  },
  fill: { height: 10, borderRadius: radius.pill, backgroundColor: colors.primary },
  macros: { flexDirection: 'row', gap: sp(3), marginTop: sp(4) },
  macroTile: { flex: 1, alignItems: 'center', padding: sp(3) },
  dot: { width: 10, height: 10, borderRadius: 5, marginBottom: sp(2) },
  macroValue: { fontSize: 16, fontWeight: '700', color: colors.text },
  cardTitle: { fontSize: 16, fontWeight: '700', color: colors.text },
  motivation: {
    marginTop: sp(4),
    backgroundColor: colors.primaryContainer,
    borderColor: colors.primaryContainer,
  },
  motivationText: { color: colors.onPrimaryContainer, fontSize: 14, lineHeight: 20 },
});
