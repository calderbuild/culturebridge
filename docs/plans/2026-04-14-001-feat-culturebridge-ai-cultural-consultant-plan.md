---
title: "feat: CultureBridge — 中国文化内容出海 AI 文化顾问引擎"
type: feat
status: active
date: 2026-04-14
supersedes: 2026-04-13-001-feat-ai-gtm-agent-cultural-export-plan.md
competition: 2026 第四届"文创上海"创新创业大赛
track: 数字文化出海+
track_partner: 临港科创城（滴水湖 AI 创新港科创社区）
deadline_register: 2026-05-31
deadline_demo: 2026-05-25
deadline_final: 2026-08
---

# CultureBridge — 中国文化内容出海 AI 文化顾问引擎

## Overview

中国数字文化出海有三道障碍：语言障碍、声音障碍、文化障碍。翻译工具（GhostCut）解决了第一道，AI 配音（DubbingX）解决了第二道。**文化障碍——至今没有工具化的解决方案。**

CultureBridge 是中国文化内容出海的 AI 文化顾问。输入任何中国文化文本内容（短剧剧本、网文章节、游戏对白、动漫台词、有声书脚本、文化短视频文案等），输出带完整文化依据的适配翻译、文化风险报告和改编建议。

核心壁垒：**可审计的文化适配过程**——通用 LLM 能翻译大部分术语，但输出是黑盒且长文本中术语不一致。CultureBridge 用结构化知识库强制术语一致性，并生成翻译决策报告让客户知道"为什么这样翻"。竞品的翻译不可审计，我们的可以。

> 待验证：Demo 前需跑对照实验——同样输入，纯 Claude（无知识库）vs 知识库增强版，盲测评分，量化知识库的增量价值。

一句话：**让每个出海团队都用得起"黑神话悟空"级别的文化把关能力。**

## Problem Frame

### 一句话痛点

中国文化内容出海，翻译了文字却丢了灵魂。修仙剧西方观众文化折损率 58%，腾讯微视短剧文化适配前完播率仅 20%。**问题不是翻译不准，是文化不通。**

### 数据支撑

**市场规模（文化出海"新三样"）：**
- 短剧出海：2025 海外收入 23.8 亿美元，翻译剧占 80-90%（光大证券/DramaBox）
- 网文出海：2025 市场规模 38 亿美元，CAGR 10.9%（行业研报）
- 游戏出海：2025 中国自研游戏海外收入 204 亿美元
- 三大产业总收入合计超 265 亿美元（TAM）。其中本地化/翻译服务子市场约 5-13 亿美元（SAM，按翻译占总收入 2-5% 估算）。CultureBridge 初期可触达的中小出海团队市场（SOM）待通过客户访谈验证

**文化适配是核心痛点：**
- 腾讯微视案例：文化适配前后完播率差异超过 60 个百分点（Etrans 自报数据，2026，翻译服务商案例研究，未经第三方验证）
- Viki 社区字幕组 70% 编辑精力用于修复文化隐喻和历史术语（Nature 2025）
- 修仙剧每集平均 4.2 个道教/佛教术语，西方观众文化折损率 58%（学术论文）
- 黑神话悟空做 100 万+词本地化，**专门配了中国文化顾问 Xuan Pan**（Altagram）
- Reddit r/noveltranslations："Is it me or is 99% of Webnovel AI slop now?"（100+ 评论）
- 小红书："中式翻译劝退老外？血亏百万教训"
- 起点国际 2025 年新增 10,000 部 AI 翻译作品，但质量饱受诟病

**现状：文化顾问 = 稀缺 + 昂贵**
- 人工文化顾问 500-1000 元/小时（火星翻译），中小团队请不起
- 黑神话悟空级别的文化把关只有头部项目才能负担
- 通用 LLM 训练数据以西方文化为主，处理东方文化概念时系统性失准（ScienceDirect 2026）

### 为什么现有工具解决不了

