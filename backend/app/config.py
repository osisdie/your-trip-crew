from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ─── App ────────────────────────────────────────
    app_name: str = "AI Trip Planner"
    debug: bool = False

    # ─── Database ───────────────────────────────────
    database_url: str = "postgresql+asyncpg://tripuser:trippass@trip-postgres:5432/tripdb"

    # ─── Redis ──────────────────────────────────────
    redis_url: str = "redis://trip-redis:6379/0"

    # ─── JWT ────────────────────────────────────────
    jwt_secret_key: str = "change-me-to-a-random-secret"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 30

    # ─── Google OAuth ───────────────────────────────
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8200/api/v1/auth/google/callback"

    # ─── LINE OAuth ─────────────────────────────────
    line_channel_id: str = ""
    line_channel_secret: str = ""
    line_redirect_uri: str = "http://localhost:8200/api/v1/auth/line/callback"

    # ─── Frontend ───────────────────────────────────
    frontend_url: str = "http://localhost:5373"

    # ─── MCP Servers ────────────────────────────────
    mcp_japan_url: str = "http://trip-mcp-japan:8001"
    mcp_taiwan_url: str = "http://trip-mcp-taiwan:8002"
    mcp_flights_url: str = "http://trip-mcp-flights:8003"
    mcp_utilities_url: str = "http://trip-mcp-utilities:8004"
    mcp_knowledge_url: str = "http://trip-mcp-knowledge:8005"

    # ─── OpenRouter ─────────────────────────────────
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    llm_model_primary: str = "arcee-ai/trinity-large-preview:free"
    llm_model_fallback: str = "arcee-ai/trinity-mini:free"

    # ─── Rate Limits ────────────────────────────────
    rate_limit_unauth: int = 100
    rate_limit_auth: int = 200
    daily_limit_free: int = 5
    daily_limit_premium: int = 50

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
