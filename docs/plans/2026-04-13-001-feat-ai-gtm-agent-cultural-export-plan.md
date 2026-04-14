---
title: "feat: CultureBridge — 短剧出海 AI 文化适配翻译引擎"
type: feat
status: active
date: 2026-04-13
competition: 2026 第四届"文创上海"创新创业大赛
track: 数字文化出海+
track_partner: 临港科创城（滴水湖 AI 创新港科创社区）
deadline_register: 2026-05-31
deadline_final: 2026-08
---

# CultureBridge — 短剧出海 AI 文化适配翻译引擎

## Overview

帮中国短剧出海团队把中文剧本/字幕翻译成"老外真正看得懂"的多语种版本。不是逐句直译，而是理解文化语境后的创造性再表达。同时生成海外推广素材（剧情简介 + 社媒帖子）。

核心差异化：**现有工具的文化适配是附加功能，CultureBridge 以可解释的文化知识库为核心引擎。** GhostCut/HeyGen 已加入文化适配相关功能，但没有提供"翻译决策报告"——逐条解释每个文化梗为什么这样翻、知识库依据是什么。这种可追溯、可解释的翻译过程是我们的差异化。

## Problem Frame

### 一句话痛点

短剧出海翻译有两个极端：AI 直译太差（完播率暴跌至 20%），本土重拍太贵（$150,000-300,000/部）。**中间缺少"文化适配"层的工具化方案。**

### 数据支撑

- 短剧出海 2025 年海外内购收入约 21.6 亿美元（中国出海 APP 占 95%），全口径（含 IAA、订阅等）约 40 亿美元
- 行业已证明直译失败："Most apps simply add subtitles... unconvincing to Western viewers. Retention and payment conversion proved poor"（Medium 行业分析）
- 海外原创拍摄成本：$150,000-300,000/部（洛杉矶），AI 翻译+配音方案仅需 $300-700/部
- 70% 翻译团队已用"AI + 人工"模式，但文化适配层没有工具化
- Viki 社区字幕组研究：70% 人工编辑精力用于修复文化隐喻和历史术语（Nature 2025）
- 修仙剧每集平均含 4.2 个道教/佛教术语，西方观众文化折损率 58%（华语观众仅 12%）
- 从擦除字幕到翻译成片要半个月
- 腾讯微视案例：文化适配前完播率 20%，适配后 83%——翻译质量直接决定商业结果

### 为什么现有工具解决不了

| 工具 | 能做什么 | 不能做什么 |
|------|--------|----------|
| Google Translate | 字面翻译 | 文化语境、情感、角色关系 |
| HeyGen | AI 配音 + Precision Mode 上下文感知翻译 | 无文化知识库，无翻译决策报告 |
| GhostCut（鬼手剪） | 短剧视频全链路（字幕擦除+翻译+配音），已有 multi-agent review | 无可解释的文化映射过程，按视频分钟计费 |
| Rask.ai | AI 配音 + 术语词典 + 可定制 glossary | 文化适配深度有限 |
| 火山引擎 | 翻译 + 配音 + 审核一体化 | 面向大厂，中小团队用不起 |
| 人工翻译 | 质量高 | 慢（半个月）、贵（$50-100/千字） |
| **CultureBridge** | **文化知识库驱动翻译 + 翻译决策报告 + 推广素材** | 配音/唇形同步（不做） |

### 赛题对应

| 赛题关键词 | 产品功能 |
|---------|---------|
| 网剧出海 | 专门服务短剧出海翻译 |
| 数字内容创制 | AI 创造性翻译 + 推广素材生成 |
| 数字内容传播 | 自动生成海外社媒推广内容 |
| 优质文化内容创造性转化 | 文化适配翻译（不是直译） |
| 运用人工智能新技术 | 多 Agent Pipeline + 文化知识图谱 |
| 打造具有全球吸引力的中国文化 IP | 帮中国 IP 准确触达全球受众 |

## Requirements Trace

