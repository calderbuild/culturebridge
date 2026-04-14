"""Agent 2: Knowledge Base Matcher + Cultural Risk Assessment."""

import json
import logging

from backend.knowledge.culture_kb import lookup
from backend.llm import call_deepseek, parse_json_response

logger = logging.getLogger("culturebridge.matcher")

RISK_SYSTEM_PROMPT = """你是一位跨文化传播专家。根据以下文化元素列表和目标市场，生成文化风险报告。

对每个文化元素评估：
- risk_level: "high" / "medium" / "low"
- risk_reason: 为什么在目标市场可能有问题
- suggestion: 建议如何处理

同时给出整体风险评估 overall_risk_level 和 summary。

输出 JSON 格式。"""


def run(context: dict, scan_result: dict) -> dict:
    """Match cultural elements against knowledge base and assess risks."""
    target_lang = context["target_lang"]
    target_market = context["target_market"]
    cultural_elements = scan_result.get("cultural_elements", [])

    enriched = []
    for elem in cultural_elements:
        concept = elem.get("concept", "")
        mapping = lookup(concept, target_lang)
        if mapping:
            enriched.append(
                {
                    "concept": concept,
                    "line": elem.get("line", ""),
                    "category": elem.get("category", ""),
                    "source": "knowledge_base",
                    "mapping": mapping,
                }
            )
        else:
            enriched.append(
                {
                    "concept": concept,
                    "line": elem.get("line", ""),
                    "category": elem.get("category", ""),
                    "source": "llm_fallback",
                    "mapping": None,
                    "needs_review": True,
                }
            )

    # Generate risk report
    risk_report = _assess_risks(cultural_elements, target_market)

    kb_hits = sum(1 for e in enriched if e["source"] == "knowledge_base")
    logger.info(
        "Matched: %d/%d from knowledge base, %d fallback",
        kb_hits,
        len(enriched),
        len(enriched) - kb_hits,
    )

    return {
        "enriched_elements": enriched,
        "risk_report": risk_report,
    }


def _assess_risks(cultural_elements: list, target_market: str) -> dict:
    """Use DeepSeek to generate cultural risk assessment."""
    if not cultural_elements:
        return {
            "overall_risk_level": "low",
            "summary": "无文化元素需要评估",
            "risks": [],
        }

    market_names = {
        "us": "美国",
        "sea": "东南亚",
        "jp": "日本",
        "kr": "韩国",
        "eu": "欧洲",
        "mena": "中东北非",
    }
    market_name = market_names.get(target_market, target_market)

    elements_desc = json.dumps(
        [
            {"concept": e.get("concept"), "line": e.get("line")}
            for e in cultural_elements
        ],
        ensure_ascii=False,
    )

    messages = [
        {"role": "system", "content": RISK_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"目标市场：{market_name}\n\n文化元素：\n{elements_desc}",
        },
    ]

    response = call_deepseek(messages, max_tokens=3000, response_format="json")
    return parse_json_response(response)
