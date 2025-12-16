"""
Utility tools used by GaiaSage agents.

The logging tool keeps side effects auditable and testable without external services.
"""

from __future__ import annotations

import logging
from typing import List

logger = logging.getLogger(__name__)

# In-memory log for assertions during tests and local debugging.
logged_out_of_scope_questions: List[str] = []


def log_out_of_scope_question(question: str) -> str:
    """
    Record an out-of-scope or predictive request for auditability.

    Returns a short acknowledgment so tool execution can be surfaced in agent traces.
    """

    logged_out_of_scope_questions.append(question)
    logger.info("Logged out-of-scope or predictive request: %s", question)
    return "logged"


def clear_logged_questions() -> None:
    """Reset the in-memory log; useful for isolated tests."""

    logged_out_of_scope_questions.clear()
