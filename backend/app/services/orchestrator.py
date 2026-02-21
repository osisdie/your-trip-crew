"""Bridge between FastAPI and the CrewAI agent orchestration layer.

MVP: Direct OpenRouter calls with structured slot extraction.
Each LLM response includes a hidden SLOTS_JSON line that gets parsed,
merged with accumulated slots, and persisted to ChatSession.intent_slots.
When required slots are complete, the LLM switches to itinerary generation mode.
"""

import asyncio
import json
import logging
import os
import re
import uuid

import httpx

from app.config import settings
from app.services.flow_events import emit as flow_emit

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# LLM config — model names come from .env via pydantic-settings
# ---------------------------------------------------------------------------
LLM_MODELS = [settings.llm_model_primary, settings.llm_model_fallback]

# ---------------------------------------------------------------------------
# Shared instructions appended to both prompts
# ---------------------------------------------------------------------------
_SHARED_INSTRUCTIONS = """\

FORMAT RULES:
- Always respond in **Markdown** unless the response is very short (under 2 sentences).
- Use headings (##, ###), bullet lists, bold, and tables for itineraries and comparisons.

LINK & CITATION RULES:
- Include relevant external links to official websites, booking platforms, and travel resources.
  Examples: attraction official sites, Japan Rail Pass, booking.com, klook, Google Maps.
- Include internal links to our travel packages where relevant: `/packages/{{slug}}`
- Format all links using numbered citation style:
  "Visit Sensō-ji Temple [1] in the morning, then take the Tsukuba Express [2]."
  At the end of the response, add a **References** section:
  [1]: https://www.senso-ji.jp/ "Sensō-ji Temple Official Site"
  [2]: https://www.mir.co.jp/en/ "Tsukuba Express"
- Only cite real, well-known URLs. Do NOT invent or guess URLs.

SLOT EXTRACTION (MANDATORY):
After your response, you MUST append exactly one line in this format:
SLOTS_JSON: {{"destination":"...","duration_days":...,"num_travelers":...}}

Rules for the SLOTS_JSON line:
- Include ONLY fields where the user has provided clear information.
- Omit fields that are unknown or not yet mentioned.
- Valid field names and types:
  destination     (string, e.g. "japan", "taiwan", "tokyo")
  start_date      (string "YYYY-MM-DD", only if specific date given)
  end_date        (string "YYYY-MM-DD", only if specific date given)
  duration_days   (integer)
  num_travelers   (integer)
  budget_usd      (number)
  trip_style      (string: adventure/relaxation/culture/family/food/luxury/budget)
  origin_city     (string, departure city)
  preferences     (array of strings, e.g. ["skiing","hot springs","temples"])
  children_ages   (array of integers)
- This line is automatically parsed and hidden from the user.
- Do NOT reference or explain SLOTS_JSON in your visible response.\
"""

GREETING_PROMPT = (
    """\
You are a professional travel planning assistant specializing in Japan and Taiwan trips.
Your job is to help users plan complete travel itineraries.

RULES:
1. Greet the user in {locale} language.
2. If critical info is missing (destination, dates/duration, number of travelers), \
ask clarifying questions. List what you still need.
3. If you have enough info, create a detailed day-by-day itinerary with:
   - Daily schedule (morning/afternoon/evening)
   - Accommodation recommendations
   - Transportation between locations
   - Estimated costs in USD and local currency
   - Total cost breakdown (flights, hotels, transport, activities, meals)
4. Consider children's ages for family trips, ski level for ski trips, \
and seasonal events/festivals.
5. Be specific with place names, train lines, and restaurant recommendations.
"""
    + _SHARED_INSTRUCTIONS
)

CONVERSATION_PROMPT = (
    """\
You are a professional travel planning assistant specializing in Japan and Taiwan trips.
Your job is to help users plan complete travel itineraries.

RULES:
1. Respond in the SAME LANGUAGE as the user.
2. If critical info is missing (destination, dates/duration, number of travelers), \
ask clarifying questions. List what you still need.
3. If you have enough info, create a detailed day-by-day itinerary with:
   - Daily schedule (morning/afternoon/evening)
   - Accommodation recommendations
   - Transportation between locations
   - Estimated costs in USD and local currency
   - Total cost breakdown (flights, hotels, transport, activities, meals)
4. Consider children's ages for family trips, ski level for ski trips, \
and seasonal events/festivals.
5. Be specific with place names, train lines, and restaurant recommendations.
"""
    + _SHARED_INSTRUCTIONS
)

