---
title: "feat: CultureBridge 2.0 — 一站式文化内容出海工作站"
type: feat
status: active
date: 2026-04-15
supersedes: 2026-04-15-001-feat-polish-to-perfection-plan.md
competition: 2026 第四届"文创上海"创新创业大赛
track: 数字文化出海+
---

# CultureBridge 2.0 — 一站式文化内容出海工作站

## Overview

从"翻译工具"升级为"全流程出海工作站"。用户从创意到发布全程不离开平台：

```
小白：说一句话 → AI 生成内容 → 文化适配翻译 → 多平台素材 → 一键发布到 TikTok/IG/YouTube/X
专业：粘贴剧本 → 文化适配翻译 → 多平台素材 → 一键发布
```

核心价值主张从"帮你翻译"升级为"帮你出海"。赛题精准命中"构建国际化服务生态""全球化表达与分众化传播""数字内容创制与传播"。

## Problem Frame

### 现状（V1 的三个根本问题）

1. **只做翻译没做出海** — 翻译完用户还得自己去各平台手动发布，流程断裂
2. **小白不知道怎么用** — 默认用户有现成内容可粘贴，没有内容的人无法起步
3. **没有产出实质价值** — 翻译报告不等于内容出海，文化内容并没有真正到达海外受众

### 升级后解决的问题

- 小白用户："我想让外国人了解中国茶文化" → 平台帮你生成内容、翻译、发布到 TikTok
- 专业用户：粘贴剧本 → 平台帮你翻译、生成各平台推广素材、直接发布
- **文化内容真正出海** — 不是拿到报告然后呢，而是内容真的发布到了海外平台

## Requirements Trace

### 全流程需求

- F1. **双模式入口**：小白模式（自然语言描述意图 → AI 生成内容）+ 专业模式（粘贴/上传内容）
- F2. **内容生成 Agent**：根据用户意图自动生成中文文化脚本（300-500 字）
- F3. **文化适配翻译**：现有 5 Agent Pipeline（保持不变）
- F4. **多平台素材生成**：针对每个平台的格式要求生成定制化内容
- F5. **平台预览**：在发布前预览每个平台上内容长什么样
- F6. **一键发布**：OAuth 授权后直接发布到海外平台（Demo 阶段模拟发布）
- F7. **引导式工作流 UI**：Step-by-step 向导，每步一屏，小白也能用

### 平台覆盖

- P1. TikTok — 竖版短文案 + hashtag + 封面建议
- P2. Instagram — 帖子文案 + hashtag + 轮播建议
- P3. YouTube — 视频标题 + 描述 + 标签 + 章节时间戳
- P4. X/Twitter — 推文 + thread 拆解
- P5. Reddit — 社区适配帖子（r/CDrama, r/noveltranslations）

### 非功能需求

- N1. 引导式 UI，3 步完成（选模式 → 内容处理 → 预览发布）
- N2. 全流程总耗时 < 5 分钟（含内容生成）
- N3. 零门槛首次体验（不注册也能跑 Demo 场景）

## Scope Boundaries

### In Scope

- 双模式入口（小白 + 专业）
- 内容生成 Agent（Agent 0）
- 多平台素材生成（增强 Agent 5）
- 平台发布预览界面（模拟各平台 UI 展示效果）
- 引导式工作流前端（Step-by-step）
- 文化 X 光保留（在翻译步骤中展示）

### Out of Scope（Demo 阶段）

- 真实 OAuth 平台授权（需要 API 审批周期）
- 真实发布到平台（Demo 阶段模拟发布，显示"已发布"状态）
- 用户账号系统
- 发布效果追踪/分析

### Demo 策略

Demo 现场演示时，"发布"按钮触发模拟发布流程：
- 显示平台 OAuth 授权页面（模拟）
- 显示发布中动画
- 显示"已发布成功"+ 模拟的平台链接
- 评委能看到完整的从创意到发布的全流程，理解产品形态

赛后接入真实 API 时改动极小——只需替换模拟发布函数为真实 API 调用。

## Key Technical Decisions

