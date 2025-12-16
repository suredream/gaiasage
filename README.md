


uv run python - <<'PY'
from gaiasage.agent import orchestrate_user_message
msg = "conduct Deforestation Analysis in Borneo."
resp, state = orchestrate_user_message(msg, deterministic=True)
print("response:", resp)
print("state:", state)
PY


uv run python - <<'PY'
from gaiasage.agent import orchestrate_user_message

msg = "Compute NDVI time series for the Amazon rainforest from 2020 to 2023."
resp, state = orchestrate_user_message(msg, deterministic=False)
print(resp)
print(state)
PY