- R1. 5 步翻译 Pipeline（分析→查库→初译→审校→终稿），翻译质量 90 分以上
- R2. 文化知识库：100 条核心文化概念映射（宫廷/武侠/修仙/都市），含正例+反例
- R3. 多语种：英/日/韩 三个主要出海语种
- R4. 输入格式：纯文本剧本 + SRT 字幕文件
- R5. 输出：翻译结果 + 翻译决策报告（每个文化梗的适配解释）+ 置信度评分
- R6. 推广素材：多语种剧情简介 + 3 条社媒帖子 + hashtag 建议
- R7. 实时可视化：Agent 工作流进度面板（SSE）
- R8. 单次任务成本 < $0.30/千字
- R9. Demo 在 2026-05-25 前完成

## Scope Boundaries

### In Scope

- 5 Agent 翻译 Pipeline（核心，90% 精力）
- 文化知识库（100 条，人工打磨）
- 推广素材 Agent（轻量，10% 精力）
- SRT 解析和输出（保持时间轴）
- Web Dashboard（复用 AgentCut 前端）
- 2 个 Demo 场景 + 对比展示（CultureBridge vs Google Translate）

### Out of Scope

- 配音 / 唇形同步 / 视频处理
- 字幕硬烧入视频
- 广告投放 / 电商对接
- 用户系统 / 计费
- 内容合规审核

## Context & Research

### 竞品空白验证

调研确认：多个竞品已在 2025-2026 年加入文化适配相关功能，但**没有产品以"可解释的文化知识库"为核心引擎**。

- **GhostCut（最直接竞品）**：短剧视频翻译头号工具，已宣传 "multi-agent review for culturally fluent translations"，按视频分钟计费（$0.1/分钟）。但文化适配是黑盒，用户看不到翻译决策过程
- **HeyGen**：2025 年推出 Precision Mode，上下文感知翻译，但核心业务仍是视频配音和数字人
- **Rask.ai**：支持术语词典和可定制 glossary，但文化适配深度有限
- **火山引擎**：一体化方案但面向头部公司
- **智译通**：宣称"情感共鸣"但本质是传统 TMS
- **录咖 AI（RecCloud）**：国内短剧出海翻译一站式方案，宣传"本土化而非字面化"

**CultureBridge 的差异化不是"唯一做文化适配的"，而是"唯一让翻译过程可解释的"**：翻译决策报告逐条展示每个文化梗的知识库依据、正反例对比、适配原则。这是评委能直观感受到的壁垒。

### PMF 验证（2026-04-14 调研）

#### 正面信号

- **痛点真实**：翻译质量直接决定完播率和付费转化。腾讯微视案例（20%→83%）、知乎从业者"翻译质量直接决定播放量"
- **市场规模**：海外短剧收入 23.8 亿美元（光大证券），翻译剧占 80-90%（DramaBox 数据）
- **文化适配是公认难题**：修仙/武侠术语 58% 文化折损率；Viki 社区 70% 编辑精力用于文化修复
- **付费意愿**：人工翻译 200-300 元/分钟，AI+人工 50 元/分钟，纯 AI 0.1-0.7 元/分钟
- **从业者呼声**：小红书"出海短剧本地化，根本不是翻译"、"中式翻译劝退老外？血亏百万教训"
- **Reddit 海外观众**：r/CDrama 大量帖子吐槽古装剧翻译质量，最推荐 Viki（有文化注释）

#### 负面信号 / 风险

- **GhostCut 已占 70% 头部客户**，日处理 10 万集，150 万+用户，定价 $0.1/分钟
- **头部自建**：容量短剧自主研发 AI 翻译平台（2 天→3 小时）
- **纯翻译非独立产品**：客户需要一站式（去字幕+翻译+配音），单卖翻译引擎购买动力不足
- **翻译剧 ARPU 低**：10% 本土剧贡献 75-83% 收入，行业趋势从翻译走向本土化制作

#### 定位策略

不与 GhostCut 抢"批量快速翻译"（已输），聚焦 **精品文化适配翻译**：
1. **翻译决策报告（唯一差异化）**——竞品都是黑盒翻译，我们展示每个文化梗的知识库依据
2. **古装/仙侠/修仙等高文化密度剧种**——AI 通用翻译最弱的环节
3. **精品剧翻译，非批量翻译**——面向平台首页推荐剧、重点推广剧

#### 赛后 PMF 路径

