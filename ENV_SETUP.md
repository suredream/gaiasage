# Environment Variables Setup

## Required Environment Variables

### For Vercel Deployment

1. **GOOGLE_API_KEY**: Your Google Gemini API key
   - Get your API key from: https://makersuite.google.com/app/apikey
   - Set this in Vercel dashboard: Settings → Environment Variables

### Optional Environment Variables

- **DETERMINISTIC**: Set to "true" for deterministic mode (uses heuristics instead of LLM)
  - Default: "false"

## Local Development

### Option 1: Using .env file (Recommended)

Create a `.env` file in the root directory (same level as `pyproject.toml`):

```
GOOGLE_API_KEY=your_google_api_key_here
DETERMINISTIC=false
```

The API will automatically load environment variables from this file when you start the server.

**Note**: Make sure to add `.env` to your `.gitignore` file to avoid committing your API key!

### Option 2: Using environment variables directly

You can also set the environment variable directly in your terminal:

```bash
# macOS/Linux
export GOOGLE_API_KEY=your_google_api_key_here

# Then start the server
uvicorn api.main:app --reload --port 8000
```

Or set it inline with the command:

```bash
GOOGLE_API_KEY=your_google_api_key_here uvicorn api.main:app --reload --port 8000
```

## Vercel Configuration

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add the following variables:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - (Optional) `DETERMINISTIC`: "false" for production

