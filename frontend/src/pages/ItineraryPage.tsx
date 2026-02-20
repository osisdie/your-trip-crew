import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { itineraryApi } from "../lib/api";
import type { ItineraryDetail } from "../lib/types";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { ItineraryTimeline } from "../components/itinerary/ItineraryTimeline";
import { CostBreakdown } from "../components/itinerary/CostBreakdown";
import { useT } from "../i18n";

export function ItineraryPage() {
  const { id } = useParams<{ id: string }>();
  const t = useT();
  const [itinerary, setItinerary] = useState<ItineraryDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    itineraryApi
      .get(id)
      .then(({ data }) => setItinerary(data))
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, [id]);

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!itinerary) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center text-gray-500">
        {t("itinerary.notFound")}
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <Link to="/itineraries" className="text-sm text-primary-600 hover:text-primary-700">
        {t("itinerary.back")}
      </Link>

      <div className="mt-4">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{itinerary.title}</h1>
            <p className="mt-1 text-gray-500">
              {itinerary.destination} · {itinerary.duration_days} {t("common.days")} ·{" "}
              {itinerary.num_travelers} {t("itinerary.travelers")}
            </p>
            {itinerary.start_date && itinerary.end_date && (
              <p className="text-sm text-gray-400">
                {itinerary.start_date} → {itinerary.end_date}
              </p>
            )}
          </div>
          <span
            className={`rounded-full px-3 py-1 text-sm font-medium ${
              itinerary.status === "confirmed"
                ? "bg-green-100 text-green-700"
                : "bg-amber-100 text-amber-700"
            }`}
          >
            {itinerary.status}
          </span>
        </div>

        {itinerary.total_cost_usd && (
          <div className="mt-4 text-2xl font-bold text-primary-600">
            {t("itinerary.total")}: ${itinerary.total_cost_usd.toLocaleString()}
          </div>
        )}

        {itinerary.cost_breakdown && (
          <CostBreakdown breakdown={itinerary.cost_breakdown} />
        )}

        <ItineraryTimeline days={itinerary.days} />
      </div>
    </div>
  );
}