| 工具 | 做什么 | 不做什么 |
|------|--------|---------|
| GhostCut | 视频翻译全链路（字幕擦除+翻译+配音） | 文化适配是黑盒，无决策报告 |
| DubbingX | AI 配音（情感表现力） | 不管"说什么"，只管"怎么说" |
| 阅文自研 AI | 网文 AI 翻译 | 封闭体系，不对外 |
| 推文科技 | 网文 AI 翻译分发 | 偏流水线，文化深度不够 |
| Altagram | 高端游戏本地化服务 | 人工为主，价格高，不可规模化 |
| Gridly/Lokalise | 通用本地化 TMS | 不理解中国文化语境 |
| 人工文化顾问 | 文化把关 | 500-1000 元/小时，不可规模化 |
| **CultureBridge** | **AI 文化顾问：文化风险扫描 + 适配翻译 + 改编建议 + 决策报告** | 配音/唇形同步/视频处理（不做） |

### 赛题对应

| 赛道关键词 | CultureBridge 对应 |
|---------|-------------------|
| 提升中华文化影响力 | 解决文化折扣，让中国 IP 被海外正确理解 |
| 数字文化贸易与新业态 | AI 文化顾问是新业态——人工顾问 → AI 产品化 |
| 构建国际化服务生态 | 出海产业链底层基础设施 |
| 全球化表达与分众化传播 | 同一内容针对不同市场生成不同适配方案 |
| 网文、网剧、网游出海 | 一个知识库同时服务三个领域 |
| 数字技术迭代创新 | 多 Agent Pipeline + 文化知识库 |
| 数字内容创制与传播 | 输出改编建议 + 推广素材 |
| 运用 AI 新技术 | DeepSeek + Claude 双模型 5 Agent Pipeline |
| 优质文化内容创造性转化 | 文化适配翻译 = 创造性转化（非直译） |
| 打造全球吸引力的中国文化 IP | 帮 IP 跨越文化障碍触达全球受众 |

核心命中 3 个赛道关键词：**"运用 AI 对优质文化内容进行创造性转化"**、**"网文/网剧/网游出海"**、**"全球化表达与分众化传播"**。其余关键词自然覆盖。

## Requirements Trace

### 功能需求（P0 — Demo 必须）

- R1. 5 Agent Pipeline（文化扫描→知识库匹配→适配翻译→审校→终稿+出海方案）
- R2. 文化知识库：Demo 阶段 35 条精选高频映射（宫廷 20 + 修仙 15），覆盖两个 Demo 场景 95%+ 文化概念。Buffer 期扩展至 60+ 条
- R3. 跨内容形态：同一引擎处理短剧剧本和网文章节（Demo 验证两种形态）。游戏对白作为展示加分项
- R4. 语种：英语（Demo 验证路径）。日/韩架构预留（知识库 schema 支持多语种字段，但 Demo 阶段只填充英语映射）
- R5. 输入格式：纯文本粘贴 + SRT 字幕文件上传
- R6. 输出四件套（P0）：适配翻译 + 翻译决策报告 + 文化风险报告 + 文化注释。改编建议和推广素材为 P2 加分项

### 非功能需求

- R7. 5 Agent Pipeline 实时进度面板（SSE）
- R8. 单次任务成本 < $0.30/千字（实际估算约 $0.12-0.18/千字）

### 里程碑约束

- R9. 两个核心 Demo 场景（短剧+网文）在 2026-05-25 前完成。游戏对白场景为 Buffer 期加分项

## Scope Boundaries

### In Scope

- 5 Agent 文化顾问 Pipeline（核心）
- 文化知识库（100+ 条，人工打磨，跨内容形态通用）
- 三个 Demo 场景（短剧 + 网文 + 游戏对白）
- 翻译决策报告 + 文化风险报告（核心差异化）
- 文化注释自动生成（Viki 模式自动化）
- 推广素材生成
- SRT 解析和输出
- Web Dashboard（复用 AgentCut 前端）
- 三列对比展示（原文 vs Google Translate vs CultureBridge）

### Out of Scope

- 配音 / 唇形同步 / 视频处理（DubbingX 等已做）
- 字幕硬烧入视频
- 用户系统 / 计费
- 内容合规审核（数美等已做）
- 漫画 OCR / 图文翻译（技术链太长）

## Context & Research

### 竞品格局

详见 `docs/research/2026-04-14-idea-research-report.md`

核心结论：现有竞品在文化适配维度存在明确缺口——GhostCut/推文科技的翻译过程是黑盒，用户无法审核文化决策；阅文 AI 翻译封闭不对外；Altagram 等人工服务不可规模化。**没有竞品提供"可审计的文化适配过程"（翻译决策报告）。**

