"""
Agno-based agent skeleton for GaiaSage.

This module defines the Guard/Planner/Coder agents and the coordinating team.
The orchestration state remains explicit in Python to avoid LLM-managed control flow.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal, Optional, Tuple

from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team

from .tools import log_out_of_scope_question

# --- Contracted responses used by the Guard agent ---
OUT_OF_SCOPE_RESPONSE = "I am a professional geospatial analysis assistant and cannot answer questions outside this domain."
PREDICTIVE_RESPONSE = (
    "This is a highly valuable predictive analysis problem. Currently, my capabilities focus primarily on "
    "historical data analysis, and I cannot perform predictions at this time. I have recorded your request for "
    "future model upgrades."
)


@dataclass
class OrchestrationState:
    """Explicit state holder for the multi-agent conversation."""

    last_user_message: Optional[str] = None
    plan_json: Optional[str] = None
    approved: bool = False
    guard_decision: Optional[str] = None
    notes: list[str] = field(default_factory=list)


# --- Agent Team Definition (Agno) ---

# 1. The Guard Agent: Handles F1 (Scope) and F6 (Capability)
guard_agent = Agent(
    name="GuardAgent",
    model=Gemini(id="gemini-2.0-flash-lite"),
    description="A gatekeeper agent that validates all user queries for scope (F1) and capability (F6).",
    instructions="""
    You are a security and validation guard for a geospatial AI assistant. You have two primary tasks:

    1.  Scope Check (F1): Analyze the user's query. If it is NOT related to geospatial analysis (e.g., "tell me a joke",
        "what is the capital of France?"), you MUST respond EXACTLY with: "I am a professional geospatial analysis
        assistant and cannot answer questions outside this domain." Do not delegate or say anything else.

    2.  Capability Check (F6): If the query IS geospatial, check if it asks for a predictive analysis (e.g., "predict",
        "forecast"). If it is a predictive query, you MUST use the `log_out_of_scope_question` tool with the user's
        query, and then respond EXACTLY with: "This is a highly valuable predictive analysis problem. Currently, my
        capabilities focus primarily on historical data analysis, and I cannot perform predictions at this time. I have
        recorded your request for future model upgrades."

    3.  Delegate if Valid: If the query is both geospatial AND not predictive, delegate it to the `PlannerAgent` to
        continue the conversation.
    """,
    tools=[log_out_of_scope_question],
)

# 2. The Planner Agent: Handles F2, F3, F4 (Collaborative Dialogue)
planner_agent = Agent(
    name="PlannerAgent",
    model=Gemini(id="gemini-2.0-flash-lite"),
    description="An expert geospatial analyst that collaborates with the user to turn goals into a step-by-step plan.",
    instructions="""
    You are a friendly and professional geospatial analyst. Your goal is to collaborate with the user to create a
    detailed analysis plan.

    Workflow:
    1.  Understand and Rephrase (F2): Start by rephrasing the user's request in your own words to confirm you've
        understood their goal.
    2.  Gather Information (F3): Ask clarifying questions to get all the necessary details (e.g., specific location,
        time range, data sources).
    3.  Propose Methodology (F4): Suggest a technical approach (e.g., "I suggest we use MODIS data for fire
        detection...").
    4.  Finalize Plan and Ask for Approval: Once the user agrees to all details, your final output MUST be a single JSON
        object representing the plan, followed immediately by the question: "Do you approve this plan for code
        generation?". Do not say anything else.
    """,
)

# 3. The Coder Agent: Generates Code and Estimates Cost (F5)
coder_agent = Agent(
    name="CoderAgent",
    model=Gemini(id="gemini-1.5-flash"),
    description=(
        "A programming expert that takes a final JSON analysis plan and generates executable Google Earth Engine "
        "JavaScript code, then provides a cost estimate."
    ),
    instructions="""
    You are an expert Google Earth Engine programmer. You will be given a JSON analysis plan.

    Your task is to perform two steps in order:
    1.  Write the Code: First, write the complete, executable GEE JavaScript script that implements the plan. Do NOT use
        the Python API.
    2.  Estimate the Cost (F5): After writing the code, add a section at the end under a "Cost Estimation" heading. In
        this section, analyze the code you just wrote (e.g., the datasets used, the complexity of the operations) and
        provide a brief, high-level estimate of the computational cost. For example: "This task is expected to involve
        processing a large volume of satellite imagery and may consume a moderate amount of GEE computation units."

    Present both the code and the cost estimation in a single, final response.
    """,
    markdown=True,
)


# --- The Root Agent: Orchestrator ---

root_team = Team(
    members=[guard_agent, planner_agent, coder_agent],
    name="GaiaSage_Coordinator",
    model=Gemini(id="gemini-2.0-flash-lite"),
    description="The main coordinator for the GaiaSage AI co-pilot.",
    instructions="""
    You are the main coordinator for the GaiaSage AI assistant. You orchestrate a team of specialized agents.

    Workflow (must be followed):
    1.  When you receive a user query, your FIRST and ONLY action is to delegate it to the `GuardAgent` for validation.
    2.  The `GuardAgent` will delegate to the `PlannerAgent`. Let the `PlannerAgent` handle the entire conversation
        until it produces a final JSON plan and asks for the user's approval.
    3.  The user's next response will be their approval or disapproval.
    4.  If the user's response is affirmative (e.g., "yes", "approved", "proceed"), you will then delegate the task to
        the `CoderAgent`, providing it with the JSON plan that was generated in the previous step. If the user does not
        approve, you will stop.
    """,
    respond_directly=True,
)

# Alias retained for compatibility with prior entry point naming
root_agent = root_team


# --- Minimal deterministic orchestrator helpers (for tests and gating) ---

GuardDecision = Literal["out_of_scope", "predictive", "delegate"]


@dataclass
class GuardResult:
    decision: GuardDecision
    response: Optional[str] = None


def _normalize_output_text(output: object) -> str:
    """Best-effort extraction of text from Agent/Team run output."""

    if output is None:
        return ""
    if isinstance(output, str):
        return output
    # Agno RunOutput exposes `.content`; default to string repr otherwise.
    content = getattr(output, "content", None)
    if isinstance(content, str):
        return content
    return str(output)


def _looks_geospatial(message: str) -> bool:
    """Lightweight heuristic to keep guard deterministic in tests."""

    terms = [
        "ndvi",
        "nightlight",
        "lake",
        "deforestation",
        "forest",
        "satellite",
        "gee",
        "geospatial",
        "spatial",
        "location",
        "distance",
        "geometry",
        "map",
    ]
    lower = message.lower()
    return any(term in lower for term in terms)


def _is_predictive(message: str) -> bool:
    predictive_terms = ["predict", "prediction", "forecast", "forecasting"]
    lower = message.lower()
    return any(term in lower for term in predictive_terms)


def run_guard_check(user_message: str, *, deterministic: bool = True) -> GuardResult:
    """
    Execute the Guard gate.

    In deterministic mode, use lightweight heuristics to avoid live LLM calls during tests.
    Otherwise, delegate to the Agno guard agent and classify based on its output.
    """

    if deterministic:
        if not _looks_geospatial(user_message):
            return GuardResult(decision="out_of_scope", response=OUT_OF_SCOPE_RESPONSE)
        if _is_predictive(user_message):
            log_out_of_scope_question(user_message)
            return GuardResult(decision="predictive", response=PREDICTIVE_RESPONSE)
        return GuardResult(decision="delegate")

    guard_output = guard_agent.run(user_message)
    guard_text = _normalize_output_text(guard_output)

    if guard_text.strip() == OUT_OF_SCOPE_RESPONSE:
        return GuardResult(decision="out_of_scope", response=guard_text)

    if guard_text.strip() == PREDICTIVE_RESPONSE:
        return GuardResult(decision="predictive", response=guard_text)

    return GuardResult(decision="delegate")


def orchestrate_user_message(
    user_message: str,
    *,
    approval: Optional[bool] = None,
    plan_json: Optional[str] = None,
    deterministic: bool = True,
    coder_callable: Optional[Callable[[str], str]] = None,
) -> Tuple[str, OrchestrationState]:
    """
    Minimal orchestration stub to gate Planner/Coder execution paths.

    The Planner/Coder bodies are intentionally left thin; tests can inject `coder_callable`
    to assert gating behavior without invoking real models.
    """

    state = OrchestrationState(last_user_message=user_message)

    guard_result = run_guard_check(user_message, deterministic=deterministic)
    state.guard_decision = guard_result.decision

    if guard_result.decision != "delegate":
        return guard_result.response or "", state

    # Planner placeholder: record plan_json if provided, otherwise leave None.
    state.plan_json = plan_json

    if approval is None:
        # Waiting for user approval after Planner step.
        return "Awaiting plan approval.", state

    if approval is False:
        state.approved = False
        return "Plan not approved. Stopping.", state

    # approval is True
    state.approved = True
    selected_plan = plan_json or "{}"
    coder_callable = coder_callable or (lambda plan: f"Generated code for plan: {plan}")
    coder_response = coder_callable(selected_plan)
    return coder_response, state
