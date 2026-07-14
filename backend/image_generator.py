"""Gemini-based cover image generation for Instagram/TikTok promo posts."""

import base64
import logging
import os
import time

import requests

from backend.config import GEMINI_API_KEY, GEMINI_IMAGE_MODEL, PUBLIC_BASE_URL

logger = logging.getLogger("culturebridge.image_generator")

GENERATED_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "frontend", "generated"
)
os.makedirs(GENERATED_DIR, exist_ok=True)

MAX_RETRIES = 2
RETRY_BACKOFF = [2, 4]


def generate_cover_image(prompt: str, job_id: str, platform: str) -> str | None:
    """Generate a cover image via Gemini and save it under frontend/generated/.

    Returns the public HTTPS URL on success, or None if generation failed
    (image generation is a nice-to-have, callers should degrade gracefully)."""
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set, skipping cover image generation")
        return None

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_IMAGE_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }

    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.post(url, json=payload, timeout=60)
            if resp.status_code >= 500 and attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF[attempt]
                logger.warning(
                    "Gemini image gen returned %d, retrying in %ds",
                    resp.status_code,
                    wait,
                )
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            parts = data["candidates"][0]["content"]["parts"]
            inline = next((p["inlineData"] for p in parts if "inlineData" in p), None)
            if not inline:
                logger.warning(
                    "Gemini response for %s/%s had no image data", job_id, platform
                )
                return None

            ext = "png" if "png" in inline.get("mimeType", "") else "jpg"
            filename = f"{job_id}_{platform}.{ext}"
            filepath = os.path.join(GENERATED_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(inline["data"]))

            public_url = f"{PUBLIC_BASE_URL}/generated/{filename}"
            logger.info(
                "Generated cover image for %s/%s: %s", job_id, platform, public_url
            )
            return public_url

        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF[attempt]
                logger.warning("Gemini image gen error, retrying in %ds: %s", wait, e)
                time.sleep(wait)
                continue

    logger.error(
        "Cover image generation failed for %s/%s: %s", job_id, platform, last_error
    )
    return None
