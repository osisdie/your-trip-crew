# Security

## Credential Handling

- **`.env`** is gitignored — never commit real credentials.
- **`.env.example`** contains placeholder values for local development only.
- **Production**: Copy `.env.example` to `.env`, then set strong values for:
  - `JWT_SECRET_KEY` — use a cryptographically random string (e.g. `openssl rand -hex 32`)
  - `POSTGRES_PASSWORD` / `NEO4J_PASSWORD` — use strong passwords
  - `OPENROUTER_API_KEY` — your OpenRouter API key
  - OAuth secrets (`GOOGLE_CLIENT_SECRET`, `LINE_CHANNEL_SECRET`) if using social login

## Pre-Publish Checklist

- [ ] No real API keys, tokens, or passwords in the repository
- [ ] `.env` is in `.gitignore` and not tracked
- [ ] Default values (`trippass`, `change-me-to-a-random-secret`) are dev-only — override via `.env` for production
