import { create } from "zustand";
import { STORAGE_KEYS } from "../lib/constants";
import type { User } from "../lib/types";
import { userApi } from "../lib/api";

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  setTokens: (accessToken: string, refreshToken: string) => void;
  fetchUser: () => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  isAuthenticated: false,

  setTokens: (accessToken, refreshToken) => {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, accessToken);
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refreshToken);
    set({ isAuthenticated: true });
  },

  fetchUser: async () => {
    const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    if (!token) {
      set({ user: null, isLoading: false, isAuthenticated: false });
      return;
    }
    try {
      const { data } = await userApi.getMe();
      set({ user: data, isLoading: false, isAuthenticated: true });
    } catch {
      set({ user: null, isLoading: false, isAuthenticated: false });
    }
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    set({ user: null, isAuthenticated: false });
  },
}));
