import { useEffect, useState } from "react";
import { packageApi } from "../lib/api";
import type { TravelPackage } from "../lib/types";
import { PackageGrid } from "../components/packages/PackageGrid";
import { PackageFilter } from "../components/packages/PackageFilter";
import { useT, useI18nStore } from "../i18n";

export function PackagesPage() {
  const t = useT();
  const locale = useI18nStore((s) => s.locale);
  const [packages, setPackages] = useState<TravelPackage[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [destination, setDestination] = useState<string | undefined>();
  const [category, setCategory] = useState<string | undefined>();
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    setIsLoading(true);
    const params: Record<string, string | number> = {};
    if (destination) params.destination = destination;
    if (category) params.category = category;

    packageApi
      .list(params)
      .then(({ data }) => setPackages(data))
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, [destination, category, locale]);

  const handleSemanticSearch = async () => {
    if (!searchQuery.trim()) return;
    setIsLoading(true);
    try {
      const { data } = await packageApi.semanticSearch(searchQuery);
      // Semantic search returns different shape — map for display
      setPackages(data as TravelPackage[]);
    } catch {
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-bold text-gray-900">{t("packages.title")}</h1>
      <p className="mt-2 text-gray-500">
        {t("packages.subtitle")}
      </p>

      <div className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <PackageFilter
          destination={destination}
          category={category}
          onDestinationChange={setDestination}
          onCategoryChange={setCategory}
        />

        <div className="flex gap-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSemanticSearch()}
            placeholder={t("packages.searchPlaceholder")}
            className="input w-64"
          />
          <button onClick={handleSemanticSearch} className="btn-primary">
            {t("packages.searchBtn")}
          </button>
        </div>
      </div>

      <div className="mt-8">
        <PackageGrid packages={packages} isLoading={isLoading} />
      </div>
    </div>
  );
}
