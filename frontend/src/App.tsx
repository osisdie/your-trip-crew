import { useEffect } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/layout/AppShell";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { ErrorBoundary } from "./components/common/ErrorBoundary";
import { useAuthStore } from "./stores/authStore";
import { useI18nStore } from "./i18n";

import { HomePage } from "./pages/HomePage";
import { LoginPage } from "./pages/LoginPage";
import { AuthCallbackPage } from "./pages/AuthCallbackPage";
import { PackagesPage } from "./pages/PackagesPage";
import { PackageDetailPage } from "./pages/PackageDetailPage";
import { ChatPage } from "./pages/ChatPage";
import { ItineraryPage } from "./pages/ItineraryPage";
import { ProfilePage } from "./pages/ProfilePage";
import { DevAgentFlowPage } from "./pages/DevAgentFlowPage";

export default function App() {
  const { fetchUser } = useAuthStore();
  const locale = useI18nStore((s) => s.locale);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  // Sync <html lang> on initial load and locale changes
  useEffect(() => {
    document.documentElement.lang = locale === "zh" ? "zh-Hant" : "en";
  }, [locale]);

  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/auth/callback" element={<AuthCallbackPage />} />
            <Route path="/dev/agents" element={<DevAgentFlowPage />} />
            <Route path="/packages" element={<PackagesPage />} />
            <Route path="/packages/:slug" element={<PackageDetailPage />} />
            <Route
              path="/chat"
              element={
                <ProtectedRoute>
                  <ChatPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/itinerary/:id"
              element={
                <ProtectedRoute>
                  <ItineraryPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/itineraries"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}
