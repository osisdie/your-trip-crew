import { useRef, useState, useEffect } from "react";
import { useI18nStore, type Locale } from "../../i18n";

const LOCALE_OPTIONS: { value: Locale; label: string }[] = [
  { value: "zh", label: "繁體中文" },
  { value: "en", label: "English" },
];

export function LanguageToggle() {
  const { locale, setLocale } = useI18nStore();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // Close on click outside
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const current = LOCALE_OPTIONS.find((o) => o.value === locale)!;

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 rounded-full border border-gray-200 px-3 py-1 text-xs font-medium text-gray-600 transition hover:bg-gray-100"
      >
        <svg
          className="h-4 w-4"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="10" />
          <path d="M2 12h20" />
          <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
        </svg>
        {current.label}
        <svg className={`h-3 w-3 transition ${open ? "rotate-180" : ""}`} viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clipRule="evenodd" />
        </svg>
      </button>

      {open && (
        <div className="absolute right-0 z-50 mt-1 min-w-[120px] rounded-lg border border-gray-200 bg-white py-1 shadow-lg">
          {LOCALE_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => { setLocale(opt.value); setOpen(false); }}
              className={`flex w-full items-center gap-2 px-3 py-1.5 text-left text-sm transition hover:bg-gray-50 ${
                opt.value === locale ? "font-semibold text-primary-600" : "text-gray-700"
              }`}
            >
              {opt.value === locale && (
                <svg className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
              {opt.value !== locale && <span className="inline-block w-3.5" />}
              {opt.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
