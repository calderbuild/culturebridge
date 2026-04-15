"""Agent 5: Finalizer — apply review fixes, generate decision report + promo materials."""

import json
import logging

from backend.llm import call_claude, parse_json_response

logger = logging.getLogger("culturebridge.finalizer")

FINALIZE_SYSTEM = """You are finalizing a cultural adaptation translation. You have:
1. The original translations
2. Review feedback with issues to fix

Apply ONLY the reviewer's suggested fixes. Do not change lines that have no issues.

Output JSON:
{{
  "final_translation": [
    {{
      "line_number": 1,
      "original": "原文",
      "translation": "final version",
      "was_revised": true/false,
      "revision_note": "what was changed and why (or null if unchanged)"
    }}
  ]
}}"""

DECISION_REPORT_SYSTEM = """Generate a Translation Decision Report for this cultural adaptation project.

For each cultural concept encountered, explain:
- The concept and its cultural significance
- Why the chosen translation was selected
- What alternatives were considered and rejected
- The knowledge base entry that informed the decision (if any)

This report lets the client audit WHY each cultural decision was made.
Write in English. Be specific and cite the knowledge base entries provided.

Output JSON:
{{
  "report_title": "Translation Decision Report",
  "target_market": "...",
  "decisions": [
    {{
      "concept": "臣妾",
      "significance": "what this means culturally",
      "chosen_translation": "the translation used",
      "alternatives_rejected": ["rejected option 1", "rejected option 2"],
      "rationale": "why this choice",
      "kb_source": "knowledge_base or llm_inference"
    }}
  ],
  "summary": "overall approach summary"
}}"""

PROMO_SYSTEM = """Based on the content analysis and translation, generate overseas promotion materials.

Output JSON:
{{
  "synopsis": "100-200 word synopsis in {target_lang} for overseas audiences",
  "social_posts": [
    {{"platform": "TikTok", "text": "post text with hashtags"}},
    {{"platform": "Instagram", "text": "post text with hashtags"}},
    {{"platform": "X", "text": "post text with hashtags"}}
  ],
  "hashtag_suggestions": ["#tag1", "#tag2"],
  "target_audience": "description of ideal overseas audience"
}}"""

PLATFORM_CONTENT_SYSTEM = """You are an overseas social media content strategist specializing in Chinese cultural content going global.

Based on the translated content and cultural context provided, generate platform-specific promotional content for 5 overseas platforms.

STRICT FORMAT CONSTRAINTS — violating character limits is unacceptable:

1. TikTok:
   - caption: max 150 characters, punchy and curiosity-driving
   - hashtags: 5-10 relevant hashtags as an array
   - cover_text_suggestion: short text overlay for the video cover

2. Instagram:
   - caption: max 2200 characters, storytelling style with line breaks
   - hashtags: up to 30 hashtags as an array
   - carousel_texts: array of exactly 3 slide captions for a carousel post

3. YouTube:
   - title: max 100 characters, SEO-friendly
   - description: max 5000 characters, with timestamps section placeholder
   - tags: exactly 15 tags as an array
   - chapter_suggestions: array of chapter title suggestions

4. Twitter/X:
   - tweets: array of exactly 3 standalone tweets, each max 280 characters
   - thread_version: array of connected thread tweets (5-8 tweets, each max 280 chars)

5. Reddit:
   - title: concise, discussion-provoking
   - body: detailed post body in markdown format
   - subreddit_suggestions: array of relevant subreddits (e.g. r/CDrama, r/noveltranslations, r/Manhua)

Output JSON with this exact structure:
{{
  "tiktok": {{"caption": "...", "hashtags": [...], "cover_text_suggestion": "..."}},
  "instagram": {{"caption": "...", "hashtags": [...], "carousel_texts": [...]}},
  "youtube": {{"title": "...", "description": "...", "tags": [...], "chapter_suggestions": [...]}},
  "twitter": {{"tweets": [...], "thread_version": [...]}},
  "reddit": {{"title": "...", "body": "...", "subreddit_suggestions": [...]}}
}}"""


def run(
    context: dict, translation_result: dict, review_result: dict, match_result: dict
) -> dict:
    """Finalize translation + generate decision report and promo materials."""
    translations = translation_result.get("translations", [])
    issues = review_result.get("issues", [])
    target_lang = context["target_lang"]

    # Step 5a: Apply review fixes
    final_translation = _apply_fixes(translations, issues)

    # Step 5b: Generate decision report
    decision_report = _generate_decision_report(context, match_result)

    # Step 5c: Generate promo materials
    promo = _generate_promo(context, translation_result)

    # Step 5d: Adaptation suggestions
    adaptation = _generate_adaptation_suggestions(context, translation_result)

    # Step 5e: Platform-specific content for 5 overseas platforms
    platform_content = _generate_platform_content(context, translation_result)

    logger.info(
        "Finalized: %d lines, %d decisions, %d promo items, %d platforms",
        len(final_translation),
        len(decision_report.get("decisions", [])),
        len(promo.get("social_posts", [])),
        len(platform_content) if isinstance(platform_content, dict) else 0,
    )

    return {
        "final_translation": final_translation,
        "decision_report": decision_report,
        "promo_materials": promo,
        "adaptation_suggestions": adaptation,
        "platform_content": platform_content,
    }