- **架构**：在现有 Pipeline 前加 Agent 0（内容生成），在 Agent 5 后加发布模块。Pipeline 核心不变
- **前端**：从分屏工作区改为 Step-by-step 向导流程。3 步：输入 → 处理 → 发布
- **平台素材**：Agent 5 Finalizer 的 prompt 按平台分别生成，每个平台有独立的格式约束
- **模拟发布**：前端实现，不需要后端 API。用各平台的 UI 样式展示"发布预览"
- **LLM**：Agent 0 内容生成用 DeepSeek（中文生成质量好、成本低）

## High-Level Technical Design

> *Directional guidance, not implementation specification.*

```
用户流程（3 步向导）：

Step 1: 选择模式
  ┌──────────────────┐  ┌──────────────────┐
  │   小白模式        │  │   专业模式        │
  │ "我想推广端午节"   │  │  粘贴剧本/上传SRT │
  │ AI 帮你生成内容    │  │  直接进入翻译     │
  └────────┬─────────┘  └────────┬─────────┘
           │                     │
           v                     │
  [Agent 0: 内容生成]            │
  DeepSeek 生成中文脚本          │
           │                     │
           └──────────┬──────────┘
                      v
Step 2: 文化适配处理（现有 Pipeline）
  Agent 1-5 串行执行
  实时展示文化 X 光效果
  输出：翻译 + 决策报告 + 风险报告 + 文化注释
                      │
                      v
Step 3: 出海发布
  ┌─────┬─────┬─────┬─────┬─────┐
  │TikTk│ IG  │ YT  │  X  │Rdit │  ← 平台 Tab
  └──┬──┴──┬──┴──┬──┴──┬──┴──┬──┘
     v     v     v     v     v
  [平台预览卡片]
  模拟各平台 UI 展示效果
  每个平台：预览 + "发布"按钮
```

后端 Pipeline：
```
Agent 0 (新增): 内容生成 ← 仅小白模式触发
  → Agent 1: 文化扫描 (现有)
  → Agent 2: 知识库匹配 (现有)
  → Agent 3: 翻译 (现有)
  → Agent 4: 审校 (现有)
  → Agent 5: 终稿 + 多平台素材 (增强)
       输出增加：platform_content = {
         tiktok: { caption, hashtags, cover_suggestion },
         instagram: { caption, hashtags, carousel_texts },
         youtube: { title, description, tags, chapters },
         twitter: { tweets: [tweet1, tweet2, tweet3] },
         reddit: { title, body, subreddit_suggestion }
       }
```

## Implementation Units

### Phase A: 后端增强

- [ ] **Unit 1: Agent 0 — 内容生成 Agent**

**Goal:** 小白模式下根据用户自然语言意图生成中文文化脚本

**Requirements:** F1, F2

**Dependencies:** None

**Files:**
- Create: `backend/agents/content_creator.py`
- Modify: `backend/pipeline.py` — 增加 content_creation 阶段（可选）
- Modify: `backend/main.py` — 新增 API 端点接受意图文本
- Test: `tests/test_content_creator.py`

**Approach:**
- LLM: DeepSeek（中文生成）
- 输入：用户意图（如"给美国人介绍端午节"）+ 内容类型 + 目标平台
- 输出：300-500 字的中文文化脚本，适合后续翻译
- Prompt 包含场景模板引导（确保生成的内容有文化深度，不是泛泛而谈）
- 生成的脚本直接传入现有 Pipeline 的 Agent 1

**Test scenarios:**
- Happy path: 输入"端午节 TikTok 美国" → 生成包含龙舟/粽子/屈原的中文脚本
- Happy path: 输入"功夫文化 YouTube" → 生成适合长视频的文化脚本
- Edge case: 模糊输入"中国文化" → 提供 3 个具体方向建议让用户选择
- Error path: 输入非文化主题 → 友好提示建议文化相关主题

**Verification:** 生成的脚本能被现有 Pipeline 正确处理

---

- [ ] **Unit 2: 增强 Agent 5 — 多平台素材生成**

**Goal:** 为每个海外平台生成格式定制的推广内容

**Requirements:** F4, P1-P5

**Dependencies:** None（可与 Unit 1 并行）

**Files:**
- Modify: `backend/agents/finalizer.py` — 增加 `_generate_platform_content` 方法
- Test: `tests/test_finalizer.py`

