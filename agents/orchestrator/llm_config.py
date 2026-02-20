"""OpenRouter LLM configuration for CrewAI agents.

Model names are read from env vars (shared with backend via .env):
  LLM_MODEL_PRIMARY  — main model for reasoning / planning
  LLM_MODEL_FALLBACK — lighter model for creative synthesis
"""

import os

from crewai import LLM

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

LLM_MODEL_PRIMARY = os.getenv("LLM_MODEL_PRIMARY", "arcee-ai/trinity-large-preview:free")
LLM_MODEL_FALLBACK = os.getenv("LLM_MODEL_FALLBACK", "arcee-ai/trinity-mini:free")


def get_llm(model: str = LLM_MODEL_PRIMARY, temperature: float = 0.7) -> LLM:
    """Create an OpenRouter-backed LLM for CrewAI."""
    return LLM(
        model=f"openrouter/{model}",
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        temperature=temperature,
    )


# Pre-configured LLMs for different agent roles
# Free-tier models via OpenRouter (upgrade to paid models for production)
llm_fast = get_llm(LLM_MODEL_PRIMARY, temperature=0.3)  # Intent parsing, structured extraction
llm_reasoning = get_llm(LLM_MODEL_PRIMARY, temperature=0.7)  # Planning, complex reasoning
llm_creative = get_llm(LLM_MODEL_FALLBACK, temperature=0.8)  # Final synthesis, writing
