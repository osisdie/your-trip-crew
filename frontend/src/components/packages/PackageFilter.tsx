import { DESTINATIONS, CATEGORIES } from "../../lib/constants";
import { useT } from "../../i18n";

interface PackageFilterProps {
  destination?: string;
  category?: string;
  onDestinationChange: (val: string | undefined) => void;
  onCategoryChange: (val: string | undefined) => void;
}

export function PackageFilter({
  destination,
  category,
  onDestinationChange,
  onCategoryChange,
}: PackageFilterProps) {
  const t = useT();

  return (
    <div className="flex flex-wrap gap-3">
      <select
        value={destination || ""}
        onChange={(e) => onDestinationChange(e.target.value || undefined)}
        className="input"
      >
        <option value="">{t("packages.allDestinations")}</option>
        {DESTINATIONS.map((d: string) => (
          <option key={d} value={d}>{d}</option>
        ))}
      </select>

      <select
        value={category || ""}
        onChange={(e) => onCategoryChange(e.target.value || undefined)}
        className="input"
      >
        <option value="">{t("packages.allCategories")}</option>
        {CATEGORIES.map((c: string) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>
    </div>
  );
}
