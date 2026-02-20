// ─── User ──────────────────────────────────────────
export interface User {
  id: string;
  email: string;
  display_name: string;
  avatar_url: string | null;
  tier: "free" | "premium";
  is_active: boolean;
  created_at: string;
}

export interface UsageInfo {
  date: string;
  query_count: number;
  daily_limit: number;
  remaining: number;
}

// ─── Auth ──────────────────────────────────────────
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// ─── Chat ──────────────────────────────────────────
export interface ChatSession {
  id: string;
  title: string;
  is_active: boolean;
  intent_slots: IntentSlots | null;
  created_at: string;
  updated_at: string;
}

export interface IntentSlots {
  destination?: string;
  start_date?: string;
  end_date?: string;
  duration_days?: number;
  num_travelers?: number;
  children_ages?: number[];
  budget_usd?: number;
  preferences?: string[];
  trip_style?: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: "user" | "assistant" | "system";
  content: string;
  metadata_?: Record<string, unknown>;
  created_at: string;
}

export interface ChatMessageList {
  messages: ChatMessage[];
  total: number;
  has_more: boolean;
}

// ─── Packages ──────────────────────────────────────
export interface TravelPackage {
  id: string;
  title: string;
  slug: string;
  destination: string;
  category: string;
  summary: string;
  duration_days: number;
  price_usd: number;
  cover_image_url: string | null;
  highlights: string[] | null;
}

export interface PackageDay {
  id: string;
  day_number: number;
  title: string;
  description: string;
  activities: Record<string, unknown>[] | null;
}

export interface PackageTag {
  id: string;
  tag: string;
}

export interface PackageDetail extends TravelPackage {
  description: string;
  is_published: boolean;
  created_at: string;
  days: PackageDay[];
  tags: PackageTag[];
}

// ─── Itineraries ───────────────────────────────────
export interface ItineraryItem {
  id: string;
  order: number;
  time_start: string | null;
  time_end: string | null;
  category: string;
  title: string;
  description: string | null;
  location: string | null;
  lat: number | null;
  lng: number | null;
  cost_usd: number | null;
  booking_url: string | null;
  notes: string | null;
}

export interface ItineraryDay {
  id: string;
  day_number: number;
  date: string | null;
  city: string;
  theme: string | null;
  items: ItineraryItem[];
}

export interface Itinerary {
  id: string;
  title: string;
  destination: string;
  start_date: string | null;
  end_date: string | null;
  duration_days: number;
  num_travelers: number;
  total_cost_usd: number | null;
  status: "draft" | "confirmed";
  created_at: string;
}

export interface ItineraryDetail extends Itinerary {
  session_id: string | null;
  cost_breakdown: Record<string, number> | null;
  days: ItineraryDay[];
}

// ─── WebSocket ─────────────────────────────────────
export interface WsMessage {
  type: "message" | "typing" | "error" | "slots_update";
  content: string;
  slots?: IntentSlots;
}
