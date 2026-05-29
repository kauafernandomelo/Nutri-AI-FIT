import { type ReactNode } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  type TextInputProps,
  View,
  type ViewStyle,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { colors, radius, sp } from '@/lib/theme';

// ---------------------------------------------------------------- Screen -----
export function Screen({
  children,
  scroll = false,
  padded = true,
}: {
  children: ReactNode;
  scroll?: boolean;
  padded?: boolean;
}) {
  const inner = (
    <View style={[{ flex: scroll ? 0 : 1 }, padded && { padding: sp(4) }]}>
      {children}
    </View>
  );
  return (
    <SafeAreaView style={styles.screen} edges={['top', 'left', 'right']}>
      {scroll ? (
        <ScrollView
          contentContainerStyle={padded ? { padding: sp(4) } : undefined}
          keyboardShouldPersistTaps="handled">
          {children}
        </ScrollView>
      ) : (
        inner
      )}
    </SafeAreaView>
  );
}

// ---------------------------------------------------------------- Button -----
export function Button({
  title,
  onPress,
  loading = false,
  disabled = false,
  variant = 'filled',
}: {
  title: string;
  onPress: () => void;
  loading?: boolean;
  disabled?: boolean;
  variant?: 'filled' | 'outline' | 'text';
}) {
  const isDisabled = disabled || loading;
  const base: ViewStyle[] = [styles.btn];
  if (variant === 'filled') base.push(styles.btnFilled);
  if (variant === 'outline') base.push(styles.btnOutline);
  if (isDisabled) base.push(styles.btnDisabled);

  const textColor =
    variant === 'filled' ? colors.white : colors.primaryDark;

  return (
    <Pressable
      onPress={onPress}
      disabled={isDisabled}
      style={({ pressed }) => [...base, pressed && !isDisabled && { opacity: 0.85 }]}>
      {loading ? (
        <ActivityIndicator color={textColor} />
      ) : (
        <Text style={[styles.btnText, { color: textColor }]}>{title}</Text>
      )}
    </Pressable>
  );
}

// ---------------------------------------------------------------- Input ------
export function Input({
  label,
  error,
  ...props
}: TextInputProps & { label?: string; error?: string }) {
  return (
    <View style={{ marginBottom: sp(3) }}>
      {label ? <Text style={styles.label}>{label}</Text> : null}
      <TextInput
        placeholderTextColor={colors.textMuted}
        style={[styles.input, error ? { borderColor: colors.danger } : null]}
        {...props}
      />
      {error ? <Text style={styles.errorText}>{error}</Text> : null}
    </View>
  );
}

// ---------------------------------------------------------------- Card -------
export function Card({
  children,
  style,
}: {
  children: ReactNode;
  style?: ViewStyle;
}) {
  return <View style={[styles.card, style]}>{children}</View>;
}

// ---------------------------------------------------------------- States -----
export function Loading() {
  return (
    <View style={styles.center}>
      <ActivityIndicator size="large" color={colors.primary} />
    </View>
  );
}

export function ErrorView({
  message,
  onRetry,
}: {
  message: string;
  onRetry?: () => void;
}) {
  return (
    <View style={styles.center}>
      <Text style={styles.errorBig}>{message}</Text>
      {onRetry ? (
        <View style={{ marginTop: sp(4), alignSelf: 'stretch' }}>
          <Button title="Tentar de novo" variant="outline" onPress={onRetry} />
        </View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  center: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: sp(6),
  },
  btn: {
    minHeight: 52,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: sp(4),
  },
  btnFilled: { backgroundColor: colors.primary },
  btnOutline: { borderWidth: 1.5, borderColor: colors.primary },
  btnDisabled: { opacity: 0.5 },
  btnText: { fontSize: 16, fontWeight: '600' },
  label: { fontSize: 13, color: colors.textMuted, marginBottom: sp(1) },
  input: {
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.md,
    paddingHorizontal: sp(3.5),
    paddingVertical: sp(3),
    fontSize: 16,
    color: colors.text,
  },
  errorText: { color: colors.danger, fontSize: 12, marginTop: sp(1) },
  errorBig: { color: colors.text, fontSize: 15, textAlign: 'center' },
  card: {
    backgroundColor: colors.surface,
    borderRadius: radius.lg,
    padding: sp(4),
    borderWidth: 1,
    borderColor: colors.border,
  },
});
