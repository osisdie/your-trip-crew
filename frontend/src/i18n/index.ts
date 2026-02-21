import { create } from "zustand";
import { zh } from "./zh";
import { en } from "./en";

export type Locale = "zh" | "en";
export type TranslationKey = keyof typeof zh;
const translations: Record<Locale, Record<TranslationKey, string>> = { zh, en };

const HTML_LANG: Record<Locale, string> = { zh: "zh-Hant", en: "en" };

interface I18nState {
  locale: Locale;
  setLocale: (locale: Locale) => void;
}

export const useI18nStore = create<I18nState>((set) => ({
  locale: (localStorage.getItem("locale") as Locale) || "en",
  setLocale: (locale) => {
    localStorage.setItem("locale", locale);
    document.documentElement.lang = HTML_LANG[locale] || locale;
    set({ locale });
  },
}));

/** Returns a translation function bound to the current locale */
export function useT() {
  const locale = useI18nStore((s) => s.locale);
  return (key: TranslationKey) => translations[locale][key];
}
