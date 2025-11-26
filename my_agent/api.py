"""
FastAPI Server for MyYear.AI
KEY CONCEPT: Agent deployment via REST API
Enables cloud deployment to Cloud Run or similar platforms
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import asyncio
import tempfile
import os
from google.adk.sessions import InMemorySessionService
from my_agent.agents.coordinator_agent import personal_curator


# FastAPI app
app = FastAPI(
    title="MyYear.AI API",
    description="Personalized viewing analytics powered by multi-agent AI",
    version="1.0.0"
)


# Session service for stateful conversations
session_service = InMemorySessionService()


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    user_id: Optional[str] = "user_001"


class ChatResponse(BaseModel):
    response: str
    session_id: str


class WrappedRequest(BaseModel):
    user_id: Optional[str] = "user_001"


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy", "service": "MyYear.AI"}


# Upload CSV endpoint
@app.post("/upload")
async def upload_viewing_data(file: UploadFile = File(...), user_id: str = "user_001"):
    """
    Upload viewing history CSV file.
    
    The file will be stored temporarily for processing.
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Store path in session (in production, use cloud storage)
        session_service.set_state(
            user_id=user_id,
            session_id=f"data_{user_id}",
            state={"csv_path": tmp_path}
        )
        
        return {
            "success": True,
            "message": "File uploaded successfully",
            "filename": file.filename,
            "user_id": user_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# Generate wrapped endpoint
@app.post("/wrapped")
async def generate_wrapped(request: WrappedRequest):
    """
    Generate personalized viewing wrapped.
    
    Requires viewing data to be uploaded first via /upload endpoint.
    """
    try:
        # Get CSV path from session
        state = session_service.get_state(
            user_id=request.user_id,
            session_id=f"data_{request.user_id}"
        )
        
        if not state or "csv_path" not in state:
            raise HTTPException(
                status_code=400,
                detail="No viewing data found. Please upload CSV file first via /upload"
            )
        
        csv_path = state["csv_path"]
        
        # Generate wrapped
        prompt = f"""
        Create my personalized viewing wrapped from: {csv_path}
        
        Include:
        1. Viewing patterns and personality
        2. Narrative story of my year
        3. Evolution analysis
        4. Shareable social posts
        
        Make it engaging! 🎉
        """
        
        session_id = f"wrapped_{request.user_id}"
        
        # Collect full response
        full_response = ""
        async for chunk in personal_curator.send_message_stream(
            prompt,
            session_id=session_id,
            session_service=session_service
        ):
            full_response += chunk
        
        return {
            "success": True,
            "wrapped": full_response,
            "user_id": request.user_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wrapped generation failed: {str(e)}")


# Chat endpoint (for interactive conversations)
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Interactive chat endpoint.
    
    Maintains conversation history via session management.
    """
    try:
        # Get full session ID
        full_session_id = f"chat_{request.user_id}_{request.session_id}"
        
        # Send message to agent
        full_response = ""
        async for chunk in personal_curator.send_message_stream(
            request.message,
            session_id=full_session_id,
            session_service=session_service
        ):
            full_response += chunk
        
        return ChatResponse(
            response=full_response,
            session_id=request.session_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


# Streaming chat endpoint
@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint for real-time responses.
    
    Returns Server-Sent Events (SSE) stream.
    """
    async def generate():
        try:
            full_session_id = f"chat_{request.user_id}_{request.session_id}"
            
            async for chunk in personal_curator.send_message_stream(
                request.message,
                session_id=full_session_id,
                session_service=session_service
            ):
                # SSE format
                yield f"data: {chunk}\n\n"
            
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


# Root endpoint
@app.get("/")
async def root():
    """API information"""
    return {
        "service": "MyYear.AI",
        "description": "Personalized viewing analytics powered by multi-agent AI",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/upload": "Upload viewing history CSV",
            "/wrapped": "Generate personalized wrapped",
            "/chat": "Interactive chat",
            "/chat/stream": "Streaming chat (SSE)"
        },
        "key_concepts": [
            "Multi-agent system",
            "Custom tools",
            "Session management",
            "Cloud deployment"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    # For local development
    uvicorn.run(
        "my_agent.api:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        reload=True
    )


