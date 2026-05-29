import { useState } from 'react';
import {
  Alert,
  Modal,
  RefreshControl,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { Button, Card, Input } from '@/components/ui';
import {
  createWeight,
  listGoals,
  listWeights,
  type Objective,
  type Sex,
} from '@/lib/api';
import { apiError, fmtDayMonth, fmtG, fmtKg } from '@/lib/format';
import { useSession } from '@/lib/session';
import { colors, radius, sp } from '@/lib/theme';
import { useApi } from '@/lib/use-api';

const SEX_LABEL: Record<Sex, string> = {
  male: 'Masculino',
  female: 'Feminino',
  other: 'Outro',
};
const OBJECTIVE_LABEL: Record<Objective, string> = {
  lose_weight: 'Emagrecer',
  gain_muscle: 'Ganhar massa',
  maintain: 'Manter peso',
};

export default function ProfileScreen() {
  const { user, signOut } = useSession();
  const { data, loading, error, refreshing, refresh } = useApi(async () => {
    const [goals, weights] = await Promise.all([listGoals(), listWeights()]);
    return { goals, weights };
  });

  const [modal, setModal] = useState(false);
  const [weight, setWeight] = useState('');
  const [saving, setSaving] = useState(false);

  async function saveWeight() {
    const n = Number(weight.replace(',', '.'));
    if (!(n > 0 && n <= 500)) {
      Alert.alert('Valor inválido', 'Informe um peso entre 1 e 500 kg.');
      return;
    }
    setSaving(true);
    try {
      await createWeight(n);
      setModal(false);
      setWeight('');
      refresh();
    } catch (e) {
      Alert.alert('Erro', apiError(e));
    } finally {
      setSaving(false);
    }
  }

  function confirmLogout() {
    Alert.alert('Sair da conta?', 'Você precisará entrar novamente.', [
      { text: 'Cancelar', style: 'cancel' },
      { text: 'Sair', style: 'destructive', onPress: () => void signOut() },
    ]);
  }

  const goal = data?.goals[0];

  return (
    <ScrollView
      style={{ backgroundColor: colors.bg }}
      contentContainerStyle={{ padding: sp(4) }}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={refresh} />
      }>
      {/* Cabeçalho */}
      <View style={{ alignItems: 'center' }}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {user?.name?.[0]?.toUpperCase() ?? '?'}
          </Text>
        </View>
        <Text style={styles.name}>{user?.name}</Text>
        <Text style={styles.muted}>{user?.email}</Text>
      </View>

      {/* Dados */}
      <Card style={{ marginTop: sp(4) }}>
        <InfoRow label="Sexo" value={user?.sex ? SEX_LABEL[user.sex] : '—'} />
        <InfoRow label="Idade" value={user?.age != null ? `${user.age} anos` : '—'} />
        <InfoRow
          label="Altura"
          value={user?.height_cm != null ? `${fmtG(user.height_cm)} cm` : '—'}
          last
        />
      </Card>

      {/* Meta */}
      <Text style={styles.section}>Minha meta</Text>
      {loading ? (
        <Text style={styles.muted}>Carregando…</Text>
      ) : error ? (
        <Text style={styles.error}>{apiError(error)}</Text>
      ) : goal ? (
        <Card>
          <Text style={styles.goalTitle}>🎯 {OBJECTIVE_LABEL[goal.objective]}</Text>
          <Text style={[styles.muted, { marginTop: sp(1) }]}>
            De {fmtKg(goal.start_weight_kg)} para {fmtKg(goal.target_weight_kg)}
          </Text>
          <View style={styles.divider} />
          <Text style={{ color: colors.text }}>
            Meta diária:{' '}
            <Text style={{ fontWeight: '700' }}>{goal.daily_calorie_target} kcal</Text>
          </Text>
        </Card>
      ) : (
        <Text style={styles.muted}>Nenhuma meta definida.</Text>
      )}

      {/* Peso */}
      <View style={styles.weightHeader}>
        <Text style={styles.section}>Histórico de peso</Text>
        <Button title="+ Registrar" variant="text" onPress={() => setModal(true)} />
      </View>
      {!loading && !error && data ? (
        data.weights.length === 0 ? (
          <Text style={styles.muted}>Nenhum peso registrado ainda.</Text>
        ) : (
          <Card>
            {data.weights.slice(0, 10).map((w, i, arr) => (
              <View key={w.id}>
                <View style={styles.weightRow}>
                  <Text style={{ color: colors.text }}>⚖️ {fmtKg(w.weight_kg)}</Text>
                  <Text style={styles.muted}>{fmtDayMonth(w.recorded_at)}</Text>
                </View>
                {i < arr.length - 1 ? <View style={styles.divider} /> : null}
              </View>
            ))}
          </Card>
        )
      ) : null}

      <View style={{ height: sp(6) }} />
      <Button title="Sair da conta" variant="outline" onPress={confirmLogout} />
      <View style={{ height: sp(6) }} />

      {/* Modal de registro de peso */}
      <Modal visible={modal} transparent animationType="fade" onRequestClose={() => setModal(false)}>
        <View style={styles.modalBackdrop}>
          <View style={styles.modalCard}>
            <Text style={styles.modalTitle}>Registrar peso</Text>
            <Input
              label="Peso (kg)"
              value={weight}
              onChangeText={setWeight}
              keyboardType="decimal-pad"
              placeholder="kg"
              autoFocus
            />
            <View style={styles.row}>
              <View style={{ flex: 1 }}>
                <Button title="Cancelar" variant="text" onPress={() => setModal(false)} />
              </View>
              <View style={{ flex: 1 }}>
                <Button title="Salvar" onPress={saveWeight} loading={saving} />
              </View>
            </View>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
}

function InfoRow({
  label,
  value,
  last,
}: {
  label: string;
  value: string;
  last?: boolean;
}) {
  return (
    <View>
      <View style={styles.infoRow}>
        <Text style={styles.muted}>{label}</Text>
        <Text style={{ color: colors.text, fontSize: 15 }}>{value}</Text>
      </View>
      {!last ? <View style={styles.divider} /> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  avatar: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: colors.primaryContainer,
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarText: { fontSize: 30, fontWeight: '800', color: colors.onPrimaryContainer },
  name: { fontSize: 20, fontWeight: '800', color: colors.text, marginTop: sp(2) },
  muted: { color: colors.textMuted, fontSize: 13 },
  error: { color: colors.danger },
  section: {
    fontSize: 16,
    fontWeight: '700',
    color: colors.text,
    marginTop: sp(5),
    marginBottom: sp(2),
  },
  goalTitle: { fontSize: 16, fontWeight: '700', color: colors.text },
  divider: { height: 1, backgroundColor: colors.border, marginVertical: sp(3) },
  infoRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  weightHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  weightRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  row: { flexDirection: 'row', gap: sp(2), marginTop: sp(2) },
  modalBackdrop: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.4)',
    alignItems: 'center',
    justifyContent: 'center',
    padding: sp(6),
  },
  modalCard: {
    backgroundColor: colors.bg,
    borderRadius: radius.lg,
    padding: sp(5),
    width: '100%',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: colors.text,
    marginBottom: sp(3),
  },
});
