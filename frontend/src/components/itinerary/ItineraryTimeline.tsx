import type { ItineraryDay } from "../../lib/types";
import { DayCard } from "./DayCard";
import { useT } from "../../i18n";

interface ItineraryTimelineProps {
  days: ItineraryDay[];
}

export function ItineraryTimeline({ days }: ItineraryTimelineProps) {
  const t = useT();
  const sortedDays = [...days].sort((a, b) => a.day_number - b.day_number);

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold text-gray-900">{t("itinerary.dayByDay")}</h2>
      <div className="mt-6 space-y-6">
        {sortedDays.map((day) => (
          <DayCard key={day.id} day={day} />
        ))}
      </div>
    </div>
  );
}