> 竞品验证方法：除线上调研外，需在 Demo 前直接访谈 2-3 个短剧/网文出海团队，确认他们目前如何处理文化适配、使用什么工具、痛点在哪里。

### 与 DubbingX（三届一等奖）的定位区分

```
DubbingX：解决"怎么说"（AI 配音，情感表现力）
CultureBridge：解决"说什么"（AI 文化适配，该翻什么、怎么改编）
→ CultureBridge 是 DubbingX 的上游，互补不竞争
```

### PMF 验证

详见 `docs/research/2026-04-14-idea-research-report.md` 第四章

| 信号 | 结论 |
|------|------|
| 痛点真实 | 文化折扣是所有信源 #1 痛点（58% 折损率；完播率 20%→83%） |
| 市场够大 | 三大领域合计 265 亿美元 |
| 竞品空白 | Product Hunt / IndieHackers 零相关产品 |
| 付费意愿 | 人工文化顾问 500-1000 元/小时，证明用户愿意为文化把关付费 |
| 海外用户需求 | Reddit 大量吐槽翻译质量；Viki 文化注释最受欢迎 |

### 往届获奖模式匹配

详见 `docs/research/2026-04-14-idea-research-report.md` 第二章

- 黑镜科技（首届一等奖）：AI 数字人 → **技术壁垒 + 商业落地**
- 回音星旅（二届年度创新）：3D 扫描国宝 → **技术赋能文化**
- DubbingX（三届一等奖）：AI 配音 → **AI + 内容出海工具**
- CultureBridge 对标：**AI + 文化适配 → 内容出海的文化层**

### 可复用代码

| 项目 | 复用部分 | 实际改动量 |
|------|--------|----------|
| `agentcut` | SSE streaming + Job 管理模式 | 直接复用 |
| `agentcut` | main.py 路由结构、错误处理 | 轻度改动 |
| `agentcut` | config.py（API 客户端） | 完全重写（从 Minimax 换为 DeepSeek + Anthropic SDK） |
| `agentcut` | pipeline.py（Agent 编排） | 中度重写（6 并行 Agent → 5 串行 Agent） |
| `agentcut` | 前端 HTML/Tailwind | 结构模式复用，UI 组件 60-70% 重写（视频制作 UI → 文本对比+报告展示 UI） |
| `agentcut` | 所有 Agent 文件 | 完全替换 |

## Key Technical Decisions

- **LLM 策略**：DeepSeek V3（或最新可用版本）做分析和审校（中文理解强、API 单价约 $0.27/M input tokens）；Claude Sonnet 4.6 做翻译输出（多语种质量高、$3/$15 per M tokens）。千字总成本约 $0.12-0.18（含 context 累积和重试 buffer，仍远低于 R8 的 $0.30 上限）
- **架构**：Fork AgentCut，复用 Pipeline/SSE/Job 管理，替换 Agent 业务逻辑
- **文化知识库**：JSON 文件。每条含 concept/context/content_types/good_translations/bad_translations/principle/cultural_notes。跨内容形态通用（同一条"渡劫"映射在短剧/网文/游戏中都适用）
- **知识库匹配**：100+ 条 key 列表注入 Agent 1 prompt，LLM 直接从列表中选择匹配项
- **质量保证**：Agent 4 审校用不同 prompt 角色 + 结构化检查清单（忠实度、流畅度、文化适配度、角色语气一致性）
- **SRT 处理**：纯代码解析，保持时间轴

## High-Level Technical Design

