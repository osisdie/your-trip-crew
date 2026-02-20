import { useT } from "../../i18n";
import type { TranslationKey } from "../../i18n";

interface CostBreakdownProps {
  breakdown: Record<string, number>;
}

const CATEGORY_KEYS: Record<string, TranslationKey> = {
  flights: "cost.flights",
  hotels: "cost.hotels",
  activities: "cost.activities",
  transport: "cost.transport",
  meals: "cost.meals",
  esim: "cost.esim",
  misc: "cost.misc",
};

export function CostBreakdown({ breakdown }: CostBreakdownProps) {
  const t = useT();
  const total = Object.values(breakdown).reduce((sum, v) => sum + v, 0);

  return (
    <div className="mt-6 card p-6">
      <h3 className="font-semibold text-gray-900">{t("itinerary.costBreakdown")}</h3>
      <div className="mt-4 space-y-3">
        {Object.entries(breakdown).map(([key, value]) => {
          const pct = total > 0 ? (value / total) * 100 : 0;
          return (
            <div key={key}>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">
                  {CATEGORY_KEYS[key] ? t(CATEGORY_KEYS[key]) : key}
                </span>
                <span className="font-medium text-gray-900">
                  ${value.toLocaleString()}
                </span>
              </div>
              <div className="mt-1 h-2 w-full overflow-hidden rounded-full bg-gray-100">
                <div
                  className="h-full rounded-full bg-primary-500"
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