| 路径 | 定位 | 优势 | 风险 |
|------|------|------|------|
| **A: API 上游** | 把文化适配能力以 API 输出给 GhostCut 等平台 | 聚焦核心壁垒，不需要全流程 | 竞品自研 |
| **B: 译员效率工具** | 帮人工翻译公司（TXV/Etrans）提升文化适配质量 | 避开正面竞争 | 天花板低 |
| **C: 本土化剧本改编** | 从"翻译"升级为"文化改编方案生成" | ARPU 高 6 倍+，竞争少 | 技术难度大 |

#### 数据来源

- 光大证券研报（海外短剧市场收入 23.8 亿美元）
- 21 经济网（DramaBox 翻译剧占比 90%+，容量短剧 AI 翻译平台）
- Etrans 深圳创译（腾讯微视短剧文化适配案例）
- Nature 2025（Viki 社区字幕组工作流研究）
- GhostCut 官网（70% 头部客户，日处理 10 万集）
- 知乎"跨境小k"、"火星翻译"（从业者视角）
- 小红书搜索（"短剧出海翻译痛点"相关帖子）
- Reddit r/CDrama, r/CShortDramas（海外观众翻译质量反馈）

### 可复用代码

| 现有项目 | 复用部分 | 改动量 |
|---------|--------|------|
| `agentcut` | Pipeline 编排、SSE 进度流、Job 管理、前端框架 | 替换 Agent 定义 |
| `agentcut` | FastAPI 后端、错误处理、自动清理 | 几乎不改 |
| `SEO_Agent` | 关键词研究逻辑 | 用于推广素材的 hashtag 建议 |

### 往届获奖模式匹配

- 互影科技（首届）：技术赋能内容 → CultureBridge 用 AI 赋能翻译
- 有源文化（二届）：平台化工具 → CultureBridge 是翻译工具平台
- 第三届大量 AI 项目 → AI 是当前评审偏好

## Key Technical Decisions

- **LLM 策略**：DeepSeek V4 做分析和审校（中文理解强、成本极低 $0.30/M tokens）；Claude Sonnet 4.6 做翻译输出（多语种质量高、性价比优于 Opus）。两个模型各司其职，千字总成本约 $0.07
- **架构**：Fork AgentCut，复用 Pipeline/SSE/Job 管理。只替换 Agent 业务逻辑
- **文化知识库**：JSON 文件，不用向量数据库。每条含 concept/context/good_translations/bad_translations/principle。MVP 够用，赛后可升级
- **知识库匹配策略**：将 100 条知识库 key 列表注入 Agent 1 的 prompt（约 200-400 token），让 LLM 直接从列表中识别和选择匹配项，绕过字符串匹配的模糊问题。未命中知识库的概念由 Agent 2 用 LLM fallback 生成候选翻译并标记"待人工审核"
- **质量保证**：Pipeline 第 4 步（审校 Agent）用不同 prompt 角色 + 结构化检查清单（忠实度、流畅度、文化适配度、字幕长度）做 self-critique
- **SRT 处理**：纯代码解析，不依赖 LLM。保持原始时间轴不变

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification.*

```
用户输入（中文剧本文本 或 SRT 字幕文件 + 目标语种）
    |
    v
[Agent 1: 内容分析] ——— DeepSeek
    提取：角色表、文化元素清单、高风险台词、情感基调
    |
    v
[Agent 2: 知识库匹配] ——— 本地查询 + LLM fallback
    每个文化元素 → 查 JSON 知识库 → 获取映射/正例/反例
    未命中 → DeepSeek 实时推理 + 标记为"待人工审核"
    |
    v
[Agent 3: 文化适配翻译] ——— Claude/GPT-4
    输入：原文 + 文化映射表 + 角色关系 + 情感基调
    输出：逐句翻译（SRT 保持时间轴）+ 每句置信度
    |
    v
[Agent 4: 审校 Agent] ——— DeepSeek（不同 prompt 角色）
    角色："在美国生活 20 年的华裔影视翻译专家"
    检查：文化冲突？翻译腔？情感偏差？遗漏？
    输出：问题列表 + 修改建议
    |
    v
[Agent 5: 终稿 + 推广] ——— Claude/GPT-4
    5a: 根据审校意见修正翻译，输出终稿
    5b: 基于剧情分析生成：剧情简介 + 3条社媒帖子 + hashtag
    |
    v
[输出]
    ├── 翻译结果（纯文本 或 SRT 文件）
    ├── 翻译决策报告（每个文化梗的适配解释）
    ├── 质量报告（整体置信度 + 建议人工复核的句子）
    └── 推广素材包（简介 + 帖子 + hashtag）
```

