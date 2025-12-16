import pytest

from gaiasage.agent import (
    OUT_OF_SCOPE_RESPONSE,
    PREDICTIVE_RESPONSE,
    orchestrate_user_message,
)
from gaiasage.tools import clear_logged_questions, logged_out_of_scope_questions


def setup_function() -> None:
    clear_logged_questions()


def test_guard_off_topic_returns_contract_response() -> None:
    response, state = orchestrate_user_message(
        "What is the capital of France?", deterministic=True
    )

    assert response == OUT_OF_SCOPE_RESPONSE
    assert state.guard_decision == "out_of_scope"
    assert logged_out_of_scope_questions == []


def test_guard_predictive_logs_and_returns_capability_message() -> None:
    message = (
        "Using historical data, predict next year's deforestation hotspots in Brazil."
    )
    response, state = orchestrate_user_message(message, deterministic=True)

    assert response == PREDICTIVE_RESPONSE
    assert state.guard_decision == "predictive"
    assert logged_out_of_scope_questions == [message]


def test_coder_not_triggered_without_approval() -> None:
    # Should delegate guard and halt before coder when approval is False.
    coder_called = {"called": False}

    def coder_stub(plan: str) -> str:
        coder_called["called"] = True
        return f"code for {plan}"

    response, state = orchestrate_user_message(
        "Compute an NDVI summary for the Amazon rainforest.",
        approval=False,
        plan_json='{"task": "ndvi"}',
        deterministic=True,
        coder_callable=coder_stub,
    )

    assert response.startswith("Plan not approved")
    assert state.guard_decision == "delegate"
    assert state.approved is False
    assert coder_called["called"] is False
