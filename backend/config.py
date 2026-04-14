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
