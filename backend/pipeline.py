"""5-Agent cultural adaptation pipeline: Scanner → Matcher → Translator → Reviewer → Finalizer."""

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


AGENTS = [
    ("scanner", "文化元素扫描", 0.05, 0.20),
    ("matcher", "知识库匹配 + 文化风险评估", 0.20, 0.35),
    ("translator", "文化适配翻译", 0.35, 0.60),
    ("reviewer", "审校", 0.60, 0.80),
    ("finalizer", "终稿 + 出海方案", 0.80, 0.95),
]


def run_pipeline(
    content: str,
    content_type: str = "drama",
    target_lang: str = "en",
    target_market: str = "us",
    on_event: Callable[[PipelineEvent], None] = None,
    job_id: str = None,
) -> dict:
    """Run the 5-agent cultural adaptation pipeline.

    Args:
        content: Chinese text content (script, novel chapter, game dialogue)
        content_type: "drama", "novel", or "game"
        target_lang: Target language code ("en", "ja", "ko")
        target_market: Target market ("us", "sea", "jp", "kr", "eu")
        on_event: Callback for SSE progress events
        job_id: Job identifier

    Returns:
        Dict with all pipeline outputs (translation, reports, etc.)
    """
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

    result = {"stages": {}, "job_id": job_id}
    context = {
        "content": content,
        "content_type": content_type,
        "target_lang": target_lang,
        "target_market": target_market,
    }

    # Agent 1: Cultural Scanner
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

    # Agent 2: Knowledge Base Matcher + Risk Assessment
    emit("matcher", "正在匹配知识库...", 0.20)
    t0 = time.time()
    try:
        match_result = kb_matcher.run(context, scan_result)
    except Exception as e:
        logger.error("KB matcher failed: %s", e, exc_info=True)
        emit("matcher", f"匹配失败: {e}", 0.20, {"level": "error"})
        raise RuntimeError(f"KB matcher failed: {e}") from e
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

    # Agent 3: Cultural Adaptation Translation
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

    # Agent 4: Review
    emit("reviewer", "审校中...", 0.60)
    t0 = time.time()
    try:
        review_result = reviewer.run(context, translation_result, match_result)
    except Exception as e:
        logger.error("Reviewer failed: %s", e, exc_info=True)
        emit("reviewer", f"审校失败: {e}", 0.60, {"level": "error"})
        raise RuntimeError(f"Reviewer failed: {e}") from e
    logger.info("Reviewer completed in %.1fs", time.time() - t0)
    result["stages"]["reviewer"] = review_result
    issues_count = len(review_result.get("issues", []))
    emit(
        "reviewer",
        f"审校完成，发现 {issues_count} 个问题",
        0.80,
        {"issues": issues_count},
    )

    # Agent 5: Finalizer + Promo
    emit("finalizer", "生成终稿和出海方案...", 0.80)
    t0 = time.time()
    try:
        final_result = finalizer.run(
            context, translation_result, review_result, match_result
        )
    except Exception as e:
        logger.error("Finalizer failed: %s", e, exc_info=True)
        emit("finalizer", f"终稿生成失败: {e}", 0.80, {"level": "error"})
        raise RuntimeError(f"Finalizer failed: {e}") from e
    logger.info("Finalizer completed in %.1fs", time.time() - t0)
    result["stages"]["finalizer"] = final_result
    emit("finalizer", "终稿和出海方案生成完成", 0.95)

    # Assemble final output
    result["output"] = {
        "translation": final_result.get("final_translation"),
        "decision_report": final_result.get("decision_report"),
        "risk_report": match_result.get("risk_report"),
        "cultural_notes": translation_result.get("cultural_notes"),
        "adaptation_suggestions": final_result.get("adaptation_suggestions"),
        "promo_materials": final_result.get("promo_materials"),
    }

    emit("complete", "全部完成！", 1.0, {"output_keys": list(result["output"].keys())})
    return result