```
输入：中国文化内容（短剧剧本 / 网文章节 / 游戏对白）+ 目标市场 + 内容类型
    |
    v
[Agent 1: 文化元素扫描] ——— DeepSeek V4
    提取：角色表、文化概念清单、高风险内容、情感基调、内容类型特征
    内置 100+ 条知识库 key 列表，直接输出匹配的 key
    |
    v
[Agent 2: 知识库匹配 + 文化风险评估] ——— 本地 JSON + DeepSeek fallback
    命中 → 返回完整映射（正例/反例/原则/文化注释）
    未命中 → LLM 生成候选 + 标记"待审核"
    新增：生成文化风险报告（目标市场的文化冲突点）
    |
    v
[Agent 3: 文化适配翻译] ——— Claude Sonnet 4.6
    输入：原文 + 文化映射表 + 角色关系 + 情感基调
    输出：逐句适配翻译 + 每句置信度 + 文化注释（Viki 模式）
    |
    v
[Agent 4: 审校] ——— DeepSeek V4（不同 prompt 角色）
    结构化检查：文化冲突？翻译腔？情感偏差？角色语气不一致？术语一致性？
    输出：问题列表 + 修改建议
    |
    v
[Agent 5: 终稿 + 出海方案] ——— Claude Sonnet 4.6
    5a: 修正翻译，输出终稿
    5b: 改编建议书（角色名本地化方案、情节调整建议）
    5c: 推广素材（剧情简介 + 社媒帖子 + hashtag）
    |
    v
[输出六件套]
    ├── 适配翻译结果（纯文本 / SRT）
    ├── 翻译决策报告（每个文化梗的知识库依据）
    ├── 文化风险报告（目标市场文化冲突点）
    ├── 改编建议书（角色/情节/视觉的本地化建议）
    ├── 文化注释（自动生成的 Viki 式注释）
    └── 推广素材包（简介 + 帖子 + hashtag）
```

**跨内容形态通用性**：同一条知识库映射（如"渡劫"）在三种场景中被不同 Agent 引用——
- 短剧：字幕翻译 + 文化注释
- 网文：术语一致性保持 + 章节间连贯
- 游戏：角色对白语气适配 + 文化风险扫描

## Implementation Units

### Phase 1: 核心框架 + 知识库（Week 1: 4/14-4/20）

- [ ] **Unit 1: Fork AgentCut + 多内容形态 Pipeline**

**Goal:** 5 Agent Pipeline 骨架，支持短剧/网文/游戏三种输入

**Requirements:** R1, R3, R7

**Files:**
- Fork: `agentcut` → `culturebridge/`
- Modify: `backend/main.py` — API 接受文本/SRT + 目标语种 + 内容类型（drama/novel/game）
- Modify: `backend/pipeline.py` — 5 Agent 串行 Pipeline
- Create: `backend/agents/cultural_scanner.py` — Agent 1
- Create: `backend/agents/kb_matcher.py` — Agent 2
- Create: `backend/agents/translator.py` — Agent 3
- Create: `backend/agents/reviewer.py` — Agent 4
- Create: `backend/agents/finalizer.py` — Agent 5
- Create: `backend/parsers/srt.py` — SRT 解析（含字幕长度约束检查：翻译后每段不超过 18 CPS）
- Test: `tests/test_pipeline.py`

**Verification:** Pipeline 骨架端到端跑通

---

- [ ] **Unit 2: 文化知识库（跨内容形态）**

**Goal:** 35 条精选高频文化概念映射（Demo 所需最小集），覆盖两个 Demo 场景 95%+ 文化概念

**Requirements:** R2

**Files:**
- Create: `backend/knowledge/culture_kb.py` — 查询接口
- Create: `backend/knowledge/mappings/palace.json` — 宫廷（20 条，覆盖 Demo 场景 1）
- Create: `backend/knowledge/mappings/xianxia.json` — 修仙/玄幻（15 条，覆盖 Demo 场景 2）
- Test: `tests/test_culture_kb.py`

**Phase 2 扩展**（Week 2-3 与 Agent 实现并行）：
- 宫廷扩展至 40 条、新增 `wuxia.json`（20 条）、`modern.json`（20 条）
- Buffer 期目标：总计 60+ 条

**映射结构（升级版）：**
```json
{
  "concept": "渡劫",
  "context": "修仙体系中修炼者突破大境界时必须经历的天雷考验",
  "content_types": ["drama", "novel", "game"],
  "genre": "xianxia",
  "mappings": {
    "en": {
      "good": ["Heavenly Tribulation", "Tribulation Lightning"],
      "bad": ["cross the robbery", "survive disaster"],
      "principle": "保留修仙体系的庄严感和危险感，不要用日常用语替代",
      "avoid": ["robbery", "disaster", "calamity"],
      "cultural_note": "In Chinese cultivation novels, 'Tribulation' refers to divine lightning that tests a cultivator's worthiness to advance. It's a life-or-death trial, not a natural disaster."
    }
  }
}
```