**质量保证链路：**
- Agent 1 防止漏识别文化元素 → 避免"没翻到"
- Agent 2 用知识库锚定翻译方向 → 避免"翻错了"
- Agent 3 带完整上下文翻译 → 避免"翻译腔"
- Agent 4 专门挑毛病 → 避免"自我感觉良好"
- Agent 5 修正 + 终稿 → 输出稳定

## Implementation Units

### Phase 1: 核心框架 + 知识库（Week 1: 4/14-4/20）

- [ ] **Unit 1: Fork AgentCut 并重构为翻译 Pipeline**

**Goal:** 将 AgentCut 改造为 5 Agent 翻译 Pipeline 骨架

**Requirements:** R1, R7

**Dependencies:** None

**Files:**
- Fork: `agentcut` → `culturebridge/`
- Modify: `backend/main.py` — API 接受剧本文本/SRT + 目标语种
- Modify: `backend/pipeline.py` — 5 Agent 串行 Pipeline
- Create: `backend/agents/analyzer.py` — Agent 1 骨架
- Create: `backend/agents/kb_matcher.py` — Agent 2 骨架
- Create: `backend/agents/translator.py` — Agent 3 骨架
- Create: `backend/agents/reviewer.py` — Agent 4 骨架
- Create: `backend/agents/finalizer.py` — Agent 5 骨架
- Create: `backend/parsers/srt.py` — SRT 解析和输出
- Test: `tests/test_pipeline.py`

**Approach:**
- 保留 AgentCut 的 Job 管理、SSE、错误处理、清理机制
- Pipeline 改为纯串行（每步依赖上一步输出），不并行
- SRT 解析器：提取时间轴+台词，翻译后重新组装 SRT

**Patterns to follow:**
- `agentcut/backend/pipeline.py` — Pipeline 编排
- `agentcut/backend/agents/director.py` — Agent 基类

**Test scenarios:**
- Happy path: 输入 5 句剧本文本 + "en" → 5 Agent 依次执行 → 返回翻译 JSON
- Happy path: 输入 SRT 文件 → 正确解析 → 翻译 → 输出 SRT（时间轴不变）
- Edge case: 空输入 → 明确报错
- Error path: Agent 3 LLM 超时 → 自动重试 1 次 → 仍失败则标记该句为"翻译失败"继续后续
- Integration: SSE 推送 5 Agent 状态（pending → active → completed）

**Verification:**
- Pipeline 端到端跑通（骨架 Agent 输出占位内容即可）
- SRT 输入/输出时间轴一致

---

- [ ] **Unit 2: 文化知识库**

**Goal:** 构建 100 条高质量文化概念映射，覆盖短剧高频场景

**Requirements:** R2

**Dependencies:** None（与 Unit 1 并行）

**Files:**
- Create: `backend/knowledge/culture_kb.py` — 查询接口
- Create: `backend/knowledge/mappings/palace.json` — 宫廷剧（40 条）
- Create: `backend/knowledge/mappings/wuxia.json` — 武侠剧（20 条）
- Create: `backend/knowledge/mappings/xianxia.json` — 修仙/玄幻（20 条）
- Create: `backend/knowledge/mappings/modern.json` — 都市剧（20 条）
- Test: `tests/test_culture_kb.py`

**Approach:**
每条映射结构：
```
concept: 原文概念
context: 使用语境
genre: palace/wuxia/xianxia/modern
mappings:
  en:
    good: [优秀翻译示例]
    bad: [错误翻译示例]
    principle: 翻译原则
    avoid: [避雷词]
  ja: ...
  ko: ...
```

重点条目（宫廷剧 40 条示例）：
- 称谓类：臣妾、本宫、皇上、爱妃、奴才、微臣、哀家、太后（15 条）
- 场景类：选秀、册封、打入冷宫、赐死、翻牌子（10 条）
- 表达类：冤家路窄、太岁头上动土、知人知面不知心（15 条）

