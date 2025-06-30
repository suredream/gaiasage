---
created_by: augment
reviewed: true
last_updated: 2025-06-30
---


# Development workflow

1. Review requirement documents ([`docs/arch.md`](docs/arch.md:1), [`docs/userstory.md`](docs/userstory.md:1), feature specifications in [`docs/features/`](docs/features/)) to identify any new requirements.
    - Purpose: Ensure a clear understanding of what needs to be built or modified.
    - Inputs: User stories, feature specifications, and other relevant documents.
    - Outputs: A consolidated list of actionable requirements.

2. Create a detailed execution plan for the identified requirements. This plan should be stored in the [`plans/`](plans/) folder, outlining the tasks, approach, and any potential challenges.
    - Purpose: To strategize the implementation and break down work into manageable steps.
    - Contents: Task breakdown, estimated effort, dependencies, acceptance criteria.
    - Location: New file or update to existing plan in the `plans/` directory.

3. Implement the plan. This involves developing the necessary code, configurations, or other artifacts. The AI assistant carries out these tasks.
    - Purpose: To build the feature or make the changes as per the plan.
    - Activities: Coding, scripting, configuration, unit testing.
    - Tools: IDEs, version control (e.g., Git), AI coding assistants.

4. Upon successful implementation and verification (e.g., through tests in [`tests/test_set.json`](tests/test_set.json:1)), update the status of the corresponding plan and features to 'done'.
    - Purpose: To track progress and confirm completion of work.
    - Verification: May include automated tests, manual testing, peer reviews.
    - Status Update: Modify plan documents, commit messages, or task management systems.

5. Check if any further requirements have emerged or remain unaddressed. If so, iterate back to Step 1. Otherwise, the current development cycle is complete.
    - Purpose: To ensure all requirements are eventually addressed and to manage the iterative nature of development.
    - Trigger for new cycle: New user feedback, discovery of missed requirements, planned iterations.
