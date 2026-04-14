"""Agent 3: Cultural Adaptation Translator — the core differentiator."""

import json
import logging

from backend.llm import call_claude, parse_json_response

logger = logging.getLogger("culturebridge.translator")

SYSTEM_PROMPT = """You are an expert cultural adaptation translator specializing in Chinese-to-{target_lang} translation for entertainment content ({content_type}).

You are NOT doing literal translation. You are doing CULTURAL ADAPTATION — preserving the emotional impact, cultural meaning, and narrative intent while making it natural for {market_name} audiences.

CRITICAL RULES:
1. Every cultural concept MUST follow the provided translation guide. Never deviate from it.
2. Maintain character voice consistency — each character should sound distinct.
3. Preserve emotional tone and dramatic tension.
4. Add cultural_note for lines containing cultural concepts (Viki-style annotations for overseas viewers).
5. Rate your confidence for each line: "high", "medium", or "low".

TRANSLATION GUIDE (from knowledge base — follow strictly):
{translation_guide}

CHARACTER REFERENCE:
{characters}

OVERALL TONE: {tone}

Output JSON array. Each element:
{{
  "line_number": 1,
  "original": "原文",
  "translation": "adapted translation",
  "confidence": "high/medium/low",
  "cultural_note": "optional Viki-style note for viewers, or null",
  "decision_reason": "why this translation was chosen (reference KB entry if applicable)"
}}

Output ONLY the JSON array. No explanation."""


def run(context: dict, scan_result: dict, match_result: dict) -> dict:
    """Produce culturally adapted translation with decision audit trail."""
    content = context["content"]
    content_type = context["content_type"]
    target_lang = context["target_lang"]
    target_market = context["target_market"]

    market_names = {
        "us": "American",
        "sea": "Southeast Asian",
        "jp": "Japanese",
        "kr": "Korean",
        "eu": "European",
        "mena": "Middle Eastern",
    }
    lang_names = {"en": "English", "ja": "Japanese", "ko": "Korean"}

    # Build translation guide from enriched elements
    guide_entries = []
    for elem in match_result.get("enriched_elements", []):
        mapping = elem.get("mapping")
        if mapping:
            guide_entries.append(
                f"- {elem['concept']}: "
                f"GOOD: {', '.join(mapping.get('good', []))} | "
                f"BAD (never use): {', '.join(mapping.get('bad', []))} | "
                f"Principle: {mapping.get('principle', 'N/A')}"
            )
        else:
            guide_entries.append(
                f"- {elem['concept']}: (no KB entry — use your best judgment, flag as low confidence)"
            )

    translation_guide = (
        "\n".join(guide_entries)
        if guide_entries
        else "No specific cultural mappings provided."
    )

    # Character reference
    characters = scan_result.get("characters", [])
    char_ref = (
        "\n".join(
            f"- {c.get('name', '?')}: {c.get('role', '?')} — speaks {c.get('speech_style', 'normally')}"
            for c in characters
        )
        if characters
        else "No character data."
    )

    tone = scan_result.get("tone", "neutral")

    system = SYSTEM_PROMPT.format(
        target_lang=lang_names.get(target_lang, target_lang),
        content_type=content_type,
        market_name=market_names.get(target_market, target_market),
        translation_guide=translation_guide,
        characters=char_ref,
        tone=tone,
    )

    # Split content into lines for line-by-line translation
    lines = [line.strip() for line in content.strip().split("\n") if line.strip()]

    # Process in chunks to stay within token limits
    chunk_size = 30
    all_translations = []

    for i in range(0, len(lines), chunk_size):
        chunk = lines[i : i + chunk_size]
        numbered = "\n".join(f"{i + j + 1}. {line}" for j, line in enumerate(chunk))

        messages = [
            {"role": "user", "content": f"Translate the following lines:\n\n{numbered}"}
        ]
        response = call_claude(
            messages, system=system, max_tokens=6000, temperature=0.3
        )
        chunk_result = parse_json_response(response)

        if isinstance(chunk_result, list):
            all_translations.extend(chunk_result)
        elif isinstance(chunk_result, dict) and "translations" in chunk_result:
            all_translations.extend(chunk_result["translations"])

    # Separate cultural notes
    cultural_notes = [
        {
            "line_number": t.get("line_number"),
            "original": t.get("original"),
            "note": t["cultural_note"],
        }
        for t in all_translations
        if t.get("cultural_note")
    ]

    logger.info(
        "Translated %d lines, %d cultural notes generated",
        len(all_translations),
        len(cultural_notes),
    )

    return {
        "translations": all_translations,
        "cultural_notes": cultural_notes,
        "line_count": len(all_translations),
    }
