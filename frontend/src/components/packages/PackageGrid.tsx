import type { TravelPackage } from "../../lib/types";
import { PackageCard } from "./PackageCard";
import { LoadingSpinner } from "../common/LoadingSpinner";
import { useT } from "../../i18n";

interface PackageGridProps {
  packages: TravelPackage[];
  isLoading: boolean;
}

export function PackageGrid({ packages, isLoading }: PackageGridProps) {
  const t = useT();

  if (isLoading) {
    return (
      <div className="flex min-h-[300px] items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (packages.length === 0) {
    return (
      <div className="flex min-h-[300px] items-center justify-center text-gray-500">
        {t("packages.noResults")}
      </div>
    );
  }

  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {packages.map((pkg) => (
        <PackageCard key={pkg.id} pkg={pkg} />
      ))}
    </div>
  );
}
