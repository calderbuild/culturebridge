---
title: "feat: CultureBridge 产品打磨 — 从 MVP 到参赛级完美"
type: feat
status: active
date: 2026-04-15
origin: docs/plans/2026-04-14-001-feat-culturebridge-ai-cultural-consultant-plan.md
---

# CultureBridge 产品打磨 — 从 MVP 到参赛级完美

## Overview

MVP 已跑通（5 Agent Pipeline + 75 条知识库 + 3 个 Demo 场景 + Web Dashboard），但存在几个会影响 Demo 质量的关键问题。本计划聚焦"从 80 分到 95 分"的打磨工作。

## Problem Frame

代码审计发现的核心风险：
1. 长文本翻译术语不一致（分 chunk 导致同一概念翻译漂移）
2. 单个 Agent 失败导致整个 Pipeline 崩溃（Demo 现场风险）
3. API 调用无重试，网络抖动直接失败
4. Demo 场景中可能有概念未被知识库覆盖
5. 前端缺少错误反馈和进度估时

## Requirements Trace

- P1. 翻译术语一致性：同一文化概念在整个输出中翻译完全一致
- P2. Pipeline 优雅降级：任何 Agent 失败不阻断全流程，输出部分结果
- P3. API 调用弹性：指数退避重试（3 次），429/503/超时自动重试
- P4. Demo 场景 100% KB 命中：三个 Demo 场景中的每个文化概念都有知识库条目
- P5. 前端错误状态：失败时显示具体原因 + 重试按钮 + 预估耗时

## Implementation Units

- [ ] **Unit 1: API 调用重试机制**

**Goal:** 所有 LLM 调用加指数退避重试，网络抖动不再导致任务失败

**Requirements:** P3

**Dependencies:** None

**Files:**
- Modify: `backend/llm.py` — `_call_openrouter` 加重试逻辑
- Test: `tests/test_llm.py`

**Approach:**
- 最多重试 3 次，间隔 2s/4s/8s
- 只对可重试错误重试：429 (rate limit)、503 (service unavailable)、超时、连接错误
- 400/401/404 等客户端错误不重试，直接抛出
- 记录重试日志

**Test scenarios:**
- Happy path: 正常调用无重试 → 返回结果
- Error path: 首次 503 + 第二次成功 → 返回结果，日志记录 1 次重试
- Error path: 3 次都 503 → 抛出异常，日志记录 3 次重试
- Edge case: 400 错误 → 不重试，直接抛出

**Verification:** 手动断网测试，恢复后自动重连成功

---

- [ ] **Unit 2: Pipeline 优雅降级**

**Goal:** 任何非核心 Agent 失败时输出部分结果，不崩溃

**Requirements:** P2

**Dependencies:** Unit 1

**Files:**
- Modify: `backend/pipeline.py` — 每个 Agent 加 try/except 降级逻辑
- Test: `tests/test_pipeline.py`

**Approach:**
- 核心 Agent（Scanner、Translator）失败 → 仍然报错（没有翻译无法继续）
- 非核心 Agent 失败 → 使用默认空值继续：
  - KB Matcher 失败 → enriched_elements 为空，Translator 用纯 LLM 翻译（无 KB 增强）
  - Reviewer 失败 → 跳过审校，Finalizer 直接用 Translator 输出
  - Finalizer 失败 → 返回 Translator 的原始翻译 + 空的决策报告/推广素材
- SSE 事件标记降级状态：`{"level": "warning", "degraded": true}`
- 前端识别降级状态并显示提示

**Test scenarios:**
- Happy path: 全部成功 → 完整输出
- Error path: Reviewer 超时 → 翻译结果正常输出，审校标记为"已跳过"
- Error path: Finalizer 失败 → 翻译 + 风险报告正常，决策报告为空
- Integration: SSE 流正确推送降级警告事件

**Verification:** 模拟 Reviewer Agent 抛异常，Pipeline 仍然完成并返回翻译结果

---

- [ ] **Unit 3: 翻译术语一致性强制**

**Goal:** 同一文化概念在整个翻译输出中使用完全一致的术语

**Requirements:** P1

**Dependencies:** Unit 1

**Files:**
- Modify: `backend/agents/translator.py` — 加术语锁定机制
- Test: `tests/test_translator.py`

