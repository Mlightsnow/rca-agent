# rca-agent

Root Cause Analysis (RCA) auto-diagnosis MVP built on
[`deepagents`](https://github.com/langchain-ai/deepagents).

This repo wires up the agent loop end-to-end:

- custom **system prompt**
- custom **tools** (stubs — real implementations land later)
- custom **model** (default: a self-hosted LiteLLM proxy)
- custom **subagents** + **SKILL.md** packs

It does **not** yet ship real diagnostic logic. The focus is the
integration seam — adding tools, subagents, or swapping models is a
one-file change.

## Quickstart

```bash
pip install -e ".[dev]"
cp .env.example .env   # fill in RCA_MODEL / RCA_MODEL_BASE_URL / RCA_MODEL_API_KEY
pytest -q              # offline tests, no network
python -m rca_agent "Service X 5xx spike at 10:00 UTC"
```

## Layout

```
src/rca_agent/
  agent.py          # build_agent() — only file that imports deepagents
  config.py         # Settings (pydantic-settings)
  prompts/          # system.md + per-subagent .md
  models/           # model factory (LiteLLM-as-OpenAI by default)
  tools/            # @rca_tool stubs (run_shell, search_logs, ...)
  subagents/        # log_analyzer, metric_analyzer, hypothesis_validator
  skills/           # SKILL.md packs (deepagents SkillsMiddleware)
  cli.py
tests/              # offline tests using FakeListChatModel
```