**每条人工审核**，不可 LLM 自动生成。知识库是核心壁垒。

**Verification:** 35 条完整，每条含英语映射 + 文化注释。Demo 场景输入中的文化概念命中率 > 95%

---

### Phase 2: 5 个 Agent 实现（Week 2-3: 4/21-5/04）

- [ ] **Unit 3: Agent 1 — 文化元素扫描**

**Goal:** 分析输入内容，提取文化元素，识别高风险内容

**Approach:**
- LLM: DeepSeek V4
- Prompt 内置 100+ 条知识库 key，直接输出匹配项
- 根据 content_type 调整扫描策略（短剧关注对白/网文关注叙述/游戏关注 UI 文本）
- 输出：cultural_elements[], high_risk_lines[], characters[], tone

---

- [ ] **Unit 4: Agent 2 — 知识库匹配 + 文化风险评估**

**Goal:** 匹配知识库 + 生成文化风险报告

**新增（相比旧版）：** 文化风险评估——根据目标市场（美国/东南亚/中东等）标注文化冲突点

---

- [ ] **Unit 5: Agent 3 — 文化适配翻译（核心）**

**Goal:** 带完整文化上下文的适配翻译 + 自动生成文化注释（Viki 模式）

**新增（相比旧版）：** 每句翻译附带 cultural_note 字段，自动生成面向海外观众的文化注释

---

- [ ] **Unit 6: Agent 4 — 审校**

**Goal:** 结构化审校，检查文化冲突、翻译腔、术语一致性、角色语气

---

- [ ] **Unit 7: Agent 5 — 终稿 + 出海方案**

**Goal:** 修正翻译 + 生成改编建议 + 推广素材

**新增（相比旧版）：**
- 改编建议书：角色名本地化方案、情节调整建议（短剧/网文场景）
- 游戏场景：角色语气适配建议

---

### Phase 3: Dashboard + 三场景 Demo（Week 4: 5/05-5/11）

- [ ] **Unit 8: CultureBridge Dashboard**

**Goal:** Web 界面，支持三种内容类型输入 + 六件套输出展示

**Approach:**
- 输入区：文本粘贴 / SRT 上传 + 语种选择 + **内容类型选择（短剧/网文/游戏）**
- 进度区：5 Agent 实时状态（SSE）
- 结果区：
  - Tab 1：适配翻译（原文 | Google Translate | CultureBridge 三列对比，文化梗高亮）。Google Translate 结果预计算并硬编码为 JSON fixture，不依赖实时 API
  - Tab 2：翻译决策报告（每个文化梗的知识库依据）——核心差异化展示
  - Tab 3：文化风险报告（带颜色标注的风险等级列表：高/中/低，Tailwind 颜色类实现，不做热力图）
  - Tab 4：文化注释（自动生成的 Viki 式注释，可展开/收起）
  - 加分项 Tab（P2）：改编建议 + 推广素材（时间允许再做）
- **杀手功能：三列对比 + 翻译决策报告。** 评委直接感受到"不是套壳 LLM"。
- **前端估计**：AgentCut 前端 SSE/Job 模式可复用，但 UI 组件需 60-70% 重写（视频制作 UI → 文本对比+报告 UI）

---

- [ ] **Unit 9: 三场景 Demo**

**Goal:** 三个路演级 Demo 场景，证明跨内容形态通用

**P0 核心场景（必须完成）：**

| 场景 | 输入 | 展示重点 |
|------|------|---------|
| 古装宫廷短剧 → 英语 | 20 句台词（臣妾/本宫/冤家/冷宫） | 文化适配 vs Google 直译三列对比 + 翻译决策报告 |
| 修仙网文 → 英语 | 10 章节选段（金丹/元婴/渡劫/道心） | 术语一致性 + 文化注释自动生成 |

**P2 加分场景（Buffer 期，时间允许再做）：**

| 场景 | 输入 | 展示重点 |
|------|------|---------|
| 仙侠游戏对白 → 英语 | 30 条对白（角色语气适配） | 跨内容形态通用性证明 |

**杀手展示**：同一个知识库条目（如"渡劫"）在短剧和网文两个场景中被不同 Agent 引用，证明知识库跨内容形态通用。如果游戏场景完成，三场景一屏展示更佳。

