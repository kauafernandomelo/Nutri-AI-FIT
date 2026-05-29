import axios from 'axios';
import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';

import { API_V1 } from './config';

const TOKEN_KEY = 'access_token';

// ============================ Tipos (espelham os schemas do backend) =========
export type Sex = 'male' | 'female' | 'other';
export type Objective = 'lose_weight' | 'gain_muscle' | 'maintain';
export type ActivityLevel =
  | 'sedentary'
  | 'light'
  | 'moderate'
  | 'active'
  | 'very_active';

export interface User {
  id: number;
  name: string;
  email: string;
  sex: Sex | null;
  age: number | null;
  height_cm: number | null;
  is_active: boolean;
}

export interface Goal {
  id: number;
  objective: Objective;
  start_weight_kg: number;
  target_weight_kg: number;
  activity_level: ActivityLevel;
  daily_calorie_target: number;
  is_active: boolean;
}

export interface Weight {
  id: number;
  weight_kg: number;
  recorded_at: string;
}

export interface MealItem {
  name: string;
  quantity: string | null;
  calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
}

export interface Meal {
  id: number;
  name: string;
  description: string | null;
  calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
  items: MealItem[] | null;
  image_url: string | null;
  ai_provider: string | null;
  consumed_at: string;
}

export interface Dashboard {
  date: string;
  calories_consumed: number;
  daily_calorie_target: number | null;
  calories_remaining: number | null;
  macros_today: { protein_g: number; carbs_g: number; fat_g: number };
  meals_today: number;
  current_streak: number;
  longest_streak: number;
  current_weight_kg: number | null;
  target_weight_kg: number | null;
  objective: Objective | null;
  motivational_message: string;
}

// ============================ Token (SecureStore + cache em memória) =========
let authToken: string | null = null;
let onUnauthorized: (() => void) | null = null;

export function setUnauthorizedHandler(cb: () => void): void {
  onUnauthorized = cb;
}

export function currentToken(): string | null {
  return authToken;
}

// No Expo Go (iOS/Android) o token vive no SecureStore (armazenamento seguro do
// SO). No WEB esse módulo é nativo-only — seu shim é um objeto vazio, então
// chamar SecureStore.getItemAsync lançava TypeError logo no boot e o app travava
// na splash. Por isso, no web caímos no localStorage. Mesma API nos dois lados.
const isWeb = Platform.OS === 'web';

async function readToken(): Promise<string | null> {
  if (isWeb) return globalThis.localStorage?.getItem(TOKEN_KEY) ?? null;
  return SecureStore.getItemAsync(TOKEN_KEY);
}

async function writeToken(token: string): Promise<void> {
  if (isWeb) {
    globalThis.localStorage?.setItem(TOKEN_KEY, token);
    return;
  }
  await SecureStore.setItemAsync(TOKEN_KEY, token);
}

async function removeToken(): Promise<void> {
  if (isWeb) {
    globalThis.localStorage?.removeItem(TOKEN_KEY);
    return;
  }
  await SecureStore.deleteItemAsync(TOKEN_KEY);
}

export async function loadToken(): Promise<string | null> {
  authToken = await readToken();
  return authToken;
}

async function saveToken(token: string): Promise<void> {
  authToken = token;
  await writeToken(token);
}

export async function clearToken(): Promise<void> {
  authToken = null;
  await removeToken();
}

// ============================ Cliente axios ==================================
export const api = axios.create({ baseURL: API_V1, timeout: 30000 });

api.interceptors.request.use((config) => {
  if (authToken) {
    config.headers.Authorization = `Bearer ${authToken}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Token expirado/inválido → limpa e avisa o SessionProvider (volta ao login).
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      await clearToken();
      onUnauthorized?.();
    }
    return Promise.reject(error);
  },
);

// ============================ Endpoints ======================================
export async function register(
  name: string,
  email: string,
  password: string,
): Promise<User> {
  const { data } = await api.post<User>('/auth/register', {
    name,
    email,
    password,
  });
  return data;
}

/** Login no formato OAuth2 (campo "username" carrega o e-mail). */
export async function login(email: string, password: string): Promise<void> {
  const body = new URLSearchParams({ username: email, password });
  const { data } = await api.post<{ access_token: string }>(
    '/auth/login',
    body.toString(),
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } },
  );
  await saveToken(data.access_token);
}

export async function getMe(): Promise<User> {
  const { data } = await api.get<User>('/users/me');
  return data;
}

export async function updateProfile(body: {
  name?: string;
  sex?: Sex;
  age?: number;
  height_cm?: number;
}): Promise<User> {
  const { data } = await api.patch<User>('/users/me', body);
  return data;
}

export async function createGoal(body: {
  objective: Objective;
  start_weight_kg: number;
  target_weight_kg: number;
  activity_level: ActivityLevel;
}): Promise<Goal> {
  const { data } = await api.post<Goal>('/goals', body);
  return data;
}

export async function listGoals(): Promise<Goal[]> {
  const { data } = await api.get<Goal[]>('/goals');
  return data;
}

export async function createWeight(weight_kg: number): Promise<Weight> {
  const { data } = await api.post<Weight>('/weights', { weight_kg });
  return data;
}

export async function listWeights(): Promise<Weight[]> {
  const { data } = await api.get<Weight[]>('/weights');
  return data;
}

export async function getDashboard(): Promise<Dashboard> {
  const { data } = await api.get<Dashboard>('/dashboard');
  return data;
}

export async function listMeals(): Promise<Meal[]> {
  const { data } = await api.get<Meal[]>('/meals', {
    params: { limit: 50, offset: 0 },
  });
  return data;
}

/** Envia a foto (multipart) para análise da IA e salva a refeição. */
export async function createMeal(uri: string): Promise<Meal> {
  const ext = uri.split('.').pop()?.toLowerCase() ?? 'jpg';
  const type =
    ext === 'png' ? 'image/png' : ext === 'webp' ? 'image/webp' : 'image/jpeg';
  const form = new FormData();
  // O React Native aceita este "arquivo" (uri/name/type) no FormData.
  form.append('file', { uri, name: `meal.${ext}`, type } as unknown as Blob);
  const { data } = await api.post<Meal>('/meals', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

/**
 * URL autenticada da imagem da refeição. Montada a partir do AppConfig (mesmo
 * host das outras chamadas), não do `image_url` que o backend devolve — assim
 * funciona em qualquer rede. Use junto com o header Authorization (ver MealImage).
 */
export function mealImageUrl(mealId: number): string {
  return `${API_V1}/meals/${mealId}/image`;
}
