# Environment Variables Setup

## Required Environment Variables

### For Vercel Deployment

1. **OPENAI_API_KEY**: Your DeepSeek API key (using OpenAI-compatible API)
   - Get your API key from: https://platform.deepseek.com/
   - Set this in Vercel dashboard: Settings → Environment Variables
   - **Note**: Even though it's called OPENAI_API_KEY, this is for DeepSeek API

### Optional Environment Variables

- **DETERMINISTIC**: Set to "true" for deterministic mode (uses heuristics instead of LLM)
  - Default: "false"

## Local Development

### Option 1: Using .env file (Recommended)

Create a `.env` file in the root directory (same level as `pyproject.toml`):

```
OPENAI_API_KEY=your_deepseek_api_key_here
DETERMINISTIC=false
```

The API will automatically load environment variables from this file when you start the server.

**Note**: Make sure to add `.env` to your `.gitignore` file to avoid committing your API key!

### Option 2: Using environment variables directly

You can also set the environment variable directly in your terminal:

```bash
# macOS/Linux
export OPENAI_API_KEY=your_deepseek_api_key_here

# Then start the server
uvicorn api.main:app --reload --port 8000
```

Or set it inline with the command:

```bash
OPENAI_API_KEY=your_deepseek_api_key_here uvicorn api.main:app --reload --port 8000
```

## Vercel Configuration

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add the following variables:
   - `OPENAI_API_KEY`: Your DeepSeek API key (get from https://platform.deepseek.com/)
   - (Optional) `DETERMINISTIC`: "false" for production

## Getting Your DeepSeek API Key

1. Visit https://platform.deepseek.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your environment variables

## Model Information

- **Model**: deepseek-chat
- **Provider**: DeepSeek (OpenAI-compatible API)
- **Base URL**: https://api.deepseek.com/v1
- **Free Tier**: Available with generous limits