**Demo 质量保证**：输入内容提前锁定为知识库高命中率的脚本，避免现场走 LLM fallback 路径。Google Translate 对比结果预计算并存为 JSON fixture。

**Verification:**
- 三个场景全部端到端跑通
- 翻译零文化冲突错误（人工验证）
- 对比 Google Translate 有明显质量差距
- 录制 3 分钟路演视频

---

### Buffer（5/12-5/25）

**技术 Buffer（5/12-5/16）**——不分配非技术任务：
- Demo 延期修复（如有）
- 知识库扩展至 60+ 条（补充武侠/都市）
- 游戏对白加分场景（如核心场景已完成）
- 对照实验：纯 Claude vs 知识库增强版盲测评分
- 路演视频录制和打磨

**材料准备（5/17-5/25）**：
- 报名注册 + 材料提交
- BP 准备（商业计划书，含 TAM/SAM/SOM 拆分）
- 联系 2-3 个出海团队访谈（验证竞品空白 + 收集付费意愿信号）
- 社媒发帖收集用户反馈

## Success Metrics

| 指标 | 目标 | 如何验证 |
|------|------|--------|
| 翻译质量 | 90+ 分 | Demo 场景人工评分 |
| 文化梗处理 | 零严重错误 | "臣妾"不出现 maid/servant，"渡劫"不出现 robbery |
| 跨场景通用 | 3 场景共享同一知识库 | 同一条映射在短剧/网文/游戏中均正确引用 |
| 任务耗时 | < 5 分钟/千字 | Demo 录屏计时 |
| 任务成本 | < $0.30/千字 | API 调用日志 |
| 文化注释 | 自动生成且准确 | 人工验证 |
| 决策报告 | 每个文化梗有知识库依据 | Demo 展示 |

## Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| 评委认为"套壳 LLM" | Medium | High | 跑对照实验证明知识库增量价值；翻译决策报告展示可审计的适配过程 |
| 评委用 ChatGPT 当场翻译"渡劫"得到正确答案 | Medium | High | 壁垒论证从"LLM 做不到"转为"LLM 黑盒不可审计、长文本术语不一致"，展示决策报告和术语一致性 |
| GhostCut/阅文增加文化适配功能 | Medium | High | 定位 API 上游，主动接触 GhostCut/DubbingX 探索合作；竞品做文化适配也需要知识库，我们有先发优势 |
| GhostCut 已占 70% 翻译市场 | High | Low | 不竞争翻译市场，定位文化层 |
| 知识库 35 条覆盖不足 | Medium | Medium | Demo 输入提前锁定为知识库高命中率脚本；非 Demo 场景用 LLM fallback + "待审核"标记 |
| 没有真实用户 | High | Medium | Buffer 期联系 2-3 个出海团队访谈，收集付费意愿信号 |
| 4 周工期紧张 | High | High | 知识库砍至 35 条 Demo 最小集；游戏场景降为加分项；前端 60-70% 重写已纳入 Week 4 预算 |
| LLM 输出不稳定 | Medium | Medium | temperature 0.3 + 知识库 few-shot 锚定 + 重试 |
| Agent 2 nil path（无文化元素） | Low | Medium | 空 cultural_elements 时 Agent 3 产出标准翻译（无文化适配上下文），Pipeline 正常继续 |
| Claude API 在中国大陆访问受限 | Low | High | 备选 DeepSeek 做翻译输出降级方案 |

## Sustainable Business Model

### 与已有获奖者的产业链定位

```
内容创作 → [CultureBridge: 文化适配] → [GhostCut: 视频翻译] → [DubbingX: 配音] → 海外分发
                    ↑ 我们在这里
```

### 定价策略

| 客户类型 | 定价 | 参考 |
|---------|------|------|
| 短剧出海公司 | 5-20 元/分钟 | 介于纯 AI（0.1 元）和 AI+人工（50 元）之间 |
| 网文出海平台 | 0.05-0.20 元/千字 | 对比人工翻译 0.30-0.60 元/千字 |
| 游戏本地化团队 | 按项目报价 | 对比 Altagram 人工服务 |
| API 调用 | 按 token 计费 | 面向 GhostCut/Vozo 等平台 |

