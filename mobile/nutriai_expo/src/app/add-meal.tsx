import { Image } from 'expo-image';
import * as ImagePicker from 'expo-image-picker';
import { useRouter } from 'expo-router';
import { useState } from 'react';
import { Alert, ScrollView, StyleSheet, Text, View } from 'react-native';

import { Button, Card } from '@/components/ui';
import { createMeal, type Meal } from '@/lib/api';
import { apiError, fmtG, fmtKcal } from '@/lib/format';
import { colors, radius, sp } from '@/lib/theme';

export default function AddMeal() {
  const router = useRouter();
  const [uri, setUri] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<Meal | null>(null);

  async function pick(source: 'camera' | 'gallery') {
    const perm =
      source === 'camera'
        ? await ImagePicker.requestCameraPermissionsAsync()
        : await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!perm.granted) {
      Alert.alert('Permissão necessária', 'Autorize o acesso para continuar.');
      return;
    }
    const res =
      source === 'camera'
        ? await ImagePicker.launchCameraAsync({ mediaTypes: ['images'], quality: 0.8 })
        : await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images'], quality: 0.8 });
    if (!res.canceled && res.assets[0]) {
      setUri(res.assets[0].uri);
      setResult(null);
    }
  }

  async function analyze() {
    if (!uri) return;
    setAnalyzing(true);
    try {
      const meal = await createMeal(uri);
      setResult(meal);
    } catch (e) {
      Alert.alert('Erro', apiError(e));
    } finally {
      setAnalyzing(false);
    }
  }

  return (
    <ScrollView
      style={{ backgroundColor: colors.bg }}
      contentContainerStyle={{ padding: sp(4) }}>
      <View style={styles.preview}>
        {uri ? (
          <Image source={{ uri }} style={styles.previewImg} contentFit="cover" />
        ) : (
          <View style={styles.previewEmpty}>
            <Text style={{ fontSize: 48 }}>📷</Text>
            <Text style={{ color: colors.textMuted, marginTop: sp(2) }}>
              Tire uma foto do seu prato
            </Text>
          </View>
        )}
      </View>

      {result ? (
        <ResultCard meal={result} onDone={() => router.back()} />
      ) : (
        <>
          <View style={styles.row}>
            <View style={{ flex: 1 }}>
              <Button title="Câmera" variant="outline" onPress={() => pick('camera')} />
            </View>
            <View style={{ flex: 1 }}>
              <Button title="Galeria" variant="outline" onPress={() => pick('gallery')} />
            </View>
          </View>
          <View style={{ height: sp(3) }} />
          <Button
            title={analyzing ? 'Analisando…' : '✨ Analisar com IA'}
            onPress={analyze}
            loading={analyzing}
            disabled={!uri}
          />
        </>
      )}
    </ScrollView>
  );
}

function ResultCard({ meal, onDone }: { meal: Meal; onDone: () => void }) {
  return (
    <View>
      <Card style={styles.resultCard}>
        <Text style={styles.resultName}>{meal.name}</Text>
        {meal.description ? (
          <Text style={styles.resultDesc}>{meal.description}</Text>
        ) : null}
        <Text style={styles.resultKcal}>{fmtKcal(meal.calories)} kcal</Text>
        <Text style={styles.resultMacros}>
          Proteína {fmtG(meal.protein_g)}g • Carbo {fmtG(meal.carbs_g)}g • Gordura{' '}
          {fmtG(meal.fat_g)}g
        </Text>
      </Card>

      {meal.items && meal.items.length > 0 ? (
        <>
          <Text style={styles.itemsTitle}>Alimentos detectados</Text>
          {meal.items.map((it, i) => (
            <Card key={i} style={{ marginTop: sp(2) }}>
              <View style={styles.itemRow}>
                <View style={{ flex: 1 }}>
                  <Text style={styles.itemName}>{it.name}</Text>
                  {it.quantity ? (
                    <Text style={{ color: colors.textMuted, fontSize: 12 }}>
                      {it.quantity}
                    </Text>
                  ) : null}
                </View>
                <Text style={{ color: colors.textMuted }}>
                  {fmtKcal(it.calories)} kcal
                </Text>
              </View>
            </Card>
          ))}
        </>
      ) : null}

      <View style={{ height: sp(5) }} />
      <Button title="Concluir" onPress={onDone} />
      <View style={{ height: sp(6) }} />
    </View>
  );
}

const styles = StyleSheet.create({
  preview: { marginBottom: sp(4) },
  previewImg: { width: '100%', aspectRatio: 4 / 3, borderRadius: radius.lg },
  previewEmpty: {
    width: '100%',
    aspectRatio: 4 / 3,
    borderRadius: radius.lg,
    backgroundColor: colors.surfaceAlt,
    alignItems: 'center',
    justifyContent: 'center',
  },
  row: { flexDirection: 'row', gap: sp(3) },
  resultCard: {
    backgroundColor: colors.primaryContainer,
    borderColor: colors.primaryContainer,
  },
  resultName: { fontSize: 20, fontWeight: '800', color: colors.onPrimaryContainer },
  resultDesc: { color: colors.onPrimaryContainer, marginTop: sp(1) },
  resultKcal: {
    fontSize: 24,
    fontWeight: '800',
    color: colors.onPrimaryContainer,
    marginTop: sp(3),
  },
  resultMacros: { color: colors.onPrimaryContainer, marginTop: sp(1) },
  itemsTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: colors.text,
    marginTop: sp(4),
  },
  itemRow: { flexDirection: 'row', alignItems: 'center' },
  itemName: { fontSize: 15, color: colors.text },
});
