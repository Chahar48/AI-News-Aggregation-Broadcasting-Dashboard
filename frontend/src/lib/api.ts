// frontend/src/lib/api.ts

import axios from "axios";

// ---------------------------------------------------------
// Base API Configuration
// ---------------------------------------------------------
const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE,
});

// ---------------------------------------------------------
// News Endpoints
// ---------------------------------------------------------
export async function fetchNews(page = 1, limit = 20) {
  const res = await api.get(`/news`, {
    params: { page, limit },
  });
  return res.data;
}

export async function refreshNews() {
  const res = await api.post(`/news/refresh`);
  return res.data;
}

// ---------------------------------------------------------
// Favorites Endpoints
// ---------------------------------------------------------
export async function fetchFavorites() {
  const res = await api.get(`/favorites`);
  return res.data;
}

export async function markFavorite(newsItemId: number) {
  const res = await api.post(`/favorites`, {
    news_item_id: newsItemId,
  });
  return res.data;
}

export async function removeFavorite(favoriteId: number) {
  const res = await api.delete(`/favorites/${favoriteId}`);
  return res.data;
}

// ---------------------------------------------------------
// Broadcast Endpoints
// ---------------------------------------------------------
export async function broadcastAction(
  favoriteId: number,
  platform: string,
  messageOverride?: string
) {
  const res = await api.post(`/broadcast`, {
    favorite_id: favoriteId,
    platform,
    message_override: messageOverride || null,
  });

  return res.data;
}

export async function getBroadcastLogs() {
  const res = await api.get(`/broadcast/logs`);
  return res.data;
}