**Approach:**
- 在现有 Finalizer 基础上增加 platform_content 输出
- 每个平台一次独立 LLM 调用（保证格式准确）：
  - TikTok: 150 字以内文案 + 5-10 个 hashtag + 封面建议文字
  - Instagram: 2200 字以内文案 + 30 个 hashtag + 3 条轮播文案
  - YouTube: 标题(100字) + 描述(5000字) + 15 个标签 + 章节时间戳建议
  - X/Twitter: 3 条独立推文（280 字限制）+ thread 版本
  - Reddit: 标题 + 正文 + 推荐 subreddit
- 每个平台的 prompt 包含该平台的格式约束和风格要求

**Test scenarios:**
- Happy path: 宫廷剧输入 → TikTok 文案 < 150 字且含 hashtag
- Happy path: 修仙网文 → Reddit 帖子推荐 r/noveltranslations
- Edge case: 短内容（3 行）→ 各平台素材仍能正常生成

**Verification:** 每个平台的输出严格符合该平台字数限制和格式要求

---

- [ ] **Unit 3: 后端 API 增强**

**Goal:** 支持双模式（小白/专业）+ 平台内容输出

**Requirements:** F1, F7

**Dependencies:** Unit 1, Unit 2

**Files:**
- Modify: `backend/main.py` — 新增 `/api/create-from-intent` 端点
- Modify: `backend/pipeline.py` — pipeline 输出增加 platform_content

**Approach:**
- 新端点 `POST /api/create-from-intent`：接受 `{intent: string, platforms: string[], target_lang: string}`
- 内部流程：Agent 0 生成内容 → 现有 Pipeline → 返回翻译 + platform_content
- 现有 `/api/create` 端点保留（专业模式）
- SSE 事件增加 Agent 0 的状态推送

**Test scenarios:**
- Happy path: intent="端午节 TikTok" → 返回含 platform_content.tiktok 的结果
- Integration: SSE 流正确推送 6 个 Agent 的进度（Agent 0 + Agent 1-5）

**Verification:** 两个端点都能正常工作，输出包含 platform_content

---

### Phase B: 前端重构 — 引导式工作流

- [ ] **Unit 4: Step 1 — 模式选择 + 输入界面**

**Goal:** 用户进入平台后看到两个模式入口

**Requirements:** F1, F7, N1, N3

**Dependencies:** Unit 3

**Files:**
- Modify: `frontend/index.html` — 完全重写为向导流程

**Approach:**
- 首屏展示两个模式卡片：
  - 小白模式："告诉 AI 你想推广什么" + 输入框 + 场景模板快捷选择（端午节/功夫/茶文化/宫廷剧...）
  - 专业模式："粘贴你的剧本或小说" + 文本框 + SRT 上传
- 底部保留 Demo 预设按钮
- 选择模式后平滑过渡到 Step 2

**Test expectation:** none — 纯 UI，视觉验证

---

- [ ] **Unit 5: Step 2 — 文化适配处理界面**

**Goal:** 保留文化 X 光效果，展示 Pipeline 处理过程

**Requirements:** F3, N2

**Dependencies:** Unit 4

**Files:**
- Modify: `frontend/index.html`

**Approach:**
- 保留现有分屏布局（左：原文高亮 / 右：翻译流入）
- 顶部进度条显示当前步骤（Step 1 ✓ → **Step 2** → Step 3）
- Pipeline Agent 进度用小圆点展示（保留现有设计）
- 完成后自动过渡到 Step 3
- 文化卡片悬停交互保留

**Test expectation:** none — 纯 UI

---

- [ ] **Unit 6: Step 3 — 出海发布界面（核心创新）**

**Goal:** 多平台预览 + 模拟发布 — 全流程闭环

**Requirements:** F4, F5, F6, P1-P5

**Dependencies:** Unit 2, Unit 5

**Files:**
- Modify: `frontend/index.html`

**Approach:**
- 平台 Tab 栏：TikTok | Instagram | YouTube | X | Reddit
- 每个 Tab 内：
  - **平台预览卡片**：模拟该平台的真实 UI 样式展示内容
    - TikTok: 手机竖屏样式，文案 + hashtag + 评论区预览
    - Instagram: 方形帖子样式，文案 + hashtag + 点赞数模拟
    - YouTube: 视频卡片样式，标题 + 描述折叠 + 标签
    - X: 推文卡片样式，头像 + 文案 + 互动数
    - Reddit: 帖子样式，标题 + 正文 + subreddit 标签
  - **"发布到 TikTok" 按钮**：点击后触发模拟发布流程
    - 弹出模拟 OAuth 授权窗口（"连接你的 TikTok 账号"）
    - 授权后显示发布进度动画
    - 完成后显示"已发布" + 模拟链接
  - **编辑按钮**：用户可以在预览中修改文案后再发布
