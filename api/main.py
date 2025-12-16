"""
FastAPI application for GaiaSage web interface.

Provides REST API endpoints for the chat interface.
"""

from __future__ import annotations

import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel

from gaiasage.agent import _normalize_output_text, root_agent

app = FastAPI(title="GaiaSage API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Process a chat message through the GaiaSage agent system.

    Args:
        message: The user's message and optional conversation ID

    Returns:
        The agent's response and conversation ID
    """
    try:
        # Call the root agent to process the message
        # Use deterministic=False to enable full LLM capabilities
        output = root_agent.run(message.message)
        response_text = _normalize_output_text(output)

        return ChatResponse(
            response=response_text,
            conversation_id=message.conversation_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

