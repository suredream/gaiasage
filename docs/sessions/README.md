# Sessions

This directory contains **AI coding session records**.

A session represents **one bounded unit of AI-assisted work** with a clear goal,
explicit constraints, and verifiable outcomes.

Sessions exist to make AI behavior:
- Auditable
- Reviewable
- Comparable over time

They are not meant to be verbose or bureaucratic.

---

## When to Create a Session

Create a session record whenever:
- An AI system modifies code or documentation
- An AI agent performs multi-step reasoning or planning
- The scope of work is non-trivial or review-sensitive

In practice:
> **One pull request = one session**

Small changes may use short sessions.

---

## What a Session Is (and Is Not)

### A session **is**
- A declaration of intent and constraints
- A record of what was actually done
- A source of evidence for verification

### A session **is not**
- A design document
- A substitute for tests
- A narrative of the entire development history

---

## How Sessions Are Used

### During Development
- The session defines the allowed modification scope
- The AI must not exceed session boundaries
- Unclear constraints require pausing and clarification

### During Review
- Reviewers should read the session **before** reviewing the diff
- The session explains *why* changes exist, not just *what* changed

### After Merge
- Sessions become part of the audit trail
- They enable structured retrospectives on AI behavior

---

## Using Sessions to Evaluate AI Performance

Sessions make it possible to analyze AI agents beyond anecdotal feedback.

Common signals to look for:
- Repeated scope violations
- Frequent assumption corrections
- High number of partial or blocked sessions
- Mismatch between planned and actual changes
- Test gaps introduced or left unresolved

Over time, these patterns inform:
- Better prompts and constraints
- Clearer conventions and contracts
- Decisions on where human intervention is required

---

## Naming & Organization

Recommended naming format: session-YYYY-MM-DD-short-topic.md

All completed sessions should remain in this directory.
Do not delete sessions, even if outcomes were unsuccessful.

---

## Authority

Session records operate under:
- `AI_CONVENTIONS.md` (general rules)
- `GEMINI.md` (project-specific rules, if applicable)

If a session conflicts with these documents, it must be revised or invalidated.

---

**Sessions are lightweight by design.  
Their value comes from consistency, not detail.**
