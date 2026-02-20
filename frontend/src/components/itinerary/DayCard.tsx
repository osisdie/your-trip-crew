import type { ItineraryDay } from "../../lib/types";

const CATEGORY_COLORS: Record<string, string> = {
  transport: "bg-blue-100 text-blue-700",
  meal: "bg-orange-100 text-orange-700",
  activity: "bg-green-100 text-green-700",
  hotel: "bg-purple-100 text-purple-700",
  shopping: "bg-pink-100 text-pink-700",
};

export function DayCard({ day }: { day: ItineraryDay }) {
  const sortedItems = [...day.items].sort((a, b) => a.order - b.order);

  return (
    <div className="card overflow-hidden">
      <div className="bg-primary-50 px-6 py-3">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-primary-900">
            Day {day.day_number}
            {day.theme && ` — ${day.theme}`}
          </h3>
          <div className="flex items-center gap-2 text-sm text-primary-600">
            <span>{day.city}</span>
            {day.date && <span>· {day.date}</span>}
          </div>
        </div>
      </div>

      <div className="divide-y divide-gray-100">
        {sortedItems.map((item) => (
          <div key={item.id} className="flex gap-4 px-6 py-4">
            <div className="w-20 flex-shrink-0 text-sm text-gray-400">
              {item.time_start && (
                <>
                  {item.time_start}
                  {item.time_end && ` - ${item.time_end}`}
                </>
              )}
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <span
                  className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                    CATEGORY_COLORS[item.category] || "bg-gray-100 text-gray-600"
                  }`}
                >
                  {item.category}
                </span>
                <span className="font-medium text-gray-900">{item.title}</span>
              </div>
              {item.description && (
                <p className="mt-1 text-sm text-gray-500">{item.description}</p>
              )}
              {item.location && (
                <p className="mt-1 text-xs text-gray-400">📍 {item.location}</p>
              )}
              {item.notes && (
                <p className="mt-1 text-xs italic text-gray-400">{item.notes}</p>
              )}
            </div>
            <div className="flex-shrink-0 text-right">
              {item.cost_usd != null && (
                <span className="text-sm font-medium text-gray-700">
                  ${item.cost_usd}
                </span>
              )}
              {item.booking_url && (
                <a
                  href={item.booking_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-1 block text-xs text-primary-600 hover:underline"
                >
                  Book →
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
