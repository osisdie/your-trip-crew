import { create } from "zustand";
import type { TravelPackage, PackageDetail } from "../lib/types";
import { packageApi } from "../lib/api";

interface PackageState {
  packages: TravelPackage[];
  currentPackage: PackageDetail | null;
  categories: string[];
  destinations: string[];
  isLoading: boolean;
  filters: {
    destination?: string;
    category?: string;
    min_price?: number;
    max_price?: number;
  };
  setFilter: (key: string, value: string | number | undefined) => void;
  fetchPackages: () => Promise<void>;
  fetchPackageBySlug: (slug: string) => Promise<void>;
  fetchCategories: () => Promise<void>;
  fetchDestinations: () => Promise<void>;
}

export const usePackageStore = create<PackageState>((set, get) => ({
  packages: [],
  currentPackage: null,
  categories: [],
  destinations: [],
  isLoading: false,
  filters: {},

  setFilter: (key, value) => {
    set((s) => ({ filters: { ...s.filters, [key]: value } }));
  },

  fetchPackages: async () => {
    set({ isLoading: true });
    try {
      const params: Record<string, string | number> = {};
      const { filters } = get();
      if (filters.destination) params.destination = filters.destination;
      if (filters.category) params.category = filters.category;
      if (filters.min_price) params.min_price = filters.min_price;
      if (filters.max_price) params.max_price = filters.max_price;

      const { data } = await packageApi.list(params);
      set({ packages: data, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  fetchPackageBySlug: async (slug) => {
    set({ isLoading: true });
    try {
      const { data } = await packageApi.getBySlug(slug);
      set({ currentPackage: data, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  fetchCategories: async () => {
    const { data } = await packageApi.getCategories();
    set({ categories: data });
  },

  fetchDestinations: async () => {
    const { data } = await packageApi.getDestinations();
    set({ destinations: data });
  },
}));
