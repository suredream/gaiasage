---
created_by: augment
reviewed: true
last_updated: 2025-06-30
---

# Execution Plan: TerraMind (The AI Does the Work)

## 1. Core Principle

The AI will be responsible for the entire intellectual workflow, from understanding the user's intent to planning the analysis, writing the code, and estimating the cost. The developer's role is to provide the high-level architecture and guidance, not to implement the core intelligence.

## 2. The Corrected Agent Team

1. **`GuardAgent` (Handles F1 & F6)**: The gatekeeper. It uses a `log_out_of_scope_question` tool for F6.
2. **`PlannerAgent` (Handles F2, F3, F4)**: The collaborative analyst. It has no tools.
3. **`CoderAgent` (Generates Code & F5)**: The programmer. It has no tools. It will:
    * Receive the JSON plan and write the GEE code as its direct response.
    * After generating the code, it will analyze the code it just wrote and provide a cost estimation (F5) using its own intelligence.

## 3. The Corrected Workflow

This is the final workflow. The core logic is handled by the agents' intelligence, not by pre-written tools.

```mermaid
graph TD
    U[User Enters Query] --> R{RootAgent};
    R --> G[GuardAgent];
    G --> F1_Decision{Is it Geospatial? (F1)};
    F1_Decision -- No --> O_Reject["Sorry, I can't help..."];
    F1_Decision -- Yes --> F6_Decision{Is it Supported? (F6)};
    F6_Decision -- No --> O_Log["Log request & inform user (F6)"];
    F6_Decision -- Yes --> R;

    R --> P[PlannerAgent];
    P --> P_Dialogue("Collaborative Dialogue (F2, F3, F4)");
    P_Dialogue --> U_Confirm{User Confirms Plan?};
    U_Confirm -- No --> P_Dialogue;
    U_Confirm -- Yes --> P_Finalize[PlannerAgent outputs final JSON plan];
    
    P_Finalize --> R;
    R --> C[CoderAgent receives plan];
    C --> C_Generate[1. CoderAgent **writes code directly**];
    C_Generate --> C_Estimate[2. CoderAgent **estimates cost of its own code (F5)**];
    C_Estimate --> R;
    R --> O_Code[Final GEE Script with Cost Estimate];
```

## 4. The Corrected Task Breakdown

### Phase 1: The Guard & Planner Agents

* **Goal:** Build the gatekeeper and the collaborative planner.
* **Tasks:**
    1. **Define `GuardAgent`:** Create an agent to handle F1 and F6, using a `log_out_of_scope_question` tool.
    2. **Define `PlannerAgent`:** Create an agent with no tools to handle the F2, F3, and F4 dialogue.
    3. **Define `RootAgent`:** Create the orchestrator for the Guard -> Planner flow.
    4. **Revise Tests:** Update tests to validate the F1 and F6 scenarios.

### Phase 2: The Intelligent Coder Agent

* **Goal:** Implement a `CoderAgent` that handles the entire technical implementation.
* **Tasks:**
    1. **Define `CoderAgent`:** Create an `LlmAgent` with a detailed, two-step instruction: first, write the GEE code based on the plan; second, analyze that code to estimate the cost. It will have **NO tools**.
    2. **Update `RootAgent` Orchestration:** The `RootAgent` will manage the full workflow, passing the plan to the `CoderAgent` and presenting the final, combined result (code + cost estimate) to the user.
    3. **Update Tests:** Add tests to validate that the `CoderAgent` can generate code and a plausible cost estimate from a given plan.