# Regex: match the last occurrence of SLOTS_JSON: {...} at end of content
_SLOTS_RE = re.compile(r"\n?SLOTS_JSON:\s*(\{[^\n]*\})\s*$")

# URL regex for link validation
_URL_RE = re.compile(r'https?://[^\s\)\]"\'<>]+')

# Fields that IntentSlots / TripPlanningState recognise
_KNOWN_SLOT_KEYS = frozenset(
    {
        "destination",
        "start_date",
        "end_date",
        "duration_days",
        "num_travelers",
        "budget_usd",
        "trip_style",
        "origin_city",
        "preferences",
        "children_ages",
    }
)

# Locale display names for the greeting prompt
_LOCALE_NAMES = {
    "en": "English",
    "zh": "Traditional Chinese (繁體中文)",
    "zh-TW": "Traditional Chinese (繁體中文)",
    "ja": "Japanese",
}


# ---------------------------------------------------------------------------
# Slot helpers
# ---------------------------------------------------------------------------


def _extract_slots_from_llm(content: str) -> tuple[str, dict | None]:
    """Parse SLOTS_JSON from the tail of an LLM response.

    Returns (visible_content, extracted_slots_or_None).
    """
    match = _SLOTS_RE.search(content)
    if not match:
        return content.strip(), None
    try:
        raw = json.loads(match.group(1))
        # Keep only recognised keys with non-null values
        slots = {k: v for k, v in raw.items() if k in _KNOWN_SLOT_KEYS and v is not None}
        clean = content[: match.start()].strip()
        return clean, slots if slots else None
    except (json.JSONDecodeError, TypeError):
        return content[: match.start()].strip(), None


# ---------------------------------------------------------------------------
# Rule-based slot extraction from user message (fallback for weak models)
# ---------------------------------------------------------------------------
_JAPAN_RE = r"日本|japan|東京|tokyo|大阪|osaka|京都|kyoto|北海道|hokkaido|沖繩|okinawa"
_TAIWAN_RE = r"台灣|台湾|taiwan|台北|taipei|高雄|kaohsiung|台中|taichung|花蓮|hualien"
_DEST_PATTERNS = [
    (re.compile(_JAPAN_RE, re.I), "japan"),
    (re.compile(_TAIWAN_RE, re.I), "taiwan"),
]
_DURATION_RE = re.compile(r"(\d+)\s*(?:天|日|days?|nights?)", re.I)
_TRAVELERS_RE = re.compile(r"(\d+)\s*(?:人|個人|位|adults?|people|persons?|pax)", re.I)
_BUDGET_RE = re.compile(r"(?:預算|budget)[^\d]*(\d[\d,]*)\s*(?:美[金元]|usd|\$)?", re.I)
_BUDGET_RE2 = re.compile(r"\$\s*(\d[\d,]*)", re.I)
_CHILDREN_RE = re.compile(r"(?:小孩|孩子|兒童|children?|kids?)\D*(\d+)\s*(?:歲|岁|years?\s*old|yo)", re.I)
_DATE_RE = re.compile(r"(\d{4})[/\-.](\d{1,2})[/\-.](\d{1,2})")


def _extract_slots_from_message(user_message: str) -> dict:
    """Extract slots from the raw user message using pattern matching.

    This is a reliable fallback when the LLM doesn't produce SLOTS_JSON.
    Only extracts what is clearly stated — never guesses.
    """
    slots: dict = {}

    # Destination
    for pattern, dest in _DEST_PATTERNS:
        if pattern.search(user_message):
            slots["destination"] = dest
            break

    # Duration
    m = _DURATION_RE.search(user_message)
    if m:
        slots["duration_days"] = int(m.group(1))

    # Number of travelers
    m = _TRAVELERS_RE.search(user_message)
    if m:
        slots["num_travelers"] = int(m.group(1))

    # Budget
    m = _BUDGET_RE.search(user_message) or _BUDGET_RE2.search(user_message)
    if m:
        slots["budget_usd"] = float(m.group(1).replace(",", ""))

    # Dates (YYYY-MM-DD)
    dates = _DATE_RE.findall(user_message)
    if len(dates) >= 2:
        slots["start_date"] = f"{dates[0][0]}-{int(dates[0][1]):02d}-{int(dates[0][2]):02d}"
        slots["end_date"] = f"{dates[1][0]}-{int(dates[1][1]):02d}-{int(dates[1][2]):02d}"
    elif len(dates) == 1:
        slots["start_date"] = f"{dates[0][0]}-{int(dates[0][1]):02d}-{int(dates[0][2]):02d}"

    # Children ages (basic: "小孩5歲")
    children = _CHILDREN_RE.findall(user_message)
    if children:
        slots["children_ages"] = [int(age) for age in children]

    return slots


