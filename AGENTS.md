# AGENTS.md  
**AI models Usage Convention — GaiaSage**

This document defines **project-specific rules** for using OpenAI models in GaiaSage.
If any rule conflicts with `AI_CONVENTIONS.md`, this file takes precedence.
Always respond in Chinese in Chat mode, while coding and document in English.

---

## Project Context
GaiaSage is an AI co-pilot for **geospatial analysis**.
Domain correctness and safety are first-class constraints.

---

## Domain & Capability Constraints
- The system addresses **geospatial analysis only**.
- Non-geospatial requests must return the approved out-of-scope response.
- Predictive or unsupported requests must:
  1. Be recorded via approved logging tools
  2. Return the approved capability-limitation response

Exact response strings are part of the system contract.

---

## Agent Architecture Rules
- Agent orchestration and state management must be implemented in Python.
- LLMs must not be relied upon to implicitly manage workflow or session state.
- Any agent output used for decisions must be normalized into structured data.

---

## Model Usage Guidelines
- High-capability models are reserved for planning and code generation.
- Lightweight models may be used for guard or classification tasks.
- Any change to model roles or selection requires documentation (ADR).

---

## Tooling Rules
- Tools represent auditable side effects.
- Logging of out-of-scope or unsupported requests is mandatory where applicable.

---

## Deployment Awareness
- Code must remain compatible with:
  - uv-managed environments
  - CI execution
  - Vercel-based deployment targets
- Runtime-only assumptions not verifiable in CI are prohibited.

---

## Prohibited Behaviors
- Expanding scope beyond geospatial analysis
- Silent changes to agent roles or workflow
- Hidden prompts, memory, or side effects
- Overriding safety or domain guards

---

**This file is authoritative for all OpenAI usage in GaiaSage.**
