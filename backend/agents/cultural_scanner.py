"""Agent 1: Cultural Element Scanner — extracts cultural concepts, characters, and risk areas."""

import json
import logging

from backend.knowledge.culture_kb import get_all_concept_keys
from backend.llm import call_deepseek, parse_json_response

logger = logging.getLogger("culturebridge.scanner")

SYSTEM_PROMPT = """你是一位中国文化内容分析专家。你的任务是分析输入的中文文本内容，提取其中的文化元素。

你需要输出以下信息（JSON 格式）：

1. characters: 角色列表，每个角色包含 name（名字）、role（身份/关系）、speech_style（说话风格）
2. cultural_elements: 文化元素列表，每个包含 concept（概念）、line（出现的原文）、category（类别：称谓/术语/典故/习俗/意象）
3. high_risk_lines: 高风险翻译行，包含 line（原文）、risk_reason（为什么难翻译）
4. tone: 整体情感基调（如：庄重、幽默、悲伤、热血）
5. genre_features: 内容类型特征（宫廷/武侠/修仙/都市/其他）

已知文化概念列表（优先从此列表中匹配）：
{concept_keys}

仅输出 JSON，不要解释。"""


def run(context: dict) -> dict:
    """Scan content for cultural elements."""
    content = context["content"]
    content_type = context["content_type"]

    concept_keys = get_all_concept_keys()
    keys_str = "、".join(concept_keys) if concept_keys else "（知识库为空）"

    type_hint = {
        "drama": "这是一段短剧/影视剧本台词。",
        "novel": "这是一段网络小说章节。",
        "game": "这是一段游戏角色对白。",
    }.get(content_type, "")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(concept_keys=keys_str)},
        {"role": "user", "content": f"{type_hint}\n\n请分析以下内容：\n\n{content}"},
    ]

    response = call_deepseek(messages, max_tokens=4000, response_format="json")
    result = parse_json_response(response)

    logger.info(
        "Scanned: %d cultural elements, %d high-risk lines, %d characters",
        len(result.get("cultural_elements", [])),
        len(result.get("high_risk_lines", [])),
        len(result.get("characters", [])),
    )
    return result
