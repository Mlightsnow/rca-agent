# rca-agent

基于 [deepagents](https://github.com/langchain-ai/deepagents) 的 RCA 自动根因诊断 MVP。

## 当前完成范围（MVP）

- ✅ 自定义 Prompt 组装（含 skills 注入）
- ✅ 自定义 Tools 接入层（当前留空，保留扩展点）
- ✅ 自定义 Model 解析层（当前最小实现，后续可接入多 provider 配置）
- ✅ Skills 本地加载（`skills/<name>/SKILL.md`）
- ✅ 本地 bash/CLI 运行循环（不启用沙箱/容器）
- ✅ 基础测试（prompt、skills、agent wiring）

## 目录结构

```text
src/rca_agent/
  agent.py       # deepagents agent loop 组装
  cli.py         # 本地运行入口
  config.py      # 运行配置
  models.py      # 模型扩展点
  prompts.py     # 系统提示词构建
  skills.py      # skills 加载
  tools.py       # 工具扩展点
skills/
  rca_baseline/SKILL.md
tests/
```

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m rca_agent.cli
```

## 如何扩展

### 1) 自定义 Tools

在 `src/rca_agent/tools.py` 中实现工具函数，并在 `build_toolset()` 返回可调用对象列表。

### 2) 自定义 Model

在 `src/rca_agent/models.py` 中扩展 `resolve_model()`，可增加 provider 鉴权、路由策略、fallback 策略。

### 3) 自定义 Skills

新增文件：

```text
skills/<your_skill>/SKILL.md
```

启动时自动加载并拼接到系统 prompt。

## 设计原则

- 测试先行：以最小单测覆盖核心拼装逻辑
- 模块清晰：按 prompt / tools / models / skills / loop 解耦
- 功能解耦：每一层均可独立替换
- 扩展性优先：为后续接入更多工具、记忆、子 agent、沙箱执行预留接口
