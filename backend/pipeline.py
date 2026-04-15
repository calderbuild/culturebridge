"""5-Agent cultural adaptation pipeline: Scanner -> Matcher -> Translator -> Reviewer -> Finalizer.

Graceful degradation: Scanner and Translator are critical (pipeline stops on failure).
Matcher, Reviewer, and Finalizer degrade gracefully — partial results are returned."""

import logging
import time
from dataclasses import dataclass, field
from typing import Callable

logger = logging.getLogger("culturebridge.pipeline")


@dataclass
class PipelineEvent:
    stage: str
    message: str
    progress: float
    data: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


def run_pipeline(
    content: str,
    content_type: str = "drama",
    target_lang: str = "en",
    target_market: str = "us",
    on_event: Callable[[PipelineEvent], None] = None,
    job_id: str = None,
    create_content: bool = False,
    intent: str = "",
    target_platforms: list = None,
) -> dict:
    from backend.agents import (
        cultural_scanner,
        kb_matcher,
        translator,
        reviewer,
        finalizer,
    )

    def emit(stage, message, progress, data=None):
        if on_event:
            on_event(PipelineEvent(stage, message, progress, data or {}))

    result = {"stages": {}, "job_id": job_id, "degraded": []}

    # ---- Agent 0: Content Creator (optional, for beginner mode) ----
    if create_content:
        from backend.agents import content_creator

        emit("content_creator", "正在根据意图生成文化内容...", 0.02)
        t0 = time.time()
        try:
            creator_context = {
                "intent": intent,
                "content_type": content_type,
                "target_platforms": target_platforms or [],
                "target_lang": target_lang,
                "target_market": target_market,
            }
            creator_result = content_creator.run(creator_context)
        except Exception as e:
            logger.error("Content creator failed: %s", e, exc_info=True)
            emit("content_creator", f"内容生成失败: {e}", 0.02, {"level": "error"})
            raise RuntimeError(f"Content creator failed: {e}") from e
        logger.info("Content creator completed in %.1fs", time.time() - t0)
        result["stages"]["content_creator"] = creator_result
        content = creator_result.get("generated_content", "")
        content_type = creator_result.get("content_type", content_type)
        emit(
            "content_creator",
            f"内容生成完成：{creator_result.get('topic', '')}",
            0.05,
            {"topic": creator_result.get("topic", ""), "content": content},
        )

    context = {
        "content": content,
        "content_type": content_type,
        "target_lang": target_lang,
        "target_market": target_market,
    }

    # ---- Agent 1: Cultural Scanner (CRITICAL — fails pipeline) ----
    emit("scanner", "正在扫描文化元素...", 0.05)
    t0 = time.time()
    try:
        scan_result = cultural_scanner.run(context)
    except Exception as e:
        logger.error("Cultural scanner failed: %s", e, exc_info=True)
        emit("scanner", f"扫描失败: {e}", 0.05, {"level": "error"})
        raise RuntimeError(f"Cultural scanner failed: {e}") from e
    logger.info("Scanner completed in %.1fs", time.time() - t0)
    result["stages"]["scanner"] = scan_result
    emit(
        "scanner",
        f"发现 {len(scan_result.get('cultural_elements', []))} 个文化元素",
        0.20,
        {"count": len(scan_result.get("cultural_elements", []))},
    )

    # ---- Agent 2: KB Matcher (DEGRADABLE — falls back to empty enrichment) ----
    emit("matcher", "正在匹配知识库...", 0.20)
    t0 = time.time()
    try:
        match_result = kb_matcher.run(context, scan_result)
    except Exception as e:
        logger.warning("KB matcher failed, degrading: %s", e, exc_info=True)
        match_result = {
            "enriched_elements": [],
            "risk_report": {
                "overall_risk_level": "unknown",
                "summary": "知识库匹配失败，跳过风险评估",
                "risks": [],
            },
        }
        result["degraded"].append("matcher")
        emit(
            "matcher",
            "知识库匹配失败，使用降级模式",
            0.35,
            {"level": "warning", "degraded": True},
        )
    else:
        logger.info("Matcher completed in %.1fs", time.time() - t0)
        result["stages"]["matcher"] = match_result
        kb_hits = sum(
            1
            for e in match_result.get("enriched_elements", [])
            if e.get("source") == "knowledge_base"
        )
        emit(
            "matcher",
            f"知识库命中 {kb_hits} 条，生成文化风险报告",
            0.35,
            {"kb_hits": kb_hits},
        )

    # ---- Agent 3: Translator (CRITICAL — fails pipeline) ----
    emit("translator", "正在进行文化适配翻译...", 0.35)
    t0 = time.time()
    try:
        translation_result = translator.run(context, scan_result, match_result)
    except Exception as e:
        logger.error("Translator failed: %s", e, exc_info=True)
        emit("translator", f"翻译失败: {e}", 0.35, {"level": "error"})
        raise RuntimeError(f"Translator failed: {e}") from e
    logger.info("Translator completed in %.1fs", time.time() - t0)
    result["stages"]["translator"] = translation_result
    emit("translator", "文化适配翻译完成", 0.60)

    # ---- Agent 4: Reviewer (DEGRADABLE — skips review) ----
    emit("reviewer", "审校中...", 0.60)
    t0 = time.time()
    try:
        review_result = reviewer.run(context, translation_result, match_result)
    except Exception as e:
        logger.warning("Reviewer failed, degrading: %s", e, exc_info=True)
        review_result = {
            "issues": [],
            "overall_quality": "unreviewed",
            "summary": "审校跳过",
        }
        result["degraded"].append("reviewer")
        emit(
            "reviewer",
            "审校失败，跳过审校环节",
            0.80,
            {"level": "warning", "degraded": True},
        )
    else:
        logger.info("Reviewer completed in %.1fs", time.time() - t0)
        result["stages"]["reviewer"] = review_result
        issues_count = len(review_result.get("issues", []))
        emit(
            "reviewer",
            f"审校完成，发现 {issues_count} 个问题",
            0.80,
            {"issues": issues_count},
        )

    # ---- Agent 5: Finalizer (DEGRADABLE — returns raw translation) ----
    emit("finalizer", "生成终稿和出海方案...", 0.80)
    t0 = time.time()
    try:
        final_result = finalizer.run(
            context, translation_result, review_result, match_result
        )
    except Exception as e:
        logger.warning("Finalizer failed, degrading: %s", e, exc_info=True)
        final_result = {
            "final_translation": translation_result.get("translations", []),
            "decision_report": {"decisions": [], "summary": "终稿生成失败"},
            "promo_materials": {"social_posts": [], "hashtag_suggestions": []},
            "adaptation_suggestions": {"suggestions": [], "summary": ""},
            "platform_content": {"_parse_failed": True},
        }
        result["degraded"].append("finalizer")
        emit(
            "finalizer",
            "终稿生成失败，使用原始翻译",
            0.95,
            {"level": "warning", "degraded": True},
        )
    else:
        logger.info("Finalizer completed in %.1fs", time.time() - t0)
        result["stages"]["finalizer"] = final_result
        emit("finalizer", "终稿和出海方案生成完成", 0.95)

    # Assemble output
    result["output"] = {
        "translation": final_result.get(
            "final_translation", translation_result.get("translations", [])
        ),
        "decision_report": final_result.get("decision_report"),
        "risk_report": match_result.get("risk_report"),
        "cultural_notes": translation_result.get("cultural_notes"),
        "adaptation_suggestions": final_result.get("adaptation_suggestions"),
        "promo_materials": final_result.get("promo_materials"),
        "platform_content": final_result.get("platform_content"),
    }

    status_msg = (
        "全部完成！"
        if not result["degraded"]
        else f"完成（{len(result['degraded'])} 个环节降级）"
    )
    emit(
        "complete",
        status_msg,
        1.0,
        {
            "output_keys": list(result["output"].keys()),
            "degraded": result["degraded"],
        },
    )
    return result
