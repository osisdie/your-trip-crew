import { useEffect, useState } from "react";
import { userApi } from "../../lib/api";
import type { UsageInfo } from "../../lib/types";
import { useT } from "../../i18n";

export function UsageBadge() {
  const [usage, setUsage] = useState<UsageInfo | null>(null);
  const t = useT();

  useEffect(() => {
    userApi.getUsage().then(({ data }) => setUsage(data)).catch(() => {});
  }, []);

  if (!usage) return null;

  const pct = Math.round((usage.query_count / usage.daily_limit) * 100);
  const color = pct >= 80 ? "text-red-600" : pct >= 50 ? "text-amber-600" : "text-green-600";

  return (
    <div className="flex items-center gap-2 text-xs">
      <span className={`font-medium ${color}`}>
        {usage.remaining}/{usage.daily_limit}
      </span>
      <span className="text-gray-400">{t("usage.queriesLeft")}</span>
    </div>
  );
}
