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

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_google_api_key_here
DETERMINISTIC=false
```

## Vercel Configuration

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add the following variables:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - (Optional) `DETERMINISTIC`: "false" for production

