# CultureBridge Demo

## 运行方式

```bash
# 安装依赖
pip install -r backend/requirements.txt

# 配置 API Key
cp .env.example .env
# 编辑 .env，填入 OpenRouter API Key

# 启动服务
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# 打开浏览器访问 http://localhost:8000
```

## Demo 场景

### 场景 1：古装宫廷短剧 → 英语

点击页面上的"宫廷剧 Demo"按钮，或手动粘贴 `demo/scenarios/palace_drama.txt` 中的内容。

展示重点：
- "臣妾"不会被翻译成 maid/servant
- "打入冷宫"正确翻译为 "Banish to the Cold Palace"
- "翻牌子""侍寝"等敏感文化概念的委婉处理
- 三列对比（原文 vs Google Translate vs CultureBridge）

### 场景 2：修仙网文 → 英语

点击"修仙网文 Demo"按钮，或手动粘贴 `demo/scenarios/xianxia_novel.txt` 中的内容。

展示重点：
- 修仙术语一致性（Golden Core, Nascent Soul, Tribulation）
- 文化注释自动生成（Viki 模式）
- 文化风险报告