def _apply_fixes(translations: list, issues: list) -> list:
    """Apply reviewer fixes to translations."""
    if not issues:
        return [
            {**t, "was_revised": False, "revision_note": None} for t in translations
        ]

    # Build fix context
    trans_text = json.dumps(translations, ensure_ascii=False, indent=2)
    issues_text = json.dumps(issues, ensure_ascii=False, indent=2)

    messages = [
        {
            "role": "user",
            "content": f"Original translations:\n{trans_text}\n\nReview issues to fix:\n{issues_text}",
        }
    ]

    response = call_claude(
        messages, system=FINALIZE_SYSTEM, max_tokens=6000, temperature=0.2
    )
    result = parse_json_response(response)
    return result.get("final_translation", translations)


def _generate_decision_report(context: dict, match_result: dict) -> dict:
    """Generate the translation decision audit report."""
    enriched = match_result.get("enriched_elements", [])
    if not enriched:
        return {
            "report_title": "Translation Decision Report",
            "decisions": [],
            "summary": "No cultural elements found.",
        }

    elements_desc = json.dumps(
        [
            {
                "concept": e["concept"],
                "source": e["source"],
                "mapping": e.get("mapping"),
            }
            for e in enriched
        ],
        ensure_ascii=False,
        indent=2,
    )

    messages = [
        {
            "role": "user",
            "content": f"Target market: {context['target_market']}\nContent type: {context['content_type']}\n\nCultural elements and their KB mappings:\n{elements_desc}",
        }
    ]

    response = call_claude(
        messages, system=DECISION_REPORT_SYSTEM, max_tokens=8000, temperature=0.3
    )
    result = parse_json_response(response)
    if isinstance(result, dict) and result.get("_parse_failed"):
        logger.warning(
            "Decision report JSON parse failed, building from enriched elements"
        )
        return {
            "report_title": "Translation Decision Report",
            "target_market": context["target_market"],
            "decisions": [
                {
                    "concept": e["concept"],
                    "significance": e.get("mapping", {}).get("cultural_note", ""),
                    "chosen_translation": ", ".join(
                        e.get("mapping", {}).get("good", [])
                    ),
                    "alternatives_rejected": e.get("mapping", {}).get("bad", []),
                    "rationale": e.get("mapping", {}).get("principle", ""),
                    "kb_source": e["source"],
                }
                for e in enriched
                if e.get("mapping")
            ],
            "summary": f"Cultural adaptation report for {context['target_market']} market",
        }
    return result


def _generate_promo(context: dict, translation_result: dict) -> dict:
    """Generate overseas promotion materials."""
    lang_names = {"en": "English", "ja": "Japanese", "ko": "Korean"}
    target_lang = lang_names.get(context["target_lang"], context["target_lang"])

    # Use first few translated lines as context
    sample = translation_result.get("translations", [])[:10]
    sample_text = "\n".join(
        f"{t.get('original', '')} → {t.get('translation', '')}" for t in sample
    )

    messages = [
        {
            "role": "user",
            "content": f"Content type: {context['content_type']}\nTarget market: {context['target_market']}\n\nSample content:\n{sample_text}",
        }
    ]

    system = PROMO_SYSTEM.format(target_lang=target_lang)
    response = call_claude(messages, system=system, max_tokens=3000, temperature=0.5)
    result = parse_json_response(response)
    if isinstance(result, dict) and result.get("_parse_failed"):
        return {
            "synopsis": "",
            "social_posts": [],
            "hashtag_suggestions": [],
            "target_audience": "",
        }
    return result


def _generate_adaptation_suggestions(context: dict, translation_result: dict) -> dict:
    """Generate adaptation suggestions (character names, plot adjustments)."""
    notes = translation_result.get("cultural_notes", [])
    if not notes:
        return {"suggestions": [], "summary": "No specific adaptation needed."}

    notes_text = json.dumps(notes, ensure_ascii=False, indent=2)

    messages = [
        {
            "role": "user",
            "content": (
                f"Content type: {context['content_type']}, target market: {context['target_market']}\n\n"
                f"Cultural notes from translation:\n{notes_text}\n\n"
                "Based on these cultural elements, suggest adaptations for the target market: "
                "character name localization, plot adjustments, visual changes. "
                "Output JSON with 'suggestions' array and 'summary'."
            ),
        }
    ]

    response = call_claude(
        messages,
        system="You are a cultural adaptation consultant.",
        max_tokens=2000,
        temperature=0.4,
    )
    return parse_json_response(response)


def _generate_platform_content(context: dict, translation_result: dict) -> dict:
    """Generate platform-specific promotional content for 5 overseas platforms."""
    lang_names = {"en": "English", "ja": "Japanese", "ko": "Korean"}
    target_lang = lang_names.get(context["target_lang"], context["target_lang"])

    sample = translation_result.get("translations", [])[:10]
    sample_text = "\n".join(
        f"{t.get('original', '')} -> {t.get('translation', '')}" for t in sample
    )

    notes = translation_result.get("cultural_notes", [])
    notes_text = ""
    if notes:
        notes_text = "\nCultural notes:\n" + json.dumps(
            notes, ensure_ascii=False, indent=2
        )

    messages = [
        {
            "role": "user",
            "content": (
                f"Content type: {context['content_type']}\n"
                f"Target market: {context['target_market']}\n"
                f"Target language: {target_lang}\n\n"
                f"Sample translated content:\n{sample_text}"
                f"{notes_text}\n\n"
                "Generate platform-specific promotional content for all 5 platforms "
                "(TikTok, Instagram, YouTube, Twitter/X, Reddit) in a single JSON response. "
                "Respect all character limits strictly."
            ),
        }
    ]

    response = call_claude(
        messages, system=PLATFORM_CONTENT_SYSTEM, max_tokens=6000, temperature=0.5
    )
    result = parse_json_response(response)
    if isinstance(result, dict) and result.get("_parse_failed"):
        logger.warning("Platform content JSON parse failed")
        return {"_parse_failed": True}
    return result
