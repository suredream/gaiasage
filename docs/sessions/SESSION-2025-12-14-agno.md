## 1. Session Metadata
- Session ID: session-2025-12-14-agno
- Date: 2025-12-14
- Initiated by: suredream
- Related Docs: SPEC.md, AI_CONVENTIONS.md, GEMINI.md

## 2. Objective
使用 **Agno**，完成“多代理骨架代码”落地，并补齐最小可行测试，使得核心域/能力边界行为可回归验证。  
本 session 的目标是“骨架 + 可测”，不是功能完善或上线部署。

## 3. Scope & Constraints

### Allowed Modifications (Allowlist)
仅允许修改/新增以下路径：
- `pyproject.toml`（新增 agno 及必要依赖；移除或保留 google-adk 需明确记录原因）
- `src/gaiasage/agent.py`（用 Agno 实现如下的 Guard/Planner/Coder/Root 结构骨架）

```
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
```

- `src/gaiasage/tools.py`（如需为测试增加可注入/可断言的日志接口；不得改变既有工具语义）
- `tests/` 下的测试文件（新增或修改以覆盖 Guard 行为与编排门控）
- `docs/sessions/`（本 session 记录与必要补充说明）

### Explicitly Out of Scope
- 不引入数据库/外部存储（PostgreSQL 等）
- 不做 Vercel 部署、CI/CD、Roadmap（后续 session 处理）
- 不做 UI（gradio）相关功能扩展
- 不改动非允许路径（尤其是 README/ARCH 等）除非与本次迁移强相关且在 allowlist 中声明

### Diff Budget
- 预期变更规模：☑ Medium（≤ 300 lines 净变更）
- 若超过预算：必须拆分为第二个 session，并先完成可测试的最小闭环

## 4. Assumptions
- Agno 提供 Agent/Team 或等价抽象，可表达多代理组合与工具挂载。
- Agno 可接入 Gemini 模型；本 session 使用 **Gemini Flash** 作为默认模型以降低成本。
- 本地/CI 可通过环境变量提供 Gemini API Key（不提交任何密钥到仓库）。
- 测试阶段允许使用 mock/fake 来避免真实模型调用（优先保证 determinism）。

## 5. Execution Summary (Planned)
1) 引入 Agno 依赖，并保证 `uv sync` 可复现（锁文件更新由 uv 生成）。  
2) 用 Agno 实现与下述 ADK 结构“语义对齐”的骨架：
   - Guard：域外拒绝（exact string）+ 预测请求记录（tool call）+ 有效请求进入 Planner
   - Planner：生成 plan JSON + 询问批准
   - Root/Orchestrator：先 Guard，再 Planner；批准后才进入 Coder（门控）
   - Coder：输出 GEE JavaScript + 成本估计（本 session 只保留最小输出结构即可）
3) 新增/调整测试，至少覆盖：
   - 域外输入 → exact out-of-scope message
   - predictive 输入 → tool 被调用 + exact capability message
   - 未批准 → 不得触发 coder
4) 确保测试不依赖真实模型调用（如需，可将 LLM 调用封装并在测试中替换）。

## 6. Verification & Evidence (Required)
必须提供以下命令与结果（粘贴关键输出片段）：

- Dependency / env:
  - `uv sync`
  - `uv run python -c "import agno; print('agno ok')"`
- Tests:
  - `uv run pytest -q`
  - （如引入 lint/format）`uv run ruff check .`（可选）
- Evidence (paste here):
  - `uv sync` → venv created, installed agno==2.3.13, pytest==9.0.2 (warning: tool.uv.dev-dependencies deprecated)
  - `uv run python -c "import agno; print('agno ok')"` → agno ok
  - `uv run pytest -q` → 3 passed

## 7. Risks & Follow-ups
- 风险：Agno 的 Gemini 连接方式与运行环境可能导致本地真实调用不稳定；本 session 通过 mock 确保测试确定性，真实调用在后续 session 集成测试验证。
- 风险：Planner 的 JSON 输出解析是常见不稳定点；本 session 只定义最小解析策略与测试样例，后续增强。
- Follow-ups:
  - Session 2：FastAPI/Vercel 部署骨架 + smoke test
  - Session 3：CI（GitHub Actions）+ PR template 强制 session 链接 + coverage gate
  - Session 4：回归测试集（tests/test_set.json）规范化与黄金结果（golden）机制

## 8. Outcome
- ☐ Completed as intended
- ☐ Partially completed
- ☐ Blocked

Blocked / Notes (if any):
- google-adk 测试运行器已移除，改为 Agno agent/team 骨架与 Python 显式门控；依赖只保留 agno[google]。
