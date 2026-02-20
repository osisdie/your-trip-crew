import { Link } from "react-router-dom";
import { useAuthStore } from "../../stores/authStore";
import { UsageBadge } from "../common/UsageBadge";
import { LanguageToggle } from "../common/LanguageToggle";
import { useT } from "../../i18n";

export function Navbar() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const t = useT();

  return (
    <nav className="sticky top-0 z-50 border-b border-gray-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-8">
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl">✈️</span>
            <span className="text-lg font-bold text-gray-900">
              {t("nav.brand")}
            </span>
          </Link>
          <div className="hidden items-center gap-6 md:flex">
            <Link
              to="/packages"
              className="text-sm font-medium text-gray-600 transition hover:text-gray-900"
            >
              {t("nav.packages")}
            </Link>
            {isAuthenticated && (
              <>
                <Link
                  to="/chat"
                  className="text-sm font-medium text-gray-600 transition hover:text-gray-900"
                >
                  {t("nav.chat")}
                </Link>
                <Link
                  to="/itineraries"
                  className="text-sm font-medium text-gray-600 transition hover:text-gray-900"
                >
                  {t("nav.trips")}
                </Link>
              </>
            )}
          </div>
        </div>

        <div className="flex items-center gap-4">
          <LanguageToggle />
          {isAuthenticated ? (
            <>
              <UsageBadge />
              <Link to="/profile" className="flex items-center gap-2">
                {user?.avatar_url ? (
                  <img
                    src={user.avatar_url}
                    alt=""
                    className="h-8 w-8 rounded-full"
                  />
                ) : (
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-sm font-medium text-primary-700">
                    {user?.display_name?.[0] || "?"}
                  </div>
                )}
              </Link>
              <button
                onClick={logout}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                {t("nav.logout")}
              </button>
            </>
          ) : (
            <Link to="/login" className="btn-primary">
              {t("nav.signIn")}
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
