import { Image, type ImageStyle } from 'expo-image';

import { currentToken, mealImageUrl } from '@/lib/api';

/// Foto da refeição.
///
/// A imagem vem de um endpoint AUTENTICADO (só o dono acessa), então anexamos o
/// token JWT no header. A URL é montada a partir do AppConfig (mesmo host das
/// outras chamadas), não do `image_url` do backend — assim funciona em qualquer
/// rede (Expo Go acessa o PC pelo IP da LAN).
export function MealImage({
  mealId,
  style,
}: {
  mealId: number;
  style?: ImageStyle;
}) {
  const token = currentToken();
  return (
    <Image
      source={{
        uri: mealImageUrl(mealId),
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      }}
      style={style}
      contentFit="cover"
      transition={150}
    />
  );
}