def _merge_slots(existing: dict | None, new: dict | None) -> dict:
    """Merge newly extracted slots into the accumulated dict.

    New non-None values override old ones; old values are preserved otherwise.
    """
    merged = dict(existing or {})
    for key, value in (new or {}).items():
        merged[key] = value
    return merged


def slots_complete(slots: dict | None) -> bool:
    """Check if we have enough info to generate an itinerary.

    Required: destination + (duration_days OR start_date+end_date) + num_travelers.
    """
    if not slots:
        return False
    if not slots.get("destination"):
        return False
    if not slots.get("num_travelers"):
        return False
    has_duration = bool(slots.get("duration_days"))
    has_dates = bool(slots.get("start_date") and slots.get("end_date"))
    return has_duration or has_dates


def _missing_fields(slots: dict | None) -> list[str]:
    """Return human-readable list of missing required fields."""
    s = slots or {}
    missing = []
    if not s.get("destination"):
        missing.append("destination")
    if not s.get("duration_days") and not (s.get("start_date") and s.get("end_date")):
        missing.append("travel dates or duration")
    if not s.get("num_travelers"):
        missing.append("number of travelers")
    return missing


# ---------------------------------------------------------------------------
# LLM calling
# ---------------------------------------------------------------------------


async def _call_llm(client: httpx.AsyncClient, model: str, messages: list[dict]) -> str | None:
    """Call OpenRouter with a specific model. Returns content or None on failure."""
    try:
        resp = await client.post(
            f"{settings.openrouter_base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 4000,
            },
        )
        if resp.status_code != 200:
            logger.warning("LLM %s returned %d: %s", model, resp.status_code, resp.text[:200])
            return None

        result = resp.json()
        return result["choices"][0]["message"]["content"]

    except (KeyError, IndexError) as e:
        logger.warning("LLM %s response parse error: %s", model, e)
        return None
    except httpx.HTTPError as e:
        logger.warning("LLM %s HTTP error: %s", model, e)
        return None


