# E2E Test: Chat → AI Response (Real LLM Call) + Docker Fix

## Context

Two tasks:

1. **Docker build fix**: Running `pnpm install` locally created `frontend/node_modules/`, which conflicts with Docker's `COPY . .` in the frontend Dockerfile. No `.dockerignore` exists to exclude it.

2. **Chat AI E2E tests**: The existing 22-test suite covers health, auth guards, packages CRUD, and OpenAPI — but **zero coverage** of the core feature: user sends a prompt → AI responds with clarifying questions. The orchestrator (`backend/app/services/orchestrator.py`) calls OpenRouter's `gpt-4o-mini`, so a true E2E test will hit the live LLM.

---

## Part A: Fix Docker Build

### Problem
`frontend/Dockerfile` line 8: `COPY . .` sends the entire build context including `node_modules/` (created locally by `pnpm install`). This conflicts with the `node_modules/` already created by `RUN npm install` in the Docker layer cache.

### Fix

**Step A1**: Delete local `frontend/node_modules/` directory

**Step A2**: Create `frontend/.dockerignore`
```
node_modules
dist
```

This prevents local `node_modules` and `dist` from being sent to the Docker build context, regardless of whether someone runs `pnpm install` locally again.

---

## Part B: Chat AI E2E Tests

### Architecture Understanding

**Chat flow:**
1. `POST /api/v1/chat/sessions` → creates `ChatSession` (requires JWT auth)
2. `POST /api/v1/chat/sessions/{id}/messages` body `{"content": "..."}` → saves user msg, calls `process_user_message()` via OpenRouter, saves + returns assistant msg as `ChatMessageRead`
3. Orchestrator system prompt tells AI: "ask clarifying questions if info missing"
4. `check_and_increment()` enforces daily rate limit (free: 5/day)

**Response shape** (`ChatMessageRead`):
```json
{"id": "uuid", "session_id": "uuid", "role": "assistant", "content": "...", "metadata_": null, "created_at": "..."}
```

**Message list** (`GET .../messages`): `{"messages": [...], "total": int, "has_more": bool}`

**Key files:**
- `backend/app/tests/conftest.py` — httpx client fixtures (sync)
- `backend/app/core/security.py` — `create_access_token(user_id: uuid.UUID) -> str`
- `backend/app/models/user.py` — `User` table with `id, email, display_name, tier, is_active`
- `backend/app/models/chat.py` — `chat_sessions`, `chat_messages` tables
- `backend/app/models/usage.py` — `usage_records` table
- `backend/app/services/orchestrator.py` — OpenRouter LLM call

### Step B1: Add auth fixtures to `conftest.py`

Append to existing `backend/app/tests/conftest.py`:

- **`test_user_token` fixture** (scope=`module`):
  - Uses `asyncpg` (already installed) via `asyncio.run()` for sync compatibility
  - `INSERT INTO users (id, email, display_name, tier, is_active)` with deterministic test UUID
  - Generates JWT via `create_access_token(user_id)`
  - Teardown: deletes test data from `chat_messages`, `chat_sessions`, `usage_records`, `users`

- **`auth_client` fixture** (scope=`module`):
  - httpx.Client with `Authorization: Bearer {token}` header, 60s timeout

**Why asyncpg?** It's already in `pyproject.toml` dependencies — no new package needed. We wrap it in `asyncio.run()` because conftest uses sync fixtures.

### Step B2: Create `backend/app/tests/test_chat_ai.py`

New file with `@pytest.mark.slow` + `skipif(not OPENROUTER_API_KEY)`:

| # | Test | What it verifies |
|---|------|------------------|
| 1 | `test_create_session` | `POST /sessions` → 200, returns `{title, is_active: true}` |
| 2 | `test_vague_prompt_gets_clarifying_response` | Send "I want to go to Japan" → AI asks about dates/budget/travelers (keyword check in both EN + ZH) |
| 3 | `test_detailed_prompt_gets_itinerary` | Send complete request (2 adults, 5 days Tokyo, $3000) → AI produces day-by-day plan |
| 4 | `test_messages_persisted` | `GET /messages` → total=4 (2 user + 2 assistant), correct role order |
| 5 | `test_list_sessions_includes_test_session` | `GET /sessions` includes our session ID |
| 6 | `test_delete_session` | `DELETE /sessions/{id}` → 200, session removed from active list |

Tests use `self.__class__.session_id` to share state across ordered test methods within the class.

### Step B3: Add Makefile target

```makefile
test-backend-ai:
	docker compose exec trip-backend pytest app/tests/test_chat_ai.py -v -m slow --timeout=120
```

---

## Files Modified Summary

| File | Change |
|---|---|
| `frontend/.dockerignore` | **NEW** — exclude `node_modules` and `dist` from Docker build context |
| `frontend/node_modules/` | **DELETE** — remove locally-created node_modules |
| `backend/app/tests/conftest.py` | Add `test_user_token` + `auth_client` fixtures using asyncpg |
| `backend/app/tests/test_chat_ai.py` | **NEW** — 6 E2E tests for chat AI flow |
| `Makefile` | Add `test-backend-ai` target |

**Total: 2 new files, 2 modified files, 1 directory deleted**

No new dependencies needed (`asyncpg` already installed).

---

## Verification

1. **Docker build**: `rm -rf frontend/node_modules && docker compose up -d --build` — frontend builds cleanly
2. **Existing tests**: `make test-backend` — 22 tests still pass
3. **AI tests**: `make test-backend-ai` — 6 tests pass (~30-60s due to LLM latency)
4. **Without API key**: `make test-backend` skips AI tests automatically (no `OPENROUTER_API_KEY`)
5. **Cleanup**: After test run, verify no leftover test user in DB
