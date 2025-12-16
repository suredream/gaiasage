# Deployment Guide for Vercel

This guide explains how to deploy GaiaSage to Vercel.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. A GitHub account (for connecting your repository)
3. A Google Gemini API key (get it from https://makersuite.google.com/app/apikey)

## Deployment Steps

### 1. Prepare Your Repository

Ensure your code is pushed to a GitHub repository.

### 2. Connect to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect the project structure

### 3. Configure Environment Variables

In the Vercel project settings:

1. Go to **Settings** → **Environment Variables**
2. Add the following variable:
   - **Name**: `GOOGLE_API_KEY`
   - **Value**: Your Google Gemini API key
   - **Environment**: Production, Preview, Development (select all)

### 4. Configure Build Settings

Vercel should auto-detect the configuration from `vercel.json`, but verify:

- **Framework Preset**: Other
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: (leave empty, handled by build command)

### 5. Deploy

Click "Deploy" and wait for the build to complete.

## Project Structure

The deployment uses:

- **Frontend**: React app built with Vite, served as static files
- **Backend**: FastAPI app running as Python serverless functions via Mangum
- **API Routes**: `/api/*` routes are handled by Python functions
- **Static Routes**: All other routes serve the React app

## Local Development

### Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on http://localhost:3000

### Running the API

```bash
uvicorn api.main:app --reload --port 8000
```

The API will run on http://localhost:8000

### Running Both Together

In separate terminals:

```bash
# Terminal 1: Frontend
cd frontend && npm run dev

# Terminal 2: API
uvicorn api.main:app --reload --port 8000
```

## Troubleshooting

### API Not Working

- Check that `GOOGLE_API_KEY` is set in Vercel environment variables
- Verify the API route is accessible at `/api/chat`
- Check Vercel function logs for errors

### Frontend Not Loading

- Verify the build output directory is `frontend/dist`
- Check that `vercel.json` routes are correctly configured
- Ensure static files are being served correctly

### CORS Issues

- The API is configured to allow all origins in development
- For production, update `api/main.py` to restrict CORS to your domain

## Notes

- The Python runtime on Vercel is Python 3.9
- Cold starts may occur for the first request after inactivity
- API responses may take time due to LLM processing

