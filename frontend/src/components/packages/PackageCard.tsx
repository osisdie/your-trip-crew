import { Link } from "react-router-dom";
import type { TravelPackage } from "../../lib/types";
import { useT } from "../../i18n";

const PLACEHOLDER_IMAGES: Record<string, string> = {
  Japan:
    "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&h=400&fit=crop",
  Taiwan:
    "https://images.unsplash.com/photo-1470004914212-05527e49370b?w=600&h=400&fit=crop",
};

export function PackageCard({ pkg }: { pkg: TravelPackage }) {
  const t = useT();
  const imageUrl =
    pkg.cover_image_url || PLACEHOLDER_IMAGES[pkg.destination] || PLACEHOLDER_IMAGES["Japan"];

  return (
    <Link to={`/packages/${pkg.slug}`} className="card group overflow-hidden transition hover:shadow-md">
      <div className="aspect-[16/10] overflow-hidden">
        <img
          src={imageUrl}
          alt={pkg.title}
          className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
        />
      </div>
      <div className="p-4">
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-primary-50 px-2 py-0.5 text-xs font-medium text-primary-700">
            {pkg.destination}
          </span>
          <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
            {pkg.category}
          </span>
        </div>
        <h3 className="mt-2 font-semibold text-gray-900 line-clamp-1">
          {pkg.title}
        </h3>
        <p className="mt-1 text-sm text-gray-500 line-clamp-2">{pkg.summary}</p>
        <div className="mt-3 flex items-center justify-between">
          <span className="text-lg font-bold text-primary-600">
            ${pkg.price_usd.toLocaleString()}
          </span>
          <span className="text-xs text-gray-400">
            {pkg.duration_days} {t("common.days")}
          </span>
        </div>
      </div>
    </Link>
  );
}