**每条都需要人工审核**，不能 LLM 自动生成。这是产品壁垒。

**Test scenarios:**
- Happy path: query("臣妾", "en") → 返回完整映射含 good/bad/principle
- Happy path: query("渡劫", "ja") → 返回日文映射
- Edge case: query("不存在的概念", "en") → 返回 None + fallback 标记
- Edge case: query("臣妾", "fr") → 返回英文 fallback

**Verification:**
- 100 条映射完整，每条含 3 语种
- 查询 < 50ms
- 每条至少 2 个 good_translation 示例

---

### Phase 2: 5 个 Agent 实现（Week 2-3: 4/21-5/04）

- [ ] **Unit 3: Agent 1 — 内容分析**

**Goal:** 分析输入内容，提取角色、文化元素、高风险台词、情感基调

**Requirements:** R1

**Dependencies:** Unit 1

**Files:**
- Modify: `backend/agents/analyzer.py`
- Test: `tests/test_analyzer.py`

**Approach:**
- LLM: DeepSeek（中文理解强）
- 两步 Prompt：1) 整体分析（剧情、角色关系） 2) 逐句扫描文化元素
- 输出 JSON：plot_summary, characters[], cultural_elements[], high_risk_lines[], tone

**Test scenarios:**
- Happy path: 古装剧 10 句台词 → 识别出"臣妾""本宫"等 + 角色关系
- Happy path: 都市剧 → 标注"低文化风险"
- Edge case: 纯旁白无对话 → 正常分析，characters 为空

**Verification:**
- 文化元素召回率 > 90%（用 Demo 场景人工验证）

---

- [ ] **Unit 4: Agent 2 — 知识库匹配**

**Goal:** 将识别出的文化元素逐个匹配知识库，未命中的用 LLM fallback

**Requirements:** R1, R2

**Dependencies:** Unit 1, Unit 2, Unit 3

**Files:**
- Modify: `backend/agents/kb_matcher.py`
- Test: `tests/test_kb_matcher.py`

**Approach:**
- 输入：Agent 1 的 cultural_elements 列表（Agent 1 已在 prompt 中内置 100 条知识库 key，直接输出匹配的 key）
- 逐个查知识库：Agent 1 已匹配的 key → 返回完整映射；Agent 1 标记为"未在知识库中"的 → 调 DeepSeek 实时生成 2-3 个候选翻译并说明选择理由 + 标记"LLM 生成，建议人工审核"
- 输出：enriched_elements[]（每个元素带翻译指南 + 来源标记：knowledge_base / llm_generated）

**Test scenarios:**
- Happy path: ["臣妾", "本宫", "冤家"] → 3 个全部命中知识库
- Happy path: ["臣妾", "未知概念"] → 1 命中 + 1 LLM fallback
- Edge case: 空列表 → 返回空，不报错

**Verification:**
- 知识库命中的元素有完整映射
- LLM fallback 的元素有"待审核"标记

---

- [ ] **Unit 5: Agent 3 — 文化适配翻译（核心）**

**Goal:** 带完整文化上下文的逐句翻译，质量 85 分

**Requirements:** R1, R3, R4, R5

**Dependencies:** Unit 1, Unit 4

**Files:**
- Modify: `backend/agents/translator.py`
- Test: `tests/test_translator.py`

**Approach:**
- LLM: Claude/GPT-4（多语种输出质量更高）
- Prompt 注入：角色关系表 + 文化映射表（含正例/反例）+ 情感基调 + 翻译原则
- 逐句翻译，每句输出：original, translation, confidence(high/medium/low), cultural_notes
- SRT 模式：保持时间轴，只替换文字
- temperature: 0.3（稳定输出）
- 长文本分段处理（每段 30 句），段间保持上下文连贯

**Test scenarios:**
- Happy path: "臣妾做不到啊" + 知识库映射 → 翻译不含"maid/servant"，含"Your Majesty"或类似敬语
- Happy path: SRT 输入 → 输出 SRT 时间轴完全一致
- Happy path: 日语输出 → 使用正确的敬语体系
- Edge case: 无文化元素的普通对话 → 正常翻译，confidence: high
- Error path: LLM 输出格式异常 → 解析失败则重试 1 次