- 底部统计："已准备 5 个平台的出海素材"

**这是 Demo 的杀手功能**：评委看到内容从中文剧本 → 翻译 → 直接"发布"到 TikTok 预览界面，全程一站式。

**Test expectation:** none — 纯 UI

---

### Phase C: Demo 场景

- [ ] **Unit 7: 小白模式 Demo 场景**

**Goal:** 完整演示"什么都不懂的小白 → 内容出海"的全流程

**Requirements:** F1, F2

**Dependencies:** Unit 1-6 全部完成

**Files:**
- Create: `demo/scenarios/beginner_duanwu.json` — 小白模式："端午节推广给美国人"
- Modify: `frontend/index.html` — 小白模式 Demo 预设

**Approach:**
- 预设意图："我想让美国年轻人了解端午节文化"
- 目标平台：TikTok + Instagram
- 完整演示：输入意图 → AI 生成中文脚本 → 文化 X 光扫描 → 翻译 → TikTok/IG 素材预览 → 模拟发布
- 录制 Demo 视频用

**Verification:** 全流程 < 5 分钟完成，小白用户零操作门槛

---

## Phased Delivery

### Phase A: 后端增强（2-3 天）
- Unit 1: Agent 0 内容生成
- Unit 2: Agent 5 多平台素材增强
- Unit 3: API 端点增强
- 可与 Phase B 部分并行

### Phase B: 前端重构（3-4 天）
- Unit 4: Step 1 模式选择
- Unit 5: Step 2 文化适配（复用现有）
- Unit 6: Step 3 出海发布预览（核心工作量）

### Phase C: Demo 打磨（1-2 天）
- Unit 7: 小白 Demo 场景 + 视频录制

## Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| 平台预览 UI 太假，评委看出是模拟的 | Medium | Medium | 用真实的平台 UI 样式（颜色/字体/布局），加"Demo 预览"标注，坦诚是模拟发布 |
| Agent 0 生成的内容质量差 | Medium | High | Demo 场景使用预生成+人工校准的脚本作为 fallback |
| 前端重构工作量超预期 | Medium | Medium | Step 2 大量复用现有文化 X 光代码；Step 3 的平台预览用 Tailwind 快速搭建 |
| 多平台素材格式不符合真实要求 | Low | Medium | 每个平台的 prompt 包含严格的格式约束（字数限制、hashtag 数量等） |

## Success Metrics

| 指标 | 目标 |
|------|------|
| 小白全流程 | 从意图到"发布" < 5 分钟 |
| 专业全流程 | 从粘贴到"发布" < 3 分钟 |
| 平台覆盖 | 5 个平台都有素材预览 |
| Demo 效果 | 评委能理解"一站式出海"的价值主张 |

## 比赛叙事（升级版）

> 中国数字文化出海，不缺好内容，缺的是从创意到出海的一站式工具。
>
> 现有工具要么只做翻译（GhostCut），要么只做发布（Hootsuite），没有一个工具能打通"文化适配 + 多平台分发"的全流程。
>
> CultureBridge 是中国文化内容出海的一站式工作站：
> - 不会写？AI 帮你生成文化内容
> - 怕翻错？文化知识库确保翻译准确
> - 不知道发哪？自动适配 TikTok/Instagram/YouTube/X/Reddit 五个平台
> - 不会操作？三步完成，从创意到发布
>
> 让每一个想讲中国故事的人，都能把故事讲给全世界听。

## Sources & References

- 现有代码库：`backend/agents/*.py`, `backend/pipeline.py`, `frontend/index.html`
- 现有方案：`docs/plans/2026-04-14-001-feat-culturebridge-ai-cultural-consultant-plan.md`
- TikTok Content Posting API: https://developers.tiktok.com/products/content-posting-api/
- Instagram Graph API: https://developers.facebook.com/docs/instagram-platform/content-publishing/
- YouTube Data API v3: https://developers.google.com/youtube/v3/guides/uploading_a_video
- 竞品 UX 调研：GhostCut, Viki, Duolingo, Grammarly, Perplexity, Runway ML
