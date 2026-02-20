import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuthStore } from "../stores/authStore";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { useT } from "../i18n";

export function AuthCallbackPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const { setTokens, fetchUser } = useAuthStore();
  const t = useT();

  useEffect(() => {
    const accessToken = params.get("access_token");
    const refreshToken = params.get("refresh_token");

    if (accessToken && refreshToken) {
      setTokens(accessToken, refreshToken);
      fetchUser().then(() => navigate("/", { replace: true }));
    } else {
      navigate("/login", { replace: true });
    }
  }, [params, setTokens, fetchUser, navigate]);

  return (
    <div className="flex min-h-[80vh] items-center justify-center">
      <div className="text-center">
        <LoadingSpinner size="lg" />
        <p className="mt-4 text-sm text-gray-500">{t("auth.signingIn")}</p>
      </div>
    </div>
  );
}
