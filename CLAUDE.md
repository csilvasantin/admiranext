# Proyecto 02 — admiranext

> Instructions for Claude & Codex

This file provides context for AI agents (Claude Code, Codex, etc.) working on this project.

## Project Overview

**AdmiraNext** is a unified AI council system with 16 agents organized into two sides, each mapped to a physical machine:

- 🎨 **Creativo** (MacBookAirBlanco) — CCO, CDO, CXO, CSO
- 🧠 **Racional** (MacBookAir16) — CEO, CTO, COO, CFO

Each side has two generational groups:
- ⭐ **Leyendas** — Legendary historical figures
- 🚀 **Coetáneos** — Contemporary leaders

## Architecture

```
admiranext/
├── agents/
│   ├── base.py              # CouncilAgent base class (Claude API calls)
│   ├── creativo/             # Creative side agents
│   │   ├── leyendas/         # Disney, Rams, Schultz, Lucas
│   │   └── coetaneos/        # Lasseter, Ive, Devlin, Reynolds
│   └── racional/             # Rational side agents
│       ├── leyendas/         # Jobs, Wozniak, Cook, Buffett
│       └── coetaneos/        # Musk, Huang, Shotwell, Hood
├── council.py                # Council orchestrator (GROUPS dict, parallel execution)
├── brainstorming.py          # HTML document generator
├── orgchart.py               # Org chart HTML generator
└── models.py                 # Brief, AgentResponse, CouncilOutput dataclasses
```

## Key Design Decisions

1. **CouncilAgent base class** (`agents/base.py`): All 16 agents inherit from this. It handles Claude API calls, the 3-round flow (propose → debate → synthesize), and has a `side` attribute ("creativo" or "racional") that determines the synthesis structure.

2. **GROUPS dict** (`council.py`): Central registry mapping group keys to agent classes, labels, side, generation, and machine. Adding a new group means adding an entry here.

3. **Parallel execution**: Proposals and debates run in parallel using `ThreadPoolExecutor(max_workers=4)`. Synthesis is sequential (leader only).

4. **HTML generation** (`brainstorming.py`): Self-contained HTML with inline CSS. No external dependencies. Uses a custom `_md_to_html()` converter.

5. **Multi-machine mapping**: Each group is tagged with a `machine` field. The creative side runs on MacBookAirBlanco, rational on MacBookAir16. This is informational — the code runs on whichever machine has the API key.

## How to Add a New Agent

1. Create a new file in the appropriate directory (e.g., `agents/racional/leyendas/cmo.py`)
2. Inherit from `CouncilAgent` and set: `name`, `role`, `persona`, `category`, `side`, `system_prompt`
3. Add the class to the group's `__init__.py`
4. Add the class to the appropriate group in `GROUPS` dict in `council.py`
5. Add persona data to `AGENT_PERSONAS` in `brainstorming.py`
6. Add color to `_CREATIVE_COLORS` or `_RATIONAL_COLORS` in `brainstorming.py`
7. Add icon to `_CREATIVE_ICONS` or `_RATIONAL_ICONS` in `brainstorming.py`
8. Update `COUNCIL_DATA` in `orgchart.py`
9. Update banner and selector in `main.py`

## How to Add a New Group

1. Create the agent directory and files following the pattern above
2. Add entry to `GROUPS` in `council.py` with: `label`, `side`, `generation`, `machine`, `agents`
3. Add persona entries to `AGENT_PERSONAS` in `brainstorming.py`
4. Add label to `GROUP_LABELS` in `brainstorming.py`
5. Add banner to `BANNERS` in `main.py`
6. Update `select_council()` in `main.py`

## Council Flow

```
Brief → Ronda 1 (4 proposals in parallel)
      → Ronda 2 (4 debate responses in parallel, each sees other 3 proposals)
      → Synthesis (leader agent integrates all 8 contributions)
      → HTML Brainstorming document generated
```

## Dependencies

- `anthropic` — Claude API SDK
- `python-dotenv` — Environment variable loading
- `rich` — Terminal UI (panels, markdown, colors)

## Testing

```bash
cd ~/AdmiraNext
python3 -c "from admiranext.council import Council, GROUPS; print(list(GROUPS.keys()))"
python3 main.py  # Interactive mode
```

## Environment

- Python 3.9+ (uses `from __future__ import annotations` for type hints)
- Requires `ANTHROPIC_API_KEY` in `.env` file
- Model: `claude-sonnet-4-20250514`

## Potential Improvements

- [ ] Add async support (replace ThreadPoolExecutor with asyncio + httpx)
- [ ] Add a "full council" mode where both sides debate the same brief
- [ ] Add streaming responses for real-time output in CLI
- [ ] Add PDF export alongside HTML
- [ ] Add inter-council debates (creative vs rational on same topic)
- [ ] Add memory/history — agents remember previous briefs
- [ ] Add web UI (Flask/FastAPI) as alternative to CLI
- [ ] Add tests with mocked API responses
- [ ] Generate pixel art for the rational side council image
