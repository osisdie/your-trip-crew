export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8200";

export const WS_BASE_URL =
  import.meta.env.VITE_WS_BASE_URL || "ws://localhost:8200";

export const DESTINATIONS = ["Japan", "Taiwan"] as const;

export const CATEGORIES = [
  "Adventure",
  "Culture",
  "Family",
  "Food & Drink",
  "Nature",
  "Relaxation",
  "Skiing",
  "Urban",
] as const;

export const STORAGE_KEYS = {
  ACCESS_TOKEN: "trip_access_token",
  REFRESH_TOKEN: "trip_refresh_token",
} as const;
