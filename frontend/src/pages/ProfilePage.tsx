import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuthStore } from "../stores/authStore";
import { userApi, itineraryApi } from "../lib/api";
import type { UsageInfo, Itinerary } from "../lib/types";
import { useT } from "../i18n";

export function ProfilePage() {
  const { user } = useAuthStore();
  const t = useT();
  const [usage, setUsage] = useState<UsageInfo | null>(null);
  const [itineraries, setItineraries] = useState<Itinerary[]>([]);

  useEffect(() => {
    userApi.getUsage().then(({ data }) => setUsage(data)).catch(() => {});
    itineraryApi.list().then(({ data }) => setItineraries(data)).catch(() => {});
  }, []);

  if (!user) return null;

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-bold text-gray-900">{t("profile.title")}</h1>

      {/* User info */}
      <div className="card mt-6 p-6">
        <div className="flex items-center gap-4">
          {user.avatar_url ? (
            <img src={user.avatar_url} alt="" className="h-16 w-16 rounded-full" />
          ) : (
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary-100 text-2xl font-bold text-primary-700">
              {user.display_name[0]}
            </div>
          )}
          <div>
            <h2 className="text-xl font-semibold text-gray-900">{user.display_name}</h2>
            <p className="text-sm text-gray-500">{user.email}</p>
            <span
              className={`mt-1 inline-block rounded-full px-2 py-0.5 text-xs font-medium ${
                user.tier === "premium"
                  ? "bg-amber-100 text-amber-700"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              {user.tier} {t("profile.tier")}
            </span>
          </div>
        </div>
      </div>

      {/* Usage */}
      {usage && (
        <div className="card mt-6 p-6">
          <h3 className="font-semibold text-gray-900">{t("profile.todayUsage")}</h3>
          <div className="mt-4 flex items-center gap-8">
            <div>
              <p className="text-3xl font-bold text-primary-600">{usage.query_count}</p>
              <p className="text-sm text-gray-500">{t("profile.queriesUsed")}</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-gray-300">{usage.remaining}</p>
              <p className="text-sm text-gray-500">{t("profile.remaining")}</p>
            </div>
            <div>
              <p className="text-3xl font-bold text-gray-300">{usage.daily_limit}</p>
              <p className="text-sm text-gray-500">{t("profile.dailyLimit")}</p>
            </div>
          </div>
          <div className="mt-3 h-3 w-full overflow-hidden rounded-full bg-gray-100">
            <div
              className="h-full rounded-full bg-primary-500 transition-all"
              style={{
                width: `${(usage.query_count / usage.daily_limit) * 100}%`,
              }}
            />
          </div>
          {user.tier === "free" && (
            <p className="mt-3 text-sm text-gray-400">
              {t("profile.upgrade")}
            </p>
          )}
        </div>
      )}

      {/* Itineraries */}
      <div className="card mt-6 p-6">
        <h3 className="font-semibold text-gray-900">{t("profile.myItineraries")}</h3>
        {itineraries.length === 0 ? (
          <p className="mt-4 text-sm text-gray-400">
            {t("profile.noItineraries")}{" "}
            <Link to="/chat" className="text-primary-600 hover:underline">
              {t("profile.startPlanning")}
            </Link>
          </p>
        ) : (
          <ul className="mt-4 divide-y divide-gray-100">
            {itineraries.map((it) => (
              <li key={it.id} className="py-3">
                <Link
                  to={`/itinerary/${it.id}`}
                  className="flex items-center justify-between hover:text-primary-600"
                >
                  <div>
                    <p className="font-medium text-gray-900">{it.title}</p>
                    <p className="text-sm text-gray-500">
                      {it.destination} · {it.duration_days} {t("common.days")}
                    </p>
                  </div>
                  {it.total_cost_usd && (
                    <span className="text-sm font-medium text-gray-600">
                      ${it.total_cost_usd.toLocaleString()}
                    </span>
                  )}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