**Verification:**
- Demo 场景翻译无"maid""servant"等已知错误翻译
- 每句都有 confidence 标记
- SRT 时间轴保持

---

- [ ] **Unit 6: Agent 4 — 审校 Agent（质量跳板）**

**Goal:** 用不同 prompt 角色审查翻译，基于结构化检查清单找出文化冲突和翻译腔

**Requirements:** R1, R5

**Dependencies:** Unit 1, Unit 5

**Files:**
- Modify: `backend/agents/reviewer.py`
- Test: `tests/test_reviewer.py`

**Approach:**
- LLM: DeepSeek（成本低，审校不需要多语种输出）
- Prompt 角色："你是一位在美国生活 20 年、精通中英双语的影视字幕翻译专家。你的任务是审查以下翻译，找出问题。"
- 审查维度：1) 文化冲突 2) 翻译腔/不自然 3) 情感偏差 4) 角色语气不一致 5) 遗漏
- 输出：issues[]（每个 issue 含 line_number, problem, suggestion, severity）
- 只挑问题，不重写翻译

**Test scenarios:**
- Happy path: 故意输入一句含"maid"的错误翻译 → 审校 Agent 标记为文化冲突
- Happy path: 输入翻译腔明显的句子 → 标记为"不自然"
- Edge case: 翻译质量很高 → 返回空 issues 列表或极少问题

**Verification:**
- 能检出已知的文化冲突错误
- 不过度挑刺（误报率 < 20%）

---

- [ ] **Unit 7: Agent 5 — 终稿 + 推广素材**

**Goal:** 根据审校意见修正翻译出终稿 + 生成推广素材

**Requirements:** R1, R5, R6

**Dependencies:** Unit 1, Unit 5, Unit 6

**Files:**
- Modify: `backend/agents/finalizer.py`
- Test: `tests/test_finalizer.py`

**Approach:**
- 5a 终稿：将 Agent 4 的 issues 逐条应用到 Agent 3 的翻译上，输出最终版
- 5b 推广：基于 Agent 1 的剧情分析 + Agent 2 的文化映射，生成：
  - 多语种剧情简介（100-200 词）
  - 3 条社媒帖子（TikTok/Instagram/X 各 1 条，含 hashtag）
  - 目标受众建议
- 5a 和 5b 可以并行（两次独立 LLM 调用）

**Test scenarios:**
- Happy path: Agent 4 报告 2 个问题 → 终稿修正了这 2 处
- Happy path: 推广素材包含剧情简介 + 3 条帖子 + hashtag
- Edge case: Agent 4 无问题 → 终稿 = Agent 3 原文
- Integration: 终稿 SRT + 推广素材同时输出

**Verification:**
- 终稿反映审校修正
- 推广素材语言与目标语种一致

---

### Phase 3: Dashboard + Demo（Week 4: 5/05-5/11）

- [ ] **Unit 8: CultureBridge Dashboard**

**Goal:** Web 界面，展示 5 Agent 工作流 + 翻译结果 + 对比

**Requirements:** R7

**Dependencies:** Unit 1

**Files:**
- Modify: `frontend/index.html`
- Modify: `frontend/styles.css`
- Test expectation: none — 视觉验证

**Approach:**
- 输入区：文本粘贴框 / SRT 上传 + 语种选择（英/日/韩）+ 剧种选择（宫廷/武侠/修仙/都市）
- 进度区：5 Agent 实时状态卡片（复用 AgentCut SSE 模式）
- 结果区 Tab 1：翻译结果（原文 | CultureBridge | Google Translate 三列对比）
- 结果区 Tab 2：翻译决策报告（每个文化梗的适配解释）
- 结果区 Tab 3：推广素材包
- 结果区 Tab 4：质量报告（置信度分布 + 建议人工复核的句子）
- 导出：下载 SRT + 决策报告 Markdown + 推广素材
- **杀手功能：三列对比展示。** 左边原文，中间 Google Translate，右边 CultureBridge。文化梗行高亮标红。这是 Demo 最有冲击力的画面。

**Verification:**
- 对比展示清晰，文化梗高亮
- SRT 下载格式正确

---

- [ ] **Unit 9: Demo 场景 + 视频录制**

