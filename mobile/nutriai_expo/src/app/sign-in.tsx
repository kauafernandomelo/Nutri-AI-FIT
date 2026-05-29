import { useRouter } from 'expo-router';
import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { Button, Input, Screen } from '@/components/ui';
import { apiError } from '@/lib/format';
import { useSession } from '@/lib/session';
import { colors, sp } from '@/lib/theme';

export default function SignIn() {
  const router = useRouter();
  const { signIn } = useSession();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setError(null);
    if (!email.includes('@')) {
      setError('Informe um e-mail válido.');
      return;
    }
    if (!password) {
      setError('Informe sua senha.');
      return;
    }
    setLoading(true);
    try {
      await signIn(email.trim(), password);
      // O redirect do router cuida da navegação ao mudar a sessão.
    } catch (e) {
      setError(apiError(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <Screen scroll>
      <View style={styles.header}>
        <Text style={styles.logo}>🥗</Text>
        <Text style={styles.title}>NutriAI Fit</Text>
        <Text style={styles.subtitle}>Sua refeição em números, num clique.</Text>
      </View>

      <Input
        label="E-mail"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
        autoCorrect={false}
        placeholder="voce@exemplo.com"
      />
      <Input
        label="Senha"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        placeholder="••••••••"
      />

      {error ? <Text style={styles.error}>{error}</Text> : null}

      <View style={{ height: sp(2) }} />
      <Button title="Entrar" onPress={submit} loading={loading} />
      <View style={{ height: sp(2) }} />
      <Button
        title="Não tem conta? Cadastre-se"
        variant="text"
        onPress={() => router.push('/register')}
      />
    </Screen>
  );
}

const styles = StyleSheet.create({
  header: { alignItems: 'center', marginVertical: sp(8) },
  logo: { fontSize: 56 },
  title: { fontSize: 28, fontWeight: '800', color: colors.text, marginTop: sp(2) },
  subtitle: { fontSize: 14, color: colors.textMuted, marginTop: sp(1) },
  error: { color: colors.danger, marginBottom: sp(2) },
});
