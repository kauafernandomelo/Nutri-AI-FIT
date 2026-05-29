import { useRouter } from 'expo-router';
import { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { Button, Input, Screen } from '@/components/ui';
import { apiError } from '@/lib/format';
import { useSession } from '@/lib/session';
import { colors, sp } from '@/lib/theme';

export default function Register() {
  const router = useRouter();
  const { signUp } = useSession();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setError(null);
    if (name.trim().length < 2) {
      setError('Informe seu nome.');
      return;
    }
    if (!email.includes('@')) {
      setError('Informe um e-mail válido.');
      return;
    }
    if (password.length < 8) {
      setError('A senha precisa de pelo menos 8 caracteres.');
      return;
    }
    setLoading(true);
    try {
      // signUp já faz login em seguida; o redirect leva ao onboarding.
      await signUp(name.trim(), email.trim(), password);
    } catch (e) {
      setError(apiError(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <Screen scroll>
      <Input
        label="Nome"
        value={name}
        onChangeText={setName}
        autoCapitalize="words"
        placeholder="Seu nome"
      />
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
        label="Senha (mín. 8 caracteres)"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        placeholder="••••••••"
      />

      {error ? <Text style={styles.error}>{error}</Text> : null}

      <View style={{ height: sp(2) }} />
      <Button title="Cadastrar" onPress={submit} loading={loading} />
      <View style={{ height: sp(2) }} />
      <Button
        title="Já tenho conta"
        variant="text"
        onPress={() => router.back()}
      />
    </Screen>
  );
}

const styles = StyleSheet.create({
  error: { color: colors.danger, marginBottom: sp(2) },
});
