import axios from "axios";
import { API_BASE_URL, STORAGE_KEYS } from "./constants";
import type {
  ChatMessage,
  ChatMessageList,
  ChatSession,
  Itinerary,
  ItineraryDetail,
  PackageDetail,
  TokenResponse,
  TravelPackage,
  UsageInfo,
  User,
} from "./types";

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto-refresh on 401
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
      if (refreshToken) {
        try {
          const { data } = await axios.post<TokenResponse>(
            `${API_BASE_URL}/api/v1/auth/refresh`,
            { refresh_token: refreshToken }
          );
          localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, data.access_token);
          localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, data.refresh_token);
          original.headers.Authorization = `Bearer ${data.access_token}`;
          return api(original);
        } catch {
          localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
          localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

// ─── Auth ────────────────────────────────────────
export const authApi = {
  refresh: (refreshToken: string) =>
    api.post<TokenResponse>("/auth/refresh", { refresh_token: refreshToken }),
};

// ─── Users ───────────────────────────────────────
export const userApi = {
  getMe: () => api.get<User>("/users/me"),
  updateMe: (data: Partial<User>) => api.patch<User>("/users/me", data),
  getUsage: () => api.get<UsageInfo>("/users/me/usage"),
};

// ─── Chat ────────────────────────────────────────
export const chatApi = {
  createSession: (title?: string) =>
    api.post<ChatSession>("/chat/sessions", { title }),
  listSessions: () => api.get<ChatSession[]>("/chat/sessions"),
  getSession: (id: string) => api.get<ChatSession>(`/chat/sessions/${id}`),
  deleteSession: (id: string) => api.delete(`/chat/sessions/${id}`),
  getMessages: (sessionId: string, limit = 50, offset = 0) =>
    api.get<ChatMessageList>(
      `/chat/sessions/${sessionId}/messages?limit=${limit}&offset=${offset}`
    ),
  sendMessage: (sessionId: string, content: string) =>
    api.post<ChatMessage>(`/chat/sessions/${sessionId}/messages`, { content }),
};

// ─── Packages ────────────────────────────────────
/** Get the current locale from localStorage (set by i18n store). */
function getLocale(): string {
  return localStorage.getItem("locale") || "zh";
}

export const packageApi = {
  list: (params?: Record<string, string | number>) =>
    api.get<TravelPackage[]>("/packages", {
      params: { ...params, locale: getLocale() },
    }),
  getBySlug: (slug: string) =>
    api.get<PackageDetail>(`/packages/${slug}`, {
      params: { locale: getLocale() },
    }),
  getCategories: () => api.get<string[]>("/packages/categories"),
  getDestinations: () => api.get<string[]>("/packages/destinations"),
  semanticSearch: (q: string, limit = 10) =>
    api.get("/packages/search/semantic", { params: { q, limit } }),
};

// ─── Itineraries ─────────────────────────────────
export const itineraryApi = {
  list: () => api.get<Itinerary[]>("/itineraries"),
  get: (id: string) => api.get<ItineraryDetail>(`/itineraries/${id}`),
  update: (id: string, data: Partial<Itinerary>) =>
    api.patch<Itinerary>(`/itineraries/${id}`, data),
  delete: (id: string) => api.delete(`/itineraries/${id}`),
};

export default api;
