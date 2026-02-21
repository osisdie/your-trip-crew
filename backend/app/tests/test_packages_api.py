"""E2E: Packages API endpoints."""


class TestListPackages:
    def test_returns_list(self, client):
        resp = client.get("/api/v1/packages")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_package_shape(self, client):
        resp = client.get("/api/v1/packages")
        pkg = resp.json()[0]
        for field in (
            "id",
            "title",
            "slug",
            "destination",
            "category",
            "summary",
            "price_usd",
            "duration_days",
        ):
            assert field in pkg, f"Missing field: {field}"

    def test_filter_by_destination_japan(self, client):
        resp = client.get("/api/v1/packages", params={"destination": "Japan"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        assert all(p["destination"] == "Japan" for p in data)

    def test_filter_by_destination_taiwan(self, client):
        resp = client.get("/api/v1/packages", params={"destination": "Taiwan"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        assert all(p["destination"] == "Taiwan" for p in data)

    def test_filter_by_category(self, client):
        resp = client.get("/api/v1/packages", params={"category": "Skiing"})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        assert all(p["category"] == "Skiing" for p in data)

    def test_filter_no_results(self, client):
        resp = client.get("/api/v1/packages", params={"destination": "Antarctica"})
        assert resp.status_code == 200
        assert resp.json() == []


class TestGetPackageBySlug:
    def test_valid_slug(self, client):
        resp = client.get("/api/v1/packages/tokyo-explorer-5day")
        assert resp.status_code == 200
        data = resp.json()
        assert data["slug"] == "tokyo-explorer-5day"
        assert "days" in data
        assert "tags" in data
        assert len(data["days"]) == 5

    def test_invalid_slug_returns_404(self, client):
        resp = client.get("/api/v1/packages/nonexistent-package")
        assert resp.status_code == 404


class TestCategories:
    def test_returns_list_of_strings(self, client):
        resp = client.get("/api/v1/packages/categories")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert all(isinstance(c, str) for c in data)
        assert "Skiing" in data
        assert "Culture" in data
