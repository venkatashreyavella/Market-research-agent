from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() in {"1", "true", "yes", "on"}
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# Groq deprecated llama-3.3-70b-versatile for non-enterprise accounts in 2026.
# Keep the model configurable because availability can vary by Groq project.
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")


def require_live_credentials() -> None:
    if not GROQ_API_KEY or not TAVILY_API_KEY:
        raise RuntimeError("Set GROQ_API_KEY and TAVILY_API_KEY, or enable MOCK_MODE=true.")