**Approach:**
- 在 Translator Agent 中构建 terminology_lock 字典：`{原文概念: 第一次翻译}` 
- 第一个 chunk 翻译完成后，提取所有文化概念的翻译，锁定为术语表
- 后续 chunk 的 prompt 注入术语锁定表："以下术语必须使用指定翻译，不得更改"
- 术语表来源优先级：知识库 good[0] > 第一个 chunk 的实际翻译
- Reviewer Agent 的审校清单增加"术语一致性检查"维度

**Test scenarios:**
- Happy path: 10 行文本含 3 次"金丹" → 3 次都翻译为"Golden Core"
- Happy path: 跨 chunk 一致性 → chunk1 的"渡劫"=Tribulation，chunk2 的"渡劫"也=Tribulation
- Edge case: 同一概念在不同语境含义不同 → 术语锁保持一致但 cultural_note 可以不同

**Verification:** 输入 30+ 行含重复文化概念的文本，检查输出中术语零不一致

---

- [ ] **Unit 4: Demo 场景 KB 命中率审计 + 补全**

**Goal:** 三个 Demo 场景中的每个文化概念都有知识库条目，零 fallback

**Requirements:** P4

**Dependencies:** None（可与其他 Unit 并行）

**Files:**
- Modify: `backend/knowledge/mappings/palace.json` — 补全缺失条目
- Modify: `backend/knowledge/mappings/xianxia.json` — 补全缺失条目
- Create: `tests/test_kb_coverage.py` — 自动检查 Demo 场景覆盖率
- Modify: `demo/scenarios/*.txt` — 微调文本确保高命中率

**Approach:**
- 对每个 Demo 场景文件，跑 Scanner Agent 提取文化元素
- 对照知识库检查命中/未命中
- 未命中的概念：1) 添加知识库条目 或 2) 微调 Demo 文本避开冷门概念
- 目标：三个场景 100% KB 命中率
- 写一个测试脚本自动验证覆盖率

**Test scenarios:**
- Happy path: palace_drama.txt 所有文化概念 → 100% KB 命中
- Happy path: xianxia_novel.txt 所有文化概念 → 100% KB 命中
- Happy path: game_dialogue.txt 所有文化概念 → 100% KB 命中

**Verification:** 测试脚本输出每个场景的命中率，全部 >= 95%

---

- [ ] **Unit 5: 前端错误状态 + 进度估时 + 体验打磨**

**Goal:** 用户在任何情况下都知道发生了什么、要等多久

**Requirements:** P5

**Dependencies:** Unit 2（需要降级状态 SSE 事件）

**Files:**
- Modify: `frontend/index.html` — 错误面板、估时、字数计数器、降级提示

**Approach:**
- 输入区：实时字数计数器 + 预估耗时（基于字数：< 500 字约 1-2 分钟，500-2000 字约 2-4 分钟）
- 进度区：Agent 卡片显示已用时间（每秒更新）
- 错误状态：Pipeline 失败时显示红色错误面板，含具体失败 Agent 和原因 + "重试"按钮
- 降级提示：某 Agent 降级时卡片显示黄色警告，结果区显示"部分功能已跳过"提示
- 完成状态：显示总耗时和 API 成本估算

**Test scenarios:**
- Test expectation: none — 纯 UI，视觉验证

**Verification:** 
- 正常完成：显示总耗时
- Agent 降级：黄色警告 + "部分功能已跳过"
- Pipeline 失败：红色面板 + 重试按钮

---

## Phased Delivery

### Phase A: 稳定性（Unit 1 + 2）
API 重试 + 优雅降级 → Demo 不会因为网络抖动或 LLM 抽风而崩溃

### Phase B: 质量（Unit 3 + 4）
术语一致性 + KB 覆盖率 100% → 翻译输出经得起逐行审查

### Phase C: 体验（Unit 5）
错误状态 + 估时 + 字数计数 → 用户始终知道发生了什么

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| 术语锁定导致翻译僵化 | 只锁定知识库中有条目的概念，其他概念允许自由翻译 |
| 降级逻辑过度宽容导致低质量输出 | Scanner 和 Translator 失败仍然报错，只有辅助 Agent 允许降级 |
| KB 补全工作量超预期 | 优先补全 Demo 场景出现的概念，非 Demo 概念用 fallback 标记 |
