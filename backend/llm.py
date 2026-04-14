"""Unified LLM client via OpenRouter — DeepSeek for analysis, Claude for translation."""

import json
import logging

import requests

from backend.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    DEEPSEEK_MODEL,
    CLAUDE_MODEL,
)

logger = logging.getLogger("culturebridge.llm")


def strip_markdown_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    return text


def _call_openrouter(
    model: str,
    messages: list,
    max_tokens: int = 4000,
    temperature: float = 0.3,
    response_format: str = None,
) -> str:
    """Call OpenRouter API (OpenAI-compatible)."""
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format == "json":
        payload["response_format"] = {"type": "json_object"}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/calderbuild/culturebridge",
        "X-Title": "CultureBridge",
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=180)
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    if not content:
        raise RuntimeError(f"{model} returned empty response")
    return content


def call_deepseek(
    messages: list,
    max_tokens: int = 4000,
    temperature: float = 0.3,
    response_format: str = None,
) -> str:
    """Call DeepSeek via OpenRouter. Used for analysis and review."""
    return _call_openrouter(
        DEEPSEEK_MODEL, messages, max_tokens, temperature, response_format
    )


def call_claude(
    messages: list,
    system: str = "",
    max_tokens: int = 4000,
    temperature: float = 0.3,
) -> str:
    """Call Claude via OpenRouter. Used for translation output."""
    if system:
        messages = [{"role": "system", "content": system}] + messages
    return _call_openrouter(CLAUDE_MODEL, messages, max_tokens, temperature)


def parse_json_response(text: str) -> dict | list:
    """Parse JSON from LLM response with robust fallback handling."""
    cleaned = strip_markdown_fences(text)

    # Try direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try extracting outermost braces
    for open_ch, close_ch in [("{", "}"), ("[", "]")]:
        start = cleaned.find(open_ch)
        end = cleaned.rfind(close_ch) + 1
        if start >= 0 and end > start:
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                continue

    # Last resort: fix common LLM JSON errors and retry
    fixed = cleaned
    fixed = fixed.replace("'", '"')  # single quotes
    fixed = fixed.replace(",}", "}")  # trailing comma in object
    fixed = fixed.replace(",]", "]")  # trailing comma in array
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass

    # If all parsing fails, return the raw text wrapped in a dict
    logger.warning(
        "Failed to parse JSON, returning raw text. First 200 chars: %s", cleaned[:200]
    )
    return {"raw_text": cleaned, "_parse_failed": True}
