"""E2E: OpenAPI schema validation."""


def test_openapi_schema_loads(client):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    assert schema["info"]["title"] == "AI Trip Planner"
    assert schema["info"]["version"] == "0.1.0"


def test_openapi_has_expected_paths(client):
    resp = client.get("/openapi.json")
    paths = resp.json()["paths"]

    expected = [
        "/health",
        "/api/v1/auth/google",
        "/api/v1/auth/line",
        "/api/v1/auth/refresh",
        "/api/v1/users/me",
        "/api/v1/chat/sessions",
        "/api/v1/packages",
        "/api/v1/packages/categories",
        "/api/v1/packages/search/semantic",
        "/api/v1/itineraries",
    ]
    for path in expected:
        assert path in paths, f"Missing path in OpenAPI: {path}"


def test_openapi_has_expected_schemas(client):
    resp = client.get("/openapi.json")
    schemas = resp.json()["components"]["schemas"]

    expected = [
        "PackageListRead",
        "PackageDetailRead",
        "ChatSessionRead",
        "ChatMessageRead",
        "UserRead",
        "TokenResponse",
        "ItineraryListRead",
        "UsageRead",
    ]
    for name in expected:
        assert name in schemas, f"Missing schema: {name}"