**Goal:** 2 个路演级 Demo 场景 + 对比展示 + 录屏

**Requirements:** R9

**Dependencies:** 全部完成

**Files:**
- Create: `demo/palace_drama.txt` — 古装宫廷剧剧本（20-30 句）
- Create: `demo/palace_drama.srt` — 对应 SRT 字幕
- Create: `demo/urban_romance.txt` — 都市情感剧剧本（20-30 句）
- Create: `demo/README.md`

**Approach:**
- 场景 1（古装宫廷剧→英语）：密集文化梗（臣妾/本宫/冤家/太岁/冷宫），展示文化适配 vs 直译的巨大差距
- 场景 2（都市情感剧→日语）：展示不同剧种和语种的适配能力
- 每个场景：
  1. 先用 Google Translate 翻译同一段（录屏保留）
  2. 再用 CultureBridge 翻译（录屏全流程）
  3. 三列对比展示，文化梗高亮
- **翻译结果必须人工校验和微调**，确保 Demo 质量 100 分
- 录制 2-3 分钟视频用于线上初评

**Test scenarios:**
- Happy path: 场景 1 → 5 分钟内完成 → "臣妾"不出现 maid/servant → 对比效果震撼
- Happy path: 场景 2 → 日语输出使用正确敬语体系

**Verification:**
- 两个场景 < 5 分钟完成
- 翻译零文化冲突错误（人工验证）
- 对比 Google Translate 有明显质量差距
- Demo 视频完成

## Success Metrics

| 指标 | 目标 | 如何验证 |
|------|------|--------|
| 翻译质量 | 90+ 分 | Demo 场景人工评分（找 2-3 个双语者打分） |
| 文化梗处理 | 零严重错误 | "臣妾"永远不出现 maid/servant 等已知错误 |
| 任务耗时 | < 5 分钟/千字 | Demo 录屏计时 |
| 任务成本 | < $0.30/千字 | API 调用日志统计 |
| 对比优势 | vs Google Translate 明显更好 | 三列对比截图 |
| 参赛结果 | 进入复赛 | — |

## Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| GhostCut 已占 70% 头部客户 | High | High | 不抢批量翻译市场，聚焦"可解释文化适配"差异化；长期走 API 上游路线 |
| 翻译质量不到 90 分 | Medium | High | 审校 Agent 是关键；Demo 场景人工微调兜底 |
| 知识库 100 条不够覆盖 | Medium | Medium | 聚焦宫廷剧（Demo 场景用的类型），其他类型用 LLM fallback |
| LLM 输出不稳定 | Medium | Medium | temperature 0.3 + 知识库 few-shot 锚定 + 重试机制 |
| 评委认为"套壳 LLM" | Medium | High | Demo 重点展示三列对比 + 翻译决策报告（展示知识库的精准映射） |
| 翻译剧 ARPU 低，行业趋势走向本土制作 | Medium | Medium | Phase 3 升级为本土化剧本改编方案，跟随行业趋势 |
| 没有真实用户 | High | Medium | 赛前社媒发帖收集反馈 + 找 1 个短剧团队试用 |
| 4 周工期紧张 | High | High | 严格复用 AgentCut；知识库从宫廷剧 40 条开始，其他类型后补 |

## Phased Delivery

### Phase 1（4/14-4/20）
- Unit 1: Fork AgentCut + Pipeline 骨架
- Unit 2: 文化知识库（优先宫廷剧 40 条）
- Milestone: Pipeline 跑通 + 知识库可查询

### Phase 2（4/21-5/04）
- Unit 3-7: 5 Agent 实现
- 优先级：Agent 3 翻译 > Agent 4 审校 > Agent 1 分析 > Agent 2 匹配 > Agent 5 终稿+推广
- 同时补充知识库到 100 条
- Milestone: 端到端翻译可运行

### Phase 3（5/05-5/11）
- Unit 8: Dashboard（重点做三列对比展示）
- Unit 9: Demo 打磨 + 视频录制
- Milestone: 路演级 Demo

### Buffer（5/12-5/25）
- 报名注册 + 材料提交
- BP 准备（商业计划书）
- 社媒发帖收集用户反馈
- 联系 1 个短剧团队试用