### 三阶段路径

- **Phase 1（参赛+验证）**：三场景 Demo 验证 PMF，精品翻译 SaaS
- **Phase 2（API 上游）**：文化适配 API 输出给翻译/配音平台
- **Phase 3（AI 文化顾问平台）**：跨内容形态的文化出海决策+执行全链路

### 核心壁垒

1. **可审计的文化适配过程**：翻译决策报告让客户看到"为什么这样翻"——所有竞品是黑盒，我们透明。这是唯一竞品真正没有的差异点
2. **术语一致性**：知识库强制长文本中同一概念翻译一致——通用 LLM 在跨章节/跨场景中术语会漂移
3. **文化知识库**：35→100→1,000 条精选高频映射，每条人工审核。宁要 100 条高质量映射也不要 10,000 条 LLM 生成的低质量数据
4. **跨内容形态通用**：一套知识库服务网文/短剧/游戏/动漫等所有中国文化文本内容

**赛后扩展壁垒**（非 Demo 阶段）：建立小型双语文化专家网络（海外华人学者/文化顾问），定期审校和扩充知识库，形成可持续的质量保证机制

### 目标客户

1. **短剧出海公司**——精品剧文化适配（平台首页推荐剧）
2. **网文出海平台**——解决 AI slop 质量问题（古装/仙侠/武侠类）
3. **游戏出海团队**——文化风险扫描 + 对白适配（中小型，请不起 Altagram）
4. **人工翻译公司**——效率工具（TXV/Etrans/火星翻译）

## 比赛叙事

> 中国数字文化出海有三道障碍：语言障碍、声音障碍、文化障碍。
>
> GhostCut 解决了语言障碍——日处理 10 万集翻译。DubbingX 解决了声音障碍——AI 配音拿了文创上海大赛一等奖。
>
> 但文化障碍——至今没有工具化的解决方案。修仙剧西方观众文化折损率 58%，短剧文化适配前后完播率从 20% 飙升到 83%。黑神话悟空做 100 万字本地化时，专门请了文化顾问来确保"Loong"不被翻成"Dragon"。但这种文化把关能力只有头部项目才用得起。
>
> CultureBridge 把这个能力 AI 产品化。我们构建了结构化的中国文化知识库——每个文化概念都有正确翻译、错误翻译、适配原则。输入任何中国文化内容——短剧、网文、游戏——输出带完整文化依据的适配翻译和改编建议。
>
> 不是翻译工具，是 AI 文化顾问。不是做一个赛道，是做所有赛道的底层基础设施。

## Sources & References

### 大赛
- 大赛手册：`2026文创上海大赛手册.pdf`
- 大赛官网：https://www.sccipa.com.cn
- 临港科创城：https://kjc.shlingang.com

### 调研报告
- 完整调研：`docs/research/2026-04-14-idea-research-report.md`

### 市场数据
- 光大证券研报：海外短剧 23.8 亿美元
- 网文翻译市场 38 亿美元（CAGR 10.9%）
- 中国游戏出海 204 亿美元
- [21 经济网：短剧出海下半场](https://www.21jingji.com/article/20260120/herald/0fbea0a0c9367654c54b632c5d6bfb75.html)
- [36氪：2025Q1 海外微短剧市场报告](https://36kr.com/p/3249594364782085)

### 痛点验证
- [Etrans：腾讯微视文化适配案例](https://www.etctrans.com/news/gongsixinwen/2026/0108/2413.html)
- [Nature 2025：Viki 社区字幕组研究](https://www.nature.com/articles/s41599-025-05856-y)
- [ScienceDirect 2026：LLM 文化偏见论文](https://www.sciencedirect.com/science/article/pii/S2949882124000380)
- [Altagram：黑神话悟空本地化案例](https://www.altagram.com/case-studies)
- Reddit r/CDrama, r/noveltranslations, r/MartialMemes
- 知乎、小红书从业者帖子

### 竞品
- [GhostCut](https://jollytoday.com/short-drama-translation/)
- [DubbingX 智声云](https://dubbingx.com)（三届一等奖）
- [Vozo AI](https://www.vozo.ai/)
- [推文科技 FunStory.ai](https://funstory.ai)
- [Gridly](https://gridly.com) / [Lokalise](https://lokalise.com)
