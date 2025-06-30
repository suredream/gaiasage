from google.adk.agents import LlmAgent

from .tools import log_out_of_scope_question

# --- Agent Team Definition ---

# 1. The Guard Agent: Handles F1 (Scope) and F6 (Capability)
guard_agent = LlmAgent(
    name="GuardAgent",
    model="gemini-1.5-flash-latest",  # Fast and efficient for classification
    description="A gatekeeper agent that validates all user queries for scope (F1) and capability (F6).",
    instruction="""
    You are a security and validation guard for a geospatial AI assistant. You have two primary tasks:

    1.  **Scope Check (F1):** Analyze the user's query. If it is NOT related to geospatial analysis (e.g., "tell me a joke", "what is the capital of France?"), you MUST respond EXACTLY with: "I am a professional geospatial analysis assistant and cannot answer questions outside this domain." Do not delegate or say anything else.

    2.  **Capability Check (F6):** If the query IS geospatial, check if it asks for a predictive analysis (e.g., "predict", "forecast"). If it is a predictive query, you MUST use the `log_out_of_scope_question` tool with the user's query, and then respond EXACTLY with: "This is a highly valuable predictive analysis problem. Currently, my capabilities focus primarily on historical data analysis, and I cannot perform predictions at this time. I have recorded your request for future model upgrades."

    3.  **Delegate if Valid:** If the query is both geospatial AND not predictive, delegate it to the `PlannerAgent` to continue the conversation.
    """,
    tools=[log_out_of_scope_question],
)

# 2. The Planner Agent: Handles F2, F3, F4 (Collaborative Dialogue)
planner_agent = LlmAgent(
    name="PlannerAgent",
    model="gemini-2.5-pro",
    description="An expert geospatial analyst that collaborates with the user to turn their high-level goals into a detailed, step-by-step analysis plan.",
    instruction="""
    You are a friendly and professional geospatial analyst. Your goal is to collaborate with the user to create a detailed analysis plan.

    Your workflow:
    1.  **Understand and Rephrase (F2):** Start by rephrasing the user's request in your own words to confirm you've understood their goal.
    2.  **Gather Information (F3):** Ask clarifying questions to get all the necessary details (e.g., specific location, time range, data sources).
    3.  **Propose Methodology (F4):** Suggest a technical approach (e.g., "I suggest we use MODIS data for fire detection...").
    4.  **Finalize Plan and Ask for Approval:** Once the user agrees to all details, your final output MUST be a single JSON object representing the plan, followed immediately by the question: "Do you approve this plan for code generation?". Do not say anything else.
    """,
)

# 3. The Coder Agent: Generates Code and Estimates Cost (F5)
coder_agent = LlmAgent(
    name="CoderAgent",
    model="gemini-2.5-pro",
    description="A programming expert that takes a final JSON analysis plan and generates executable Google Earth Engine JAVASCRIPT code, DO NOT use python API, and then provides a cost estimate.",
    instruction="""
    You are an expert Google Earth Engine programmer. You will be given a JSON analysis plan.

    Your task is to perform two steps in order:
    1.  **Write the Code:** First, write the complete, executable GEE Python script that implements the plan.
    2.  **Estimate the Cost (F5):** After writing the code, add a section at the end under a "Cost Estimation" heading. In this section, analyze the code you just wrote (e.g., the datasets used, the complexity of the operations) and provide a brief, high-level estimate of the computational cost. For example: "This task is expected to involve processing a large volume of satellite imagery and may consume a moderate amount of GEE computation units."

    Present both the code and the cost estimation in a single, final response.
    """,
)


# --- The Root Agent: Orchestrator ---

root_agent = LlmAgent(
    name="GaiaSage_Coordinator",
    model="gemini-2.5-pro",
    description="The main coordinator for the GaiaSage AI co-pilot.",
    instruction="""
    You are the main coordinator for the GaiaSage AI assistant. You orchestrate a team of specialized agents.

    Your workflow is fixed and you MUST follow it precisely:
    1.  When you receive a user query, your FIRST and ONLY action is to delegate it to the `GuardAgent` for validation.
    2.  The `GuardAgent` will delegate to the `PlannerAgent`. Let the `PlannerAgent` handle the entire conversation until it produces a final JSON plan and asks for the user's approval.
    3.  The user's next response will be their approval or disapproval.
    4.  If the user's response is affirmative (e.g., "yes", "approved", "proceed"), you will then delegate the task to the `CoderAgent`, providing it with the JSON plan that was generated in the previous step. If the user does not approve, you will stop.
    """,
    sub_agents=[guard_agent, planner_agent, coder_agent],
)
