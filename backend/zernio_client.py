"""Zernio API client — real publish to Instagram + TikTok.

Only Instagram and TikTok are wired for real publishing (both already
connected + free on the current Zernio plan). Other platforms stay on the
frontend's demo-simulation flow.
"""

import logging

import requests

from backend.config import (
    ZERNIO_API_KEY,
    ZERNIO_BASE_URL,
    ZERNIO_INSTAGRAM_ACCOUNT_ID,
    ZERNIO_TIKTOK_ACCOUNT_ID,
)

logger = logging.getLogger("culturebridge.zernio")

TIMEOUT = 30


def _headers():
    return {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
        "Content-Type": "application/json",
    }


def _get_tiktok_privacy_level(account_id: str) -> str:
    """Fetch the creator's allowed privacy levels and pick the most public one."""
    resp = requests.get(
        f"{ZERNIO_BASE_URL}/accounts/{account_id}/tiktok/creator-info",
        headers=_headers(),
        params={"mediaType": "photo"},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    levels = [lv["value"] for lv in resp.json().get("privacyLevels", [])]
    if "PUBLIC_TO_EVERYONE" in levels:
        return "PUBLIC_TO_EVERYONE"
    return levels[0] if levels else "SELF_ONLY"


def publish_instagram(caption: str, image_url: str) -> dict:
    """Publish a single-image post to the connected Instagram account."""
    if not ZERNIO_API_KEY or not ZERNIO_INSTAGRAM_ACCOUNT_ID:
        return {"success": False, "error": "Zernio Instagram account not configured"}

    payload = {
        "content": caption[:2200],
        "mediaItems": [{"type": "image", "url": image_url}],
        "platforms": [
            {"platform": "instagram", "accountId": ZERNIO_INSTAGRAM_ACCOUNT_ID}
        ],
        "publishNow": True,
    }
    return _create_post(payload)


def publish_tiktok(title: str, description: str, image_url: str) -> dict:
    """Publish a single-image (photo mode) post to the connected TikTok account."""
    if not ZERNIO_API_KEY or not ZERNIO_TIKTOK_ACCOUNT_ID:
        return {"success": False, "error": "Zernio TikTok account not configured"}

    try:
        privacy_level = _get_tiktok_privacy_level(ZERNIO_TIKTOK_ACCOUNT_ID)
    except requests.exceptions.RequestException as e:
        logger.error("Failed to fetch TikTok creator info: %s", e)
        return {"success": False, "error": f"Could not fetch TikTok creator info: {e}"}

    payload = {
        "content": title[:90],
        "mediaItems": [{"type": "image", "url": image_url}],
        "platforms": [{"platform": "tiktok", "accountId": ZERNIO_TIKTOK_ACCOUNT_ID}],
        "tiktokSettings": {
            "privacy_level": privacy_level,
            "allow_comment": True,
            "content_preview_confirmed": True,
            "express_consent_given": True,
            "media_type": "photo",
            "description": description[:4000],
        },
        "publishNow": True,
    }
    return _create_post(payload)


def _create_post(payload: dict) -> dict:
    try:
        resp = requests.post(
            f"{ZERNIO_BASE_URL}/posts",
            json=payload,
            headers=_headers(),
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        logger.error("Zernio publish request failed: %s", e)
        return {"success": False, "error": str(e)}

    if resp.status_code >= 400:
        try:
            error = resp.json().get("error", resp.text)
            detail = (
                error.get("message", resp.text) if isinstance(error, dict) else error
            )
        except ValueError:
            detail = resp.text
        logger.error("Zernio publish failed (%d): %s", resp.status_code, detail)
        return {"success": False, "error": detail}

    data = resp.json()
    post = data.get("post", {})
    logger.info(
        "Zernio publish succeeded: post_id=%s status=%s",
        post.get("_id"),
        post.get("status"),
    )
    return {"success": True, "post_id": post.get("_id"), "status": post.get("status")}
