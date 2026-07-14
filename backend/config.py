"""Configuration for CultureBridge — unified OpenRouter LLM access."""

import os
import sys
import logging

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# DeepSeek for analysis/review (Chinese understanding, cheap)
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek/deepseek-chat-v3-0324")
# Claude for translation output (multilingual quality)
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "anthropic/claude-sonnet-4")

# Gemini for cover image generation (Instagram/TikTok promo assets)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image")

# Zernio: social publishing aggregator (real publish to Instagram + TikTok)
ZERNIO_API_KEY = os.getenv("ZERNIO_API_KEY", "")
ZERNIO_BASE_URL = "https://zernio.com/api/v1"
ZERNIO_INSTAGRAM_ACCOUNT_ID = os.getenv("ZERNIO_INSTAGRAM_ACCOUNT_ID", "")
ZERNIO_TIKTOK_ACCOUNT_ID = os.getenv("ZERNIO_TIKTOK_ACCOUNT_ID", "")

# Public base URL this server is reachable at. Zernio must fetch media over
# the public internet, so generated images need a real HTTPS URL, not a
# localhost path.
PUBLIC_BASE_URL = os.getenv(
    "PUBLIC_BASE_URL", "https://culturebridge-dwoy.onrender.com"
)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge", "mappings")


def validate_config():
    logger = logging.getLogger("culturebridge")
    if not OPENROUTER_API_KEY:
        logger.error(
            "OPENROUTER_API_KEY not set. Copy .env.example to .env and add your key."
        )
        sys.exit(1)
