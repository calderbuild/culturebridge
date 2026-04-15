"""Agent 0: Content Creator — generates Chinese cultural content from user intent (beginner mode)."""

import logging

from backend.llm import call_deepseek, parse_json_response

logger = logging.getLogger("culturebridge.content_creator")

SYSTEM_PROMPT = """你是一位中国文化内容创作专家。你的任务是根据用户意图，创作一段富含中国文化元素的中文内容。

创作要求：
1. 内容长度 300-500 字
2. 必须包含具体的文化术语和概念（如称谓、典故、习俗、意象），不能写泛泛的文化介绍
3. 根据内容类型选择合适的格式：
   - drama（短剧）：写成对白形式，包含角色名、台词、动作描写
   - novel（网文）：写成叙事散文形式，包含心理描写和环境渲染
   - game（游戏）：写成角色对白形式，包含技能/道具名称
   - general（通用）：写成短文/随笔形式
4. 根据目标平台调整长度：
   - tiktok/instagram：偏短，300 字左右
   - youtube/reddit：可以更长，400-500 字
   - twitter：精炼，300 字以内

输出 JSON 格式：
{
  "generated_content": "创作的中文内容",
  "content_type": "内容类型",
  "topic": "主题概括（一句话）",
  "cultural_elements_hint": ["文化元素1", "文化元素2", ...]
}

cultural_elements_hint 列出内容中包含的主要文化概念关键词（如"臣妾"、"渡劫"、"江湖"等），用于后续文化知识库匹配。

仅输出 JSON，不要解释。"""


def run(context: dict) -> dict:
    """Generate Chinese cultural content from user intent."""
    intent = context["intent"]
    content_type = context.get("content_type", "general")
    target_platforms = context.get("target_platforms", [])
    target_lang = context.get("target_lang", "en")
    target_market = context.get("target_market", "us")

    platform_hint = ""
    if target_platforms:
        platform_hint = f"目标发布平台：{', '.join(target_platforms)}。"

    type_label = {
        "drama": "短剧剧本台词",
        "novel": "网文章节",
        "game": "游戏角色对白",
        "general": "文化短文",
    }.get(content_type, "文化短文")

    user_message = (
        f"请创作一段{type_label}。\n\n"
        f"用户意图：{intent}\n"
        f"内容类型：{content_type}\n"
        f"目标语言：{target_lang}\n"
        f"目标市场：{target_market}\n"
        f"{platform_hint}"
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    response = call_deepseek(messages, max_tokens=4000, response_format="json")
    result = parse_json_response(response)

    logger.info(
        "Created content: type=%s, topic=%s, hints=%d",
        result.get("content_type", content_type),
        result.get("topic", "unknown"),
        len(result.get("cultural_elements_hint", [])),
    )
    return result
