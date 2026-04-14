"""Agent 4: Review — structured quality check with a different persona."""

import json
import logging

from backend.llm import call_deepseek, parse_json_response

logger = logging.getLogger("culturebridge.reviewer")

SYSTEM_PROMPT = """你是一位在美国生活 20 年的华裔影视字幕翻译专家。你精通中英双语和两种文化。

你的任务是审校以下翻译，找出问题。你只挑问题，不重写翻译。

审校维度（按优先级）：
1. 文化冲突：翻译是否引入了目标市场不存在或冒犯的文化概念？
2. 术语一致性：同一个文化概念在不同句子中是否翻译一致？
3. 翻译腔：英文是否自然？是否读起来像翻译而非原生英文？
4. 情感偏差：翻译是否保留了原文的情感强度和语气？
5. 角色语气一致：同一角色的说话风格是否前后一致？
6. 遗漏：是否有重要文化信息被丢失？

翻译指南（知识库提供）：
{translation_guide}

输出 JSON：
{{
  "issues": [
    {{
      "line_number": 1,
      "dimension": "文化冲突/术语一致性/翻译腔/情感偏差/角色语气/遗漏",
      "severity": "high/medium/low",
      "problem": "问题描述",
      "suggestion": "修改建议"
    }}
  ],
  "overall_quality": "excellent/good/needs_improvement",
  "summary": "整体评价一句话"
}}"""


def run(context: dict, translation_result: dict, match_result: dict) -> dict:
    """Review translation quality with structured checklist."""
    translations = translation_result.get("translations", [])

    # Build translation guide summary for reviewer context
    guide_entries = []
    for elem in match_result.get("enriched_elements", []):
        mapping = elem.get("mapping")
        if mapping:
            guide_entries.append(
                f"- {elem['concept']}: 正确={', '.join(mapping.get('good', []))} | "
                f"错误={', '.join(mapping.get('bad', []))}"
            )
    guide_str = "\n".join(guide_entries) if guide_entries else "无特定指南"

    # Format translations for review
    review_lines = []
    for t in translations:
        review_lines.append(
            f"第{t.get('line_number', '?')}句\n"
            f"  原文: {t.get('original', '')}\n"
            f"  译文: {t.get('translation', '')}"
        )
    review_text = "\n\n".join(review_lines)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT.format(translation_guide=guide_str),
        },
        {"role": "user", "content": f"请审校以下翻译：\n\n{review_text}"},
    ]

    response = call_deepseek(messages, max_tokens=4000, response_format="json")
    result = parse_json_response(response)

    issues = result.get("issues", [])
    logger.info(
        "Review: %d issues found, overall=%s",
        len(issues),
        result.get("overall_quality", "?"),
    )

    return result
