import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { packageApi } from "../lib/api";
import type { TravelPackage } from "../lib/types";
import { PackageCard } from "../components/packages/PackageCard";
import { useAuthStore } from "../stores/authStore";
import { useT, useI18nStore } from "../i18n";

export function HomePage() {
  const { isAuthenticated } = useAuthStore();
  const t = useT();
  const locale = useI18nStore((s) => s.locale);
  const [featured, setFeatured] = useState<TravelPackage[]>([]);

  useEffect(() => {
    packageApi.list({ limit: 6 }).then(({ data }) => setFeatured(data)).catch(() => {});
  }, [locale]);

  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 py-24 text-white">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSA2MCAwIEwgMCAwIDAgNjAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')]" />
        </div>
        <div className="relative mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            {t("home.hero.title")}
            <br />
            <span className="text-primary-200">{t("home.hero.titleAccent")}</span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-primary-100">
            {t("home.hero.subtitle")}
          </p>
          <div className="mt-10 flex items-center justify-center gap-4">
            {isAuthenticated ? (
              <Link to="/chat" className="btn-accent text-base px-8 py-3">
                {t("home.hero.startPlanning")}
              </Link>
            ) : (
              <Link to="/login" className="btn-accent text-base px-8 py-3">
                {t("home.hero.signInToStart")}
              </Link>
            )}
            <Link to="/packages" className="btn-secondary text-base px-8 py-3 bg-white/10 border-white/20 text-white hover:bg-white/20">
              {t("home.hero.browsePackages")}
            </Link>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center text-3xl font-bold text-gray-900">
            {t("home.how.title")}
          </h2>
          <div className="mt-12 grid gap-8 sm:grid-cols-3">
            {[
              {
                icon: "💬",
                title: t("home.how.step1.title"),
                desc: t("home.how.step1.desc"),
              },
              {
                icon: "🤖",
                title: t("home.how.step2.title"),
                desc: t("home.how.step2.desc"),
              },
              {
                icon: "🗺️",
                title: t("home.how.step3.title"),
                desc: t("home.how.step3.desc"),
              },
            ].map((step, i) => (
              <div key={i} className="text-center">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-primary-50 text-3xl">
                  {step.icon}
                </div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900">
                  {step.title}
                </h3>
                <p className="mt-2 text-sm text-gray-500">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Packages */}
      {featured.length > 0 && (
        <section className="bg-gray-50 py-20">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold text-gray-900">
                {t("home.featured.title")}
              </h2>
              <Link
                to="/packages"
                className="text-sm font-medium text-primary-600 hover:text-primary-700"
              >
                {t("home.featured.viewAll")}
              </Link>
            </div>
            <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {featured.map((pkg) => (
                <PackageCard key={pkg.id} pkg={pkg} />
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
