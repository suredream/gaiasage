---
created_by: Jun, gemini
reviewed: true
last_updated: 2025-06-30
---

# Architecture

## Background

Use google Agent Development Kit (ADK) to build a chatbot(AI agent) for the geospatial analysis domain.

## Structure of the project

```text
/
├── plans/               # AI prompts and task decomposition
│   ├── 01_xx_plan.md
│   └── 02_xx_plan.md
├── docs/                # Human-readable documents
│   ├── ARCH.md          # Architecture
│   └── features/        # New features
│       ├── 01_xx.md
│       └── 02_xx.md
├── tests/
└── ... (Other project files)
```

## Core Documentation

The following md files are created manually by Jun, as context for guide AI coder
- ARCH.md: Architecture instruction

The other ai.md files are created by the AI coder for human reader 
- tour.ai.md                  # High-level walk-through on how the components work together
- ui_guide.ai.md              # User guide on the visualization app

`README.md` and `Devel_notes.md` are used for high-level takeaways, for human readers / reviewers. 


## Technology Stackls

- Language: Python
- Package Manager: uv (<https://github.com/astral-sh/uv>)
- AI Agent Framework: Google ADK (Agent Development Kit)
- Model: Gemini 2.5 Pro
- Database: PostgreSQL

## Extra Notes

- Must use @context7 to get lastest docs of Google ADK (Agent Development Kit)
- Must use uv to manage dependencies (uv init && uv sync)