def _build_user_prompt(user_message: str, intent_slots: dict | None) -> str:
    """Build the user-role prompt with accumulated slot context."""
    parts: list[str] = []

    if intent_slots:
        parts.append(f"[Accumulated travel info]: {json.dumps(intent_slots, ensure_ascii=False)}")
        if slots_complete(intent_slots):
            parts.append("[Status]: All required info collected. Generate a detailed itinerary now.")
        else:
            missing = _missing_fields(intent_slots)
            parts.append(f"[Status]: Still need: {', '.join(missing)}")
    else:
        parts.append("[Accumulated travel info]: None yet — this is a new conversation.")

    parts.append(f"\nUser message: {user_message}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Link validation (post-processing)
# ---------------------------------------------------------------------------

# Derive concurrency limit from runtime resources.
# Free-threading (PEP 703) builds aren't GIL-bound, so higher I/O concurrency
# is safe.  Standard CPython stays conservative to avoid fd exhaustion.
_LINK_MAX_CONCURRENCY = min(os.cpu_count() or 4, 16) * 2


async def _validate_links(content: str) -> str:
    """Validate URLs in markdown content. Remove dead links.

    Uses a single shared AsyncClient (connection pooling) and a semaphore
    to cap concurrency based on available runtime resources.
    """
    urls = list(set(_URL_RE.findall(content)))
    if not urls:
        return content

    sem = asyncio.Semaphore(_LINK_MAX_CONCURRENCY)

    async def check_url(client: httpx.AsyncClient, url: str) -> tuple[str, bool]:
        async with sem:
            try:
                resp = await client.head(url)
                return url, resp.status_code < 400
            except Exception:
                return url, False

    async with httpx.AsyncClient(
        timeout=5.0,
        follow_redirects=True,
        limits=httpx.Limits(
            max_connections=_LINK_MAX_CONCURRENCY,
            max_keepalive_connections=_LINK_MAX_CONCURRENCY // 2,
        ),
    ) as client:
        results = await asyncio.gather(*[check_url(client, u) for u in urls])

    dead_urls = {url for url, ok in results if not ok}

    if not dead_urls:
        return content

    for url in dead_urls:
        # Remove lines containing dead URLs from References section
        content = re.sub(rf"\n\[?\d*\]?:?\s*{re.escape(url)}[^\n]*", "", content)
        # Convert inline dead links to plain text: [text](url) → text
        content = re.sub(rf"\[([^\]]+)\]\({re.escape(url)}\)", r"\1", content)

    return content.strip()


# ---------------------------------------------------------------------------
# Flow-event helper (best-effort — never breaks the chat flow)
# ---------------------------------------------------------------------------


async def _emit(session_id, **kwargs) -> None:
    try:
        await flow_emit(session_id, **kwargs)
    except Exception:
        logger.debug("flow_emit failed (non-critical)", exc_info=True)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


async def process_user_message(
    session_id: uuid.UUID,
    user_message: str,
    intent_slots: dict | None,
    locale: str = "en",
) -> tuple[str, dict]:
    """Process a chat message and return (visible_reply, updated_slots).

    Slot extraction uses two layers:
      1. Rule-based regex on the user message (always works)
      2. LLM SLOTS_JSON line in response (bonus, if the model cooperates)
    Both are merged into the accumulated slots.

    The caller is responsible for persisting the updated slots to the DB.
    """
    await _emit(session_id, step="received", status="active", message="Message received")

    # Layer 1: rule-based extraction from user message (reliable)
    await _emit(
        session_id,
        step="intent_parsing",
        crew="intent",
        status="active",
        message="Extracting intent from user message",
    )
    regex_slots = _extract_slots_from_message(user_message)
    merged = _merge_slots(intent_slots, regex_slots)
    logger.info("Regex extraction: %s | after merge: %s", regex_slots, merged)
    await _emit(
        session_id,
        step="intent_parsing",
        crew="intent",
        status="done",
        slots=merged,
        message="Slots extracted via regex",
    )

    # Check completeness → routing decision
    await _emit(
        session_id,
        step="routing",
        crew="router",
        status="active",
        message="Checking slot completeness",
    )
    dest = merged.get("destination")
    dest_crew = dest if dest in ("japan", "taiwan") else None
    await _emit(
        session_id,
        step="routing",
        crew="router",
        status="done",
        slots=merged,
        message=f"Route: {'plan_' + dest if dest_crew else 'ask_user'}",
    )

    # Select prompt: greeting (first message) vs conversation (subsequent)
    is_greeting = not intent_slots
    if is_greeting:
        locale_name = _LOCALE_NAMES.get(locale, locale)
        system_prompt = GREETING_PROMPT.format(locale=locale_name)
    else:
        system_prompt = CONVERSATION_PROMPT

    # Build LLM prompt with latest accumulated context
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": _build_user_prompt(user_message, merged)},
    ]

    # LLM call → planning phase
    planning_crew = dest_crew or "japan"
    await _emit(
        session_id,
        step="planning",
        crew=planning_crew,
        status="active",
        message="Waiting for LLM response",
    )

    async with httpx.AsyncClient(timeout=120.0) as client:
        for model in LLM_MODELS:
            logger.info("Trying model: %s for session %s", model, session_id)
            content = await _call_llm(client, model, messages)
            if content:
                logger.info("Success with model: %s", model)
                await _emit(
                    session_id,
                    step="planning",
                    crew=planning_crew,
                    status="done",
                    message=f"LLM responded ({model})",
                )

                # Layer 2: LLM SLOTS_JSON (bonus) → post-processing
                await _emit(
                    session_id,
                    step="post_processing",
                    crew=["booking", "advisory"],
                    status="active",
                    message="Extracting LLM slots",
                )
                visible, llm_slots = _extract_slots_from_llm(content)
                if llm_slots:
                    merged = _merge_slots(merged, llm_slots)
                    logger.info("LLM slots: %s | final: %s", llm_slots, merged)
                await _emit(
                    session_id,
                    step="post_processing",
                    crew=["booking", "advisory"],
                    status="done",
                    slots=merged,
                    message="Slots merged",
                )

                # Link validation
                await _emit(
                    session_id,
                    step="link_validation",
                    crew="link_validator",
                    status="active",
                    message="Validating links",
                )
                visible = await _validate_links(visible)
                await _emit(
                    session_id,
                    step="link_validation",
                    crew="link_validator",
                    status="done",
                    message="Links validated",
                )

                logger.info(
                    "Final slots: %s | complete: %s",
                    merged,
                    slots_complete(merged),
                )

                await _emit(
                    session_id,
                    step="synthesizing",
                    crew="synthesis",
                    status="done",
                    slots=merged,
                    message="Response ready",
                )
                await _emit(session_id, step="complete", status="done", slots=merged, message="All done")
                return visible, merged

    await _emit(
        session_id,
        step="complete",
        status="error",
        slots=merged,
        message="All LLM models unavailable",
    )
    return ("I'm sorry, all AI models are currently unavailable. Please try again in a few minutes."), merged
