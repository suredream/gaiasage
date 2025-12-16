# GaiaSage

GaiaSage is an AI co-pilot for geospatial analysis powered by Agno multi-agent framework.

## Features

- **Web Interface**: Chat-based interface for geospatial analysis tasks
- **Multi-Agent System**: Guard, Planner, and Coder agents working together
- **Geospatial Focus**: Specialized for geospatial analysis tasks only

## Quick Start

### Web Interface (Recommended)

1. **Deploy to Vercel**: See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
2. **Set Environment Variables**: Configure `GOOGLE_API_KEY` in Vercel dashboard
3. **Access**: Open your Vercel deployment URL in a browser

### Local Development

#### Running the Web Interface

**First, set up your environment variables:**

Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_google_api_key_here
```

Or set it directly:
```bash
export GOOGLE_API_KEY=your_google_api_key_here
```

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
