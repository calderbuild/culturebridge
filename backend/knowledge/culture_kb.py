"""Cultural Knowledge Base — load and query cultural concept mappings."""

import json
import logging
import os
from pathlib import Path

from backend.config import KNOWLEDGE_DIR

logger = logging.getLogger("culturebridge.kb")

_cache: dict = {}


def _load_all() -> dict:
    """Load all mapping files into memory. Cached after first call."""
    global _cache
    if _cache:
        return _cache

    kb_dir = Path(KNOWLEDGE_DIR)
    if not kb_dir.exists():
        logger.warning("Knowledge directory not found: %s", kb_dir)
        return {}

    for f in kb_dir.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for entry in data:
                    concept = entry.get("concept", "")
                    if concept:
                        _cache[concept] = entry
            logger.info(
                "Loaded %s: %d entries",
                f.name,
                len(data) if isinstance(data, list) else 0,
            )
        except Exception as e:
            logger.error("Failed to load %s: %s", f.name, e)

    logger.info("Knowledge base total: %d concepts", len(_cache))
    return _cache


def get_all_concept_keys() -> list[str]:
    """Return all known concept keys for prompt injection."""
    kb = _load_all()
    return list(kb.keys())


def lookup(concept: str, target_lang: str = "en") -> dict | None:
    """Look up a cultural concept and return its mapping for the target language.

    Returns dict with good/bad/principle/avoid/cultural_note keys, or None if not found.
    """
    kb = _load_all()
    entry = kb.get(concept)
    if not entry:
        return None
    mappings = entry.get("mappings", {})
    lang_mapping = mappings.get(target_lang)
    if not lang_mapping:
        return mappings.get("en")
    return lang_mapping


def lookup_full(concept: str) -> dict | None:
    """Return the full entry including context, content_types, etc."""
    kb = _load_all()
    return kb.get(concept)


def reload():
    """Force reload of knowledge base (for hot-reloading during development)."""
    global _cache
    _cache = {}
    _load_all()
