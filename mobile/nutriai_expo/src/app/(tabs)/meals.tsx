import { useRouter } from 'expo-router';
import {
  FlatList,
  Pressable,
  RefreshControl,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { MealImage } from '@/components/meal-image';
import { ErrorView, Loading } from '@/components/ui';
import { listMeals, type Meal } from '@/lib/api';
import { apiError, fmtDayMonth, fmtG, fmtKcal, fmtTime } from '@/lib/format';
import { colors, radius, sp } from '@/lib/theme';
import { useApi } from '@/lib/use-api';

export default function MealsScreen() {
  const router = useRouter();
  const { data, loading, error, refreshing, refresh } = useApi(listMeals);

  if (loading) return <Loading />;
  if (error || !data) {
    return <ErrorView message={apiError(error)} onRetry={refresh} />;
  }

  return (
    <FlatList
      style={{ backgroundColor: colors.bg }}
      contentContainerStyle={{ padding: sp(4), flexGrow: 1 }}
      data={data}
      keyExtractor={(m) => String(m.id)}
      ItemSeparatorComponent={() => <View style={{ height: sp(3) }} />}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={refresh} />
      }
      ListEmptyComponent={<Empty onAdd={() => router.push('/add-meal')} />}
      renderItem={({ item }) => <MealRow meal={item} />}
    />
  );
}

function MealRow({ meal }: { meal: Meal }) {
  return (
    <View style={styles.row}>
      {meal.image_url ? (
        <MealImage mealId={meal.id} style={styles.thumb} />
      ) : (
        <View style={[styles.thumb, styles.thumbPlaceholder]}>
          <Text style={{ fontSize: 26 }}>🍽️</Text>
        </View>
      )}
      <View style={{ flex: 1, padding: sp(3) }}>
        <Text style={styles.name} numberOfLines={1}>
          {meal.name}
        </Text>
        <Text style={styles.meta}>
          {fmtKcal(meal.calories)} kcal • P {fmtG(meal.protein_g)}g C{' '}
          {fmtG(meal.carbs_g)}g G {fmtG(meal.fat_g)}g
        </Text>
        <Text style={styles.date}>
          {fmtDayMonth(meal.consumed_at)} às {fmtTime(meal.consumed_at)}
        </Text>
      </View>
    </View>
  );
}

function Empty({ onAdd }: { onAdd: () => void }) {
  return (
    <View style={styles.empty}>
      <Text style={{ fontSize: 52 }}>🍽️</Text>
      <Text style={styles.emptyTitle}>Nenhuma refeição ainda</Text>
      <Text style={[styles.meta, { textAlign: 'center', marginTop: sp(1) }]}>
        Toque para registrar a sua primeira.
      </Text>
      <Pressable onPress={onAdd} style={styles.emptyBtn}>
        <Text style={styles.emptyBtnText}>📷 Registrar refeição</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    overflow: 'hidden',
  },
  thumb: { width: 88, height: 88 },
  thumbPlaceholder: {
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.surfaceAlt,
  },
  name: { fontSize: 16, fontWeight: '600', color: colors.text },
  meta: { fontSize: 12, color: colors.textMuted, marginTop: sp(1) },
  date: { fontSize: 12, color: colors.textMuted, marginTop: sp(1) },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', paddingTop: sp(20) },
  emptyTitle: { fontSize: 18, fontWeight: '700', color: colors.text, marginTop: sp(3) },
  emptyBtn: {
    marginTop: sp(5),
    backgroundColor: colors.primary,
    paddingHorizontal: sp(5),
    paddingVertical: sp(3),
    borderRadius: radius.md,
  },
  emptyBtnText: { color: colors.white, fontWeight: '600', fontSize: 15 },
});
