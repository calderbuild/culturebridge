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

## 常用命令

```bash
# 安装依赖
pip install -r backend/requirements.txt

# 启动开发服务器
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 语法检查
python -m py_compile backend/main.py backend/pipeline.py

# 运行单个模块
python -c "from backend.agents import cultural_scanner; print('OK')"
```

前端访问 http://localhost:8000，静态文件由 FastAPI 直接托管（`frontend/index.html`）。

## 架构

Fork 自 `github.com/calderbuild/agentcut`（多 Agent 视频生产流水线），改造为文化顾问 Pipeline：

```
输入（中国文化文本 + 目标市场 + 内容类型）
  → Agent 0: 内容生成（可选，小白模式）  backend/agents/content_creator.py
  → Agent 1: 文化元素扫描（DeepSeek）     backend/agents/cultural_scanner.py
  → Agent 2: 知识库匹配 + 风险评估         backend/agents/kb_matcher.py
  → Agent 3: 文化适配翻译（Claude）        backend/agents/translator.py
  → Agent 4: 审校（DeepSeek）              backend/agents/reviewer.py
  → Agent 5: 终稿 + 推广素材（Claude）     backend/agents/finalizer.py
  → 输出六件套
```

后端 Python FastAPI + SSE 实时进度，前端 HTML + Tailwind。

关键容错设计：Scanner 和 Translator 是关键 Agent（失败则终止），Matcher/Reviewer/Finalizer 可降级（失败返回部分结果）。

## API 端点

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/create` | POST | 创建翻译任务（JSON body: content, content_type, target_lang, target_market） |
| `/api/create-srt` | POST | 上传 SRT 字幕文件创建任务（multipart form） |
| `/api/create-from-intent` | POST | 小白模式——根据意图自动生成内容（触发 Agent 0） |
| `/api/status/{job_id}` | GET | 查询任务状态 |
| `/api/stream/{job_id}` | GET | SSE 实时进度流 |
| `/api/health` | GET | 健康检查 |

## LLM 路由

通过 OpenRouter 统一调用，分工：
- **DeepSeek V4**（`backend/llm.py:call_deepseek`）：Agent 1 扫描、Agent 2 匹配、Agent 4 审校——中文理解强、成本低
- **Claude Sonnet 4**（`backend/llm.py:call_claude`）：Agent 3 翻译、Agent 5 终稿——多语言输出质量高

## 技术栈

- **后端**：Python 3.10+, FastAPI, SSE streaming
- **LLM**：DeepSeek（分析/审校）+ Claude Sonnet 4（翻译输出），统一通过 OpenRouter API 调用
- **文化知识库**：`backend/knowledge/mappings/*.json`，90 条文化概念映射，跨内容形态通用
- **图片生成**：Gemini Imagen 4 API
- **平台发布**：X/Twitter OAuth 1.0a + YouTube OAuth 2.0 + TikTok Content Posting API + Instagram Graph API
- **前端**：HTML + Tailwind CSS，三步向导（选择→处理→发布）
- **部署**：需要公网 URL（TikTok/Instagram 验证需要）

## 开发约定

- 产品方向确认后锁定执行，不反复改
- 赛题关键词必须逐词对应到产品功能
- 前端交互优先为小白设计（引导式，不是专业工具形态）
- API 凭证全部在 `.env` 中（已 gitignore），包括 OpenRouter、Gemini、X、YouTube、TikTok

## 文化知识库

产品核心壁垒。位于 `backend/knowledge/mappings/`，分四个文件：
- `palace.json` — 宫廷（臣妾/本宫/冤家等，23 条）
- `wuxia.json` — 武侠（江湖/内力/轻功等，20 条）
- `xianxia.json` — 修仙/玄幻（渡劫/金丹/元婴等，27 条）
- `modern.json` — 都市（相亲/彩礼/面子等，20 条）

每条含 concept/context/content_types/good_translations/bad_translations/principle/cultural_note。跨内容形态通用——同一条映射在短剧/网文/游戏/动漫中均适用。

每条必须人工审核，不能 LLM 自动生成。

## Demo 场景（三场景证明通用性）

测试数据位于 `demo/scenarios/`：
1. `palace_drama.txt` — 古装宫廷短剧（文化适配 vs 直译三列对比）
2. `xianxia_novel.txt` — 修仙网文（术语一致性 + 文化注释自动生成）
3. `game_dialogue.txt` — 仙侠游戏对白（角色语气适配 + 文化风险扫描）

## 可复用代码来源

| 项目 | 复用部分 |
|------|--------|
| `agentcut` | Pipeline 编排、SSE、Job 管理、前端框架、Agent 基类 |
| `SEO_Agent` | 关键词研究逻辑（用于推广素材 hashtag） |
