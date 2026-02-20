import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { packageApi } from "../lib/api";
import type { PackageDetail, PackageTag, PackageDay } from "../lib/types";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { useT, useI18nStore } from "../i18n";

export function PackageDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const t = useT();
  const locale = useI18nStore((s) => s.locale);
  const [pkg, setPkg] = useState<PackageDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!slug) return;
    setIsLoading(true);
    packageApi
      .getBySlug(slug)
      .then((res) => setPkg(res.data))
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, [slug, locale]);

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!pkg) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center text-gray-500">
        {t("pkgDetail.notFound")}
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      <Link to="/packages" className="text-sm text-primary-600 hover:text-primary-700">
        {t("pkgDetail.back")}
      </Link>

      <div className="mt-4">
        {pkg.cover_image_url && (
          <img
            src={pkg.cover_image_url}
            alt={pkg.title}
            className="h-64 w-full rounded-xl object-cover"
          />
        )}

        <div className="mt-6">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-primary-50 px-3 py-1 text-sm font-medium text-primary-700">
              {pkg.destination}
            </span>
            <span className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-600">
              {pkg.category}
            </span>
            {pkg.tags.map((tag: PackageTag) => (
              <span
                key={tag.id}
                className="rounded-full bg-gray-50 px-2 py-0.5 text-xs text-gray-500"
              >
                #{tag.tag}
              </span>
            ))}
          </div>

          <h1 className="mt-4 text-3xl font-bold text-gray-900">{pkg.title}</h1>
          <p className="mt-2 text-gray-600">{pkg.summary}</p>

          <div className="mt-4 flex items-center gap-6">
            <div>
              <span className="text-2xl font-bold text-primary-600">
                ${pkg.price_usd.toLocaleString()}
              </span>
              <span className="text-sm text-gray-400"> {t("pkgDetail.perPerson")}</span>
            </div>
            <div className="text-sm text-gray-500">
              {pkg.duration_days} {t("pkgDetail.days")}
            </div>
          </div>

          {pkg.highlights && pkg.highlights.length > 0 && (
            <div className="mt-6">
              <h3 className="font-semibold text-gray-900">{t("pkgDetail.highlights")}</h3>
              <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-gray-600">
                {pkg.highlights.map((h: string, i: number) => (
                  <li key={i}>{h}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="mt-6">
            <p className="text-gray-700 whitespace-pre-line">{pkg.description}</p>
          </div>
        </div>

        {/* Day-by-day */}
        {pkg.days.length > 0 && (
          <div className="mt-10">
            <h2 className="text-2xl font-bold text-gray-900">{t("pkgDetail.dayByDay")}</h2>
            <div className="mt-6 space-y-6">
              {pkg.days
                .sort((a: PackageDay, b: PackageDay) => a.day_number - b.day_number)
                .map((day: PackageDay) => (
                  <div key={day.id} className="card p-6">
                    <h3 className="font-semibold text-gray-900">
                      {t("pkgDetail.day")} {day.day_number}: {day.title}
                    </h3>
                    <p className="mt-2 text-sm text-gray-600">{day.description}</p>
                    {day.activities && day.activities.length > 0 && (
                      <ul className="mt-3 space-y-2">
                        {day.activities.map((act: Record<string, unknown>, i: number) => (
                          <li
                            key={i}
                            className="flex items-start gap-2 text-sm text-gray-500"
                          >
                            <span className="mt-0.5 text-primary-400">•</span>
                            {typeof act === "string" ? act : JSON.stringify(act)}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
