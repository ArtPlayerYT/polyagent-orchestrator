"""The two models the agent loop uses, kept in one place so they are easy to swap.

The orchestrator (Google ADK) authors the shared look and the hub page; the five
workers build the games.

By default, the orchestrator routes through your local OmniRoute server
(OpenAI-compatible API at http://localhost:20128/v1) using the 'auto' model.
"""

import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm

load_dotenv(override=True)

# --- OmniRoute configuration ---
_OMNIROUTE_ENABLED = os.environ.get("OMNIROUTE_ENABLED", "1") == "1"

_OMNIROUTE_BASE = (
    os.environ.get("OMNIROUTER_BASE_URL")
    or os.environ.get("OMNIROUTE_BASE_URL")
    or "http://localhost:20128/v1"
).strip().strip('"').strip("'")

_OMNIROUTE_API_KEY = (
    os.environ.get("OMNIROUTER_API_KEY")
    or os.environ.get("OMNIROUTE_API_KEY")
    or ""
).strip()

_RAW_MODEL = os.environ.get("ORCHESTRATOR_MODEL", "auto").strip()

if _RAW_MODEL.startswith("openai/"):
    _LITELLM_MODEL = _RAW_MODEL
else:
    _LITELLM_MODEL = f"openai/{_RAW_MODEL}"

if _OMNIROUTE_ENABLED:
    ORCHESTRATOR_MODEL = LiteLlm(
        model=_LITELLM_MODEL,
        api_base=_OMNIROUTE_BASE,
        api_key=_OMNIROUTE_API_KEY,
    )
    ORCHESTRATOR_MODEL_NAME = f"OmniRoute ({_RAW_MODEL})"
else:
    # Direct Gemini fallback (uses GOOGLE_API_KEY from .env)
    ORCHESTRATOR_MODEL = "gemini-3.5-flash"
    ORCHESTRATOR_MODEL_NAME = "gemini-3.5-flash"

WORKER_MODEL = os.environ.get("WORKER_MODEL", "auto")