## Sustainable Business Model（赛后路径）

### 定价策略

| 方式 | 市场参考价 | CultureBridge 定价 |
|------|----------|-------------------|
| 纯 AI 翻译（GhostCut 等） | 0.1-0.7 元/分钟 | — |
| AI + 人工校对 | 50 元/分钟 | — |
| 人工翻译 | 200-300 元/分钟 | — |
| **CultureBridge（AI 文化适配翻译）** | — | **5-20 元/分钟**（介于纯 AI 和 AI+人工之间） |

### 三阶段商业路径

- **Phase 1（参赛+验证）**：精品剧文化适配翻译 SaaS，5-20 元/分钟
- **Phase 2（API 上游）**：把文化适配能力以 API 输出给 GhostCut/Vozo 等平台，按调用量计费
- **Phase 3（本土化改编）**：从翻译升级为"中国剧本→海外本土化改编方案"，ARPU 提升 6 倍+

### 核心壁垒

- **文化知识库**：越积累越深（100→1000→10000 条），含正例/反例/适配原则
- **翻译决策报告**：可解释的翻译过程，竞品没有
- **数据飞轮**：用户反馈持续优化知识库映射质量

### 目标客户

- 短剧出海平台内容审核团队（需要翻译决策报告做质量把控）
- 精品古装/仙侠剧翻译需求方（文化密度高，通用 AI 翻译质量差）
- 人工翻译公司（如 TXV/Etrans/火星翻译）的效率工具

## Sources & References

### 大赛

- 大赛手册：`2026文创上海大赛手册.pdf`
- 大赛官网：https://www.sccipa.com.cn
- 临港科创城：https://kjc.shlingang.com

### 市场数据

- 光大证券研报：海外短剧市场收入 23.8 亿美元、下载量 12.1 亿次
- [21 经济网：短剧出海下半场](https://www.21jingji.com/article/20260120/herald/0fbea0a0c9367654c54b632c5d6bfb75.html)——DramaBox 翻译剧占比 90%+，容量短剧 AI 翻译平台
- [澎湃新闻：海外 AI 短剧市场规模预计 6.5 亿美金](https://m.thepaper.cn/newsDetail_forward_32894342)
- [36氪：进击的 DramaBox](https://36kr.com/p/2764514332015365)
- [36氪：2025Q1 海外微短剧市场报告](https://36kr.com/p/3249594364782085)

### 痛点验证

- [Etrans 短剧翻译案例](https://www.etctrans.com/news/gongsixinwen/2026/0108/2413.html)——腾讯微视文化适配前后完播率 20%→83%
- [Nature 2025：Viki 社区字幕组工作流](https://www.nature.com/articles/s41599-025-05856-y)——70% 编辑精力用于文化隐喻修复
- [Medium：Lost in Translation or Localization](https://medium.com/@dominique.bizbuzz/has-exporting-short-dramas-been-lost-in-translation-or-localization-35e959760055)
- 知乎"跨境小k"：短剧出海翻译避坑指南
- 小红书搜索"短剧出海翻译痛点"：多篇从业者帖子
- Reddit r/CDrama, r/CShortDramas：海外观众翻译质量吐槽

### 竞品

- [GhostCut 短剧出海方案](https://jollytoday.com/short-drama-translation/)——70% 头部客户，日处理 10 万集，$0.1/分钟
- [HeyGen Precision Mode](https://www.heygen.com/translate/language-localization)
- [Rask.ai](https://www.rask.ai/)
- [Vozo AI](https://www.vozo.ai/zh/short-drama-translation)——700 万+用户
- [火山引擎赋能短剧出海](https://zhuanlan.zhihu.com/p/1900848657093333565)
- 录咖 AI（RecCloud）、ViiTor AI、趣丸千音

### 技术

- AgentCut：https://github.com/calderbuild/agentcut
- [短剧本地化成功要素](https://wordsprime.com/how-chinese-micro-dramas-localization-drives-global-success-and-viral-growth/)
- [短剧出海合规挑战](https://artlangs.com/news-detail/Regulatory-Challenges-in-the-overseas-expansion-of-Short-Dramas--How-Should-Subtitles-and-Dubbing-Navigate-Global-Content-Censorship-)
