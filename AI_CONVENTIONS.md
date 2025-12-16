# AI_CONVENTIONS.md  
**General AI Usage & Coding Conventions**

## Purpose
This document defines **general rules** for using AI systems as coders or agents in Python projects managed with **uv**.

Goals:
- Correctness and reproducibility
- Controlled autonomy
- Testability and auditability
- Minimal architectural drift

These rules apply to all AI-assisted activities unless explicitly overridden by project-specific conventions.

---

## Scope of AI Authority
AI systems may:
- Read and reason over existing code and documentation
- Propose and implement changes within explicit constraints
- Generate tests, scripts, and documentation

AI systems must not:
- Change architecture or public interfaces without approval
- Modify files outside the allowed scope
- Invent undocumented APIs, data, or capabilities

If constraints are unclear, the AI must stop and ask.

---

## Change Control Principles
1. Small, reviewable changes are preferred.
2. File/path allowlists are required for non-trivial work.
3. Deterministic or rule-based solutions are preferred when feasible.

---

## Testing & Verification
- Any logic-affecting behavior must be verifiable.
- Tests or validation artifacts are required unless explicitly exempted.
- Passing the project’s standard check script is the minimum acceptance bar.

---

## Tool Usage
- Tools define explicit side-effect boundaries.
- Tools must be single-purpose and independently testable.
- Tool calls may be logged and asserted in tests.

---

## AI Coding Sessions
Each AI-assisted session must define:
- A clear objective
- A bounded modification scope
- Completion evidence (tests, logs, artifacts)

AI systems must not silently exceed session boundaries.

---

**This file is authoritative for all AI-assisted work.**
