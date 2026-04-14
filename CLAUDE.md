# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**CultureBridge** — 中国文化内容出海 AI 文化顾问引擎。参加 2026 第四届"文创上海"创新创业大赛，数字文化出海+ 赛道。

定位：中国数字文化出海的三道障碍——语言（GhostCut 已解决）、声音（DubbingX 已解决）、**文化（CultureBridge 解决）**。让每个出海团队都用得起"黑神话悟空"级别的文化把关能力。

核心功能：输入任何中国文化文本内容（短剧剧本/网文章节/游戏对白/动漫台词等），通过 5 Agent Pipeline 输出六件套——适配翻译、翻译决策报告、文化风险报告、改编建议、文化注释、推广素材。

详细方案：`docs/plans/2026-04-14-001-feat-culturebridge-ai-cultural-consultant-plan.md`
调研报告：`docs/research/2026-04-14-idea-research-report.md`

## 关键时间节点

- 报名截止：2026-05-31
- 线上初评：2026-06
- 复赛：2026-07，决赛：2026-08
- Demo 完成目标：2026-05-25

## 架构

Fork 自 `github.com/calderbuild/agentcut`（多 Agent 视频生产流水线），改造为文化顾问 Pipeline：

```
输入（中国文化文本 + 目标市场 + 内容类型）
  → Agent 1: 文化元素扫描（DeepSeek V4）
  → Agent 2: 知识库匹配 + 文化风险评估（本地 JSON + LLM fallback）
  → Agent 3: 文化适配翻译 + 文化注释（Claude Sonnet 4.6）
  → Agent 4: 审校（DeepSeek V4，不同 prompt 角色）
  → Agent 5: 终稿 + 改编建议 + 推广素材（Claude Sonnet 4.6）
  → 输出六件套：翻译 + 决策报告 + 风险报告 + 改编建议 + 文化注释 + 推广素材
```

后端 Python FastAPI + SSE 实时进度，前端 HTML + Tailwind。

## 技术栈

- **后端**：Python 3.10+, FastAPI, SSE streaming
- **LLM**：DeepSeek（分析/审校）+ Claude Sonnet 4（翻译输出），统一通过 OpenRouter API 调用
- **文化知识库**：`backend/knowledge/mappings/*.json`，75 条文化概念映射，跨内容形态通用
- **前端**：HTML + Tailwind CSS（复用 AgentCut 模式）
- **部署**：Docker + Vercel

## 文化知识库

产品核心壁垒。位于 `backend/knowledge/mappings/`，分四个文件：
- `palace.json` — 宫廷（臣妾/本宫/冤家等，20 条）
- `wuxia.json` — 武侠（江湖/内力/轻功等，20 条）
- `xianxia.json` — 修仙/玄幻（渡劫/金丹/元婴等，15 条）
- `modern.json` — 都市（相亲/彩礼/面子等，20 条）

每条含 concept/context/content_types/good_translations/bad_translations/principle/cultural_note。跨内容形态通用——同一条映射在短剧/网文/游戏/动漫中均适用。

每条必须人工审核，不能 LLM 自动生成。

## Demo 场景（三场景证明通用性）

1. 古装宫廷短剧 → 英语（文化适配 vs 直译三列对比）
2. 修仙网文 → 英语（术语一致性 + 文化注释自动生成）
3. 仙侠游戏对白 → 英语（角色语气适配 + 文化风险扫描）

## 可复用代码来源

| 项目 | 复用部分 |
|------|--------|
| `agentcut` | Pipeline 编排、SSE、Job 管理、前端框架、Agent 基类 |
| `SEO_Agent` | 关键词研究逻辑（用于推广素材 hashtag） |
