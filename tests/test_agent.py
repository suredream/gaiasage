import asyncio
import json

from google.adk import Runner
from google.adk.sessions import InMemorySessionService

from src.gaiasage import root_agent


async def run_test(test_case):
    """Runs a single test case against the agent."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent, session_service=session_service, app_name="GaiaSage_test_app"
    )

    session = await session_service.create_session(
        app_name="GaiaSage_test_app",
        user_id=f"test_user_{test_case['id']}",
        session_id=f"test_session_{test_case['id']}",
    )

    print(f"--- Running Test: {test_case['id']} - {test_case['description']} ---")
    print(f"User Input: {test_case['user_input']}")

    response_generator = runner.run(
        user_id=session.user_id,
        session_id=session.id,
        new_message=test_case["user_input"],
    )

    final_response = ""
    for event in response_generator:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_response += part.text

    print(f"Agent Response: {final_response}")

    if "expected_response" in test_case:
        assert final_response == test_case["expected_response"]
        print("✅ Test Passed")
    elif "expected_response_contains" in test_case:
        for expected_text in test_case["expected_response_contains"]:
            assert expected_text in final_response
        print("✅ Test Passed")


async def main():
    """Loads test cases and runs them."""
    with open("tests/test_set.json", "r") as f:
        test_cases = json.load(f)

    # Filter for GuardAgent tests (F1 and F6)
    guard_test_ids = {"004", "005", "006", "010"}
    guard_tests = [tc for tc in test_cases if tc["id"] in guard_test_ids]

    for test_case in guard_tests:
        await run_test(test_case)
        print("-" * 50)


if __name__ == "__main__":
    asyncio.run(main())
