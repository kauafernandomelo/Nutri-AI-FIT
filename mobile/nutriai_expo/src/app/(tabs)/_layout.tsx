import { FontAwesome } from '@expo/vector-icons';
import { Tabs, useRouter } from 'expo-router';
import { Pressable } from 'react-native';

import { colors } from '@/lib/theme';

function HeaderCameraButton() {
  const router = useRouter();
  return (
    <Pressable
      onPress={() => router.push('/add-meal')}
      hitSlop={12}
      style={{ paddingHorizontal: 16 }}>
      <FontAwesome name="camera" size={20} color={colors.primary} />
    </Pressable>
  );
}

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: colors.primary,
        headerTitleAlign: 'center',
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Início',
          headerRight: () => <HeaderCameraButton />,
          tabBarIcon: ({ color, size }) => (
            <FontAwesome name="home" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="meals"
        options={{
          title: 'Refeições',
          tabBarIcon: ({ color, size }) => (
            <FontAwesome name="cutlery" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Perfil',
          tabBarIcon: ({ color, size }) => (
            <FontAwesome name="user" color={color} size={size} />
          ),
        }}
      />
    </Tabs>
  );
}
