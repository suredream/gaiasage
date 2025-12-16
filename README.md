# GaiaSage

GaiaSage is an AI co-pilot for geospatial analysis powered by Agno multi-agent framework.

## Features

- **Web Interface**: Chat-based interface for geospatial analysis tasks
- **Multi-Agent System**: Guard, Planner, and Coder agents working together
- **Geospatial Focus**: Specialized for geospatial analysis tasks only

## Quick Start

### Web Interface (Recommended)

1. **Deploy to Vercel**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
2. **Set Environment Variables**: Configure `OPENAI_API_KEY` (DeepSeek API key) in Vercel dashboard
3. **Access**: Open your Vercel deployment URL in a browser

### Local Development

#### Running the Web Interface

**First, set up your environment variables:**

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_deepseek_api_key_here
```

Or set it directly:
```bash
export OPENAI_API_KEY=your_deepseek_api_key_here
```

**Get your DeepSeek API key**: https://platform.deepseek.com/

**Important**: Make sure you're using a **DeepSeek API key**, not an OpenAI key. DeepSeek keys start with `sk-` (not `sk-proj-`). See [GET_DEEPSEEK_KEY.md](GET_DEEPSEEK_KEY.md) for detailed instructions.

**Then start the servers:**

```bash
# Terminal 1: Start the API
uvicorn api.main:app --reload --port 8000

# Terminal 2: Start the frontend
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000 in your browser.

#### Command Line Usage

```bash
uv run python - <<'PY'
from gaiasage.agent import orchestrate_user_message
msg = "conduct Deforestation Analysis in Borneo."
resp, state = orchestrate_user_message(msg, deterministic=True)
print("response:", resp)
print("state:", state)
PY
```

## Project Structure

- `src/gaiasage/`: Core agent implementation
- `api/`: FastAPI backend for web interface
- `frontend/`: React frontend application
- `vercel.json`: Vercel deployment configuration

## Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md): Deployment guide for Vercel
- [ENV_SETUP.md](ENV_SETUP.md): Environment variables configuration
- [AGENTS.md](AGENTS.md): Agent architecture and design
- [FREE_MODELS.md](FREE_MODELS.md): Free model API options for testing
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md): Troubleshooting common issues
