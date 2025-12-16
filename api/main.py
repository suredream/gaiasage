"""
FastAPI application for GaiaSage web interface.

Provides REST API endpoints for the chat interface.
"""

from __future__ import annotations

import asyncio
import logging
import os
import traceback
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel

from gaiasage.agent import _normalize_output_text, root_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GaiaSage API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check environment variables on startup
def check_environment():
    """Check if required environment variables are set."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.warning("GOOGLE_API_KEY environment variable is not set. API calls will fail.")
    else:
        logger.info("GOOGLE_API_KEY is configured (length: %d)", len(api_key))
    return api_key is not None

# Check environment on module load
check_environment()

# Mangum handler for Vercel serverless
handler = Mangum(app)


class ChatMessage(BaseModel):
    """Request model for chat messages."""

    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat messages."""

    response: str
    conversation_id: Optional[str] = None


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "GaiaSage API"}


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Process a chat message through the GaiaSage agent system.

    Args:
        message: The user's message and optional conversation ID

    Returns:
        The agent's response and conversation ID
    """
    try:
        logger.info(f"Received chat message: {message.message[:100]}...")
        
        # Check environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("GOOGLE_API_KEY environment variable is not set")
            raise HTTPException(
                status_code=500,
                detail="GOOGLE_API_KEY environment variable is not configured. Please set it in Vercel environment variables."
            )
        
        # Call the root agent to process the message
        # Use deterministic=False to enable full LLM capabilities
        # Run in thread pool to avoid blocking the event loop
        logger.info("Calling root_agent.run()...")
        loop = asyncio.get_event_loop()
        output = await loop.run_in_executor(
            None,  # Use default executor
            root_agent.run,
            message.message
        )
        logger.info("root_agent.run() completed")
        
        response_text = _normalize_output_text(output)
        logger.info(f"Response generated: {len(response_text)} characters")

        return ChatResponse(
            response=response_text,
            conversation_id=message.conversation_id,
        )
    except HTTPException:
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error(f"Error processing message: {str(e)}\n{error_trace}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )


@app.get("/health")
async def health():
    """Health check endpoint."""
    api_key_configured = os.getenv("GOOGLE_API_KEY") is not None
    return {
        "status": "healthy",
        "api_key_configured": api_key_configured
    }

