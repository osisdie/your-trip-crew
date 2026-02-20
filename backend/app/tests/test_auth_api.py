"""E2E: Auth endpoints — guards and redirects."""


class TestAuthGuard:
    def test_users_me_requires_auth(self, client):
        resp = client.get("/api/v1/users/me")
        assert resp.status_code == 401

    def test_invalid_token_rejected(self, client):
        resp = client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert resp.status_code == 401
        assert "Invalid" in resp.json()["detail"]

    def test_chat_sessions_requires_auth(self, client):
        resp = client.get("/api/v1/chat/sessions")
        assert resp.status_code == 401

    def test_itineraries_requires_auth(self, client):
        resp = client.get("/api/v1/itineraries")
        assert resp.status_code == 401

    def test_usage_requires_auth(self, client):
        resp = client.get("/api/v1/users/me/usage")
        assert resp.status_code == 401


class TestOAuthRedirects:
    def test_google_login_redirects(self, client):
        resp = client.get("/api/v1/auth/google", follow_redirects=False)
        assert resp.status_code in (302, 307)
        assert "accounts.google.com" in resp.headers.get("location", "")

    def test_line_login_redirects(self, client):
        resp = client.get("/api/v1/auth/line", follow_redirects=False)
        assert resp.status_code in (302, 307)
        assert "access.line.me" in resp.headers.get("location", "")


class TestTokenRefresh:
    def test_refresh_without_body_returns_422(self, client):
        resp = client.post("/api/v1/auth/refresh")
        assert resp.status_code == 422

    def test_refresh_with_invalid_token(self, client):
        resp = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "bogus"},
        )
        assert resp.status_code == 401
