"""Bridge between FastAPI and the CrewAI agent orchestration layer.

MVP: Direct OpenRouter calls with structured slot extraction.
Each LLM response includes a hidden SLOTS_JSON line that gets parsed,
merged with accumulated slots, and persisted to ChatSession.intent_slots.
When required slots are complete, the LLM switches to itinerary generation mode.
"""

import json
import logging
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

SYSTEM_PROMPT = """\
You are a professional travel planning assistant specializing in Japan and Taiwan trips.
Your job is to help users plan complete travel itineraries.

RULES:
1. Respond in the SAME LANGUAGE as the user. If the user writes in Chinese, reply in Traditional Chinese (繁體中文), NOT Simplified Chinese.
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

SLOT EXTRACTION (MANDATORY):
After your response, you MUST append exactly one line in this format:
SLOTS_JSON: {"destination":"...","duration_days":...,"num_travelers":...}

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

# Regex: match the last occurrence of SLOTS_JSON: {...} at end of content
_SLOTS_RE = re.compile(r"\n?SLOTS_JSON:\s*(\{[^\n]*\})\s*$")

# Fields that IntentSlots / TripPlanningState recognise
_KNOWN_SLOT_KEYS = frozenset({
    "destination", "start_date", "end_date", "duration_days",
    "num_travelers", "budget_usd", "trip_style", "origin_city",
    "preferences", "children_ages",
})


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
_DEST_PATTERNS = [
    (re.compile(r"日本|japan|東京|tokyo|大阪|osaka|京都|kyoto|北海道|hokkaido|沖繩|okinawa", re.I), "japan"),
    (re.compile(r"台灣|台湾|taiwan|台北|taipei|高雄|kaohsiung|台中|taichung|花蓮|hualien", re.I), "taiwan"),
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
        parts.append(
            f"[Accumulated travel info]: {json.dumps(intent_slots, ensure_ascii=False)}"
        )
        if slots_complete(intent_slots):
            parts.append(
                "[Status]: All required info collected. Generate a detailed itinerary now."
            )
        else:
            missing = _missing_fields(intent_slots)
            parts.append(f"[Status]: Still need: {', '.join(missing)}")
    else:
        parts.append("[Accumulated travel info]: None yet — this is a new conversation.")

    parts.append(f"\nUser message: {user_message}")
    return "\n".join(parts)


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
    await _emit(session_id, step="intent_parsing", crew="intent", status="active",
                message="Extracting intent from user message")
    regex_slots = _extract_slots_from_message(user_message)
    merged = _merge_slots(intent_slots, regex_slots)
    logger.info("Regex extraction: %s | after merge: %s", regex_slots, merged)
    await _emit(session_id, step="intent_parsing", crew="intent", status="done",
                slots=merged, message="Slots extracted via regex")

    # Check completeness → routing decision
    await _emit(session_id, step="routing", crew="router", status="active",
                message="Checking slot completeness")
    dest = merged.get("destination")
    dest_crew = dest if dest in ("japan", "taiwan") else None
    await _emit(session_id, step="routing", crew="router", status="done",
                slots=merged,
                message=f"Route: {'plan_' + dest if dest_crew else 'ask_user'}")

    # Build LLM prompt with latest accumulated context
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_prompt(user_message, merged)},
    ]

    # LLM call → planning phase
    planning_crew = dest_crew or "japan"
    await _emit(session_id, step="planning", crew=planning_crew, status="active",
                message="Waiting for LLM response")

    async with httpx.AsyncClient(timeout=120.0) as client:
        for model in LLM_MODELS:
            logger.info("Trying model: %s for session %s", model, session_id)
            content = await _call_llm(client, model, messages)
            if content:
                logger.info("Success with model: %s", model)
                await _emit(session_id, step="planning", crew=planning_crew, status="done",
                            message=f"LLM responded ({model})")

                # Layer 2: LLM SLOTS_JSON (bonus) → post-processing
                await _emit(session_id, step="post_processing",
                            crew=["booking", "advisory"], status="active",
                            message="Extracting LLM slots")
                visible, llm_slots = _extract_slots_from_llm(content)
                if llm_slots:
                    merged = _merge_slots(merged, llm_slots)
                    logger.info("LLM slots: %s | final: %s", llm_slots, merged)
                await _emit(session_id, step="post_processing",
                            crew=["booking", "advisory"], status="done",
                            slots=merged, message="Slots merged")

                logger.info(
                    "Final slots: %s | complete: %s",
                    merged, slots_complete(merged),
                )

                await _emit(session_id, step="synthesizing", crew="synthesis",
                            status="done", slots=merged, message="Response ready")
                await _emit(session_id, step="complete", status="done",
                            slots=merged, message="All done")
                return visible, merged

    await _emit(session_id, step="complete", status="error",
                slots=merged, message="All LLM models unavailable")
    return (
        "I'm sorry, all AI models are currently unavailable. "
        "Please try again in a few minutes."
    ), merged
