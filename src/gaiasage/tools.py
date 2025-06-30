import os
from datetime import datetime

def log_out_of_scope_question(question: str) -> str:
    """
    Logs a user's question that is valid but outside the agent's current
    capabilities (e.g., predictive analysis).

    Args:
        question: The user's question to log.

    Returns:
        A confirmation message that the question has been logged.
    """
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, 'unsupported_requests.log')
    timestamp = datetime.now().isoformat()

    with open(log_file_path, 'a') as f:
        f.write(f"{timestamp}: {question}\n")

    return "Confirmation: The unsupported request has been logged for future review."
