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
import os
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from my_agent.agents.coordinator_agent import personal_curator
from pathlib import Path
# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

# FastAPI app
app = FastAPI(
    title="MyYear.AI API",
    description="Personalized viewing analytics powered by multi-agent AI",
    version="1.0.0"
)


# Session service for stateful conversations
session_service = InMemorySessionService()

# Runner for executing agents (same pattern as interactive.py)
runner = InMemoryRunner(agent=personal_curator, app_name="agents")

# Fixed CSV path - using the data file in the data directory
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "my_viewing_history.csv")

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

# Generate wrapped endpoint
@app.post("/wrapped")
async def generate_wrapped(request: WrappedRequest):
    """
    Generate personalized viewing wrapped.
    
    Uses the viewing history CSV file from the data directory.
    """
    try:
        # Check if CSV file exists
        if not os.path.exists(CSV_PATH):
            raise HTTPException(
                status_code=404,
                detail=f"Viewing data file not found at {CSV_PATH}"
            )
        
        # Generate wrapped
        prompt = f"""
        Create my personalized viewing wrapped from: {CSV_PATH}
        
        Include:
        1. Viewing patterns and personality
        2. Narrative story of my year
        3. Evolution analysis
        4. Shareable social posts
        
        Make it engaging! 🎉
        """
        
        session_id = f"wrapped_{request.user_id}"
        
        # Create session if it doesn't exist (same pattern as interactive.py)
        session = await runner.session_service.get_session(
            app_name=runner.app_name,
            user_id=request.user_id,
            session_id=session_id
        )
        if not session:
            session = await runner.session_service.create_session(
                app_name=runner.app_name,
                user_id=request.user_id,
                session_id=session_id
            )
        
        # Collect full response using runner (same pattern as interactive.py)
        full_response = ""
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session_id,
            new_message=types.UserContent(parts=[types.Part(text=prompt)])
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        full_response += part.text
        
        return {
            "success": True,
            "wrapped": full_response,
            "user_id": request.user_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wrapped generation failed: {str(e)}")

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
            
            # Create session if it doesn't exist (same pattern as interactive.py)
            session = await runner.session_service.get_session(
                app_name=runner.app_name,
                user_id=request.user_id,
                session_id=full_session_id
            )
            is_new_session = not session
            if not session:
                session = await runner.session_service.create_session(
                    app_name=runner.app_name,
                    user_id=request.user_id,
                    session_id=full_session_id
                )
            
            # If this is a new session, initialize with CSV path context
            if is_new_session:
                message_with_context = f"""
                CRITICAL: Use this exact file path immediately: {CSV_PATH}

                DO NOT ask the user to confirm the path. DO NOT ask for the file path. 
                The path is correct and ready to use. Load the data immediately using the read_viewing_data tool with this path.

                Then answer the user's question: {request.message}

                Start by calling read_viewing_data with the path above, then proceed with the analysis.
                """
            else:
                message_with_context = request.message
            
            
            event_count = 0
            has_yielded = False
            function_calls_detected = False
            
            async for event in runner.run_async(
                user_id=request.user_id,
                session_id=full_session_id,
                new_message=types.UserContent(parts=[types.Part(text=message_with_context)])
            ):
                event_count += 1
                
                # Yield status update on first event
                if event_count == 1:
                    yield f"data: [STATUS] Processing request...\n\n"
                
                # Check for function calls
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        # Check for function calls
                        if hasattr(part, 'function_call'):
                            function_calls_detected = True
                            func_name = getattr(part.function_call, 'name', 'unknown')
                            yield f"data: [STATUS] Calling function: {func_name}\n\n"
                        
                        # Check for text (both partial and complete)
                        if hasattr(part, 'text') and part.text:
                            yield f"data: {part.text}\n\n"
                            has_yielded = True
                
                # Also check for direct text attribute on event
                if hasattr(event, 'text') and event.text:
                    yield f"data: {event.text}\n\n"
                    has_yielded = True
                
                # Check for partial events (streaming text)
                if hasattr(event, 'partial') and not event.partial:
                    # This is a complete event, might have final response
                    pass
            
            # If function calls were detected but no text response, the agent might be waiting
            if function_calls_detected and not has_yielded:
                yield f"data: [STATUS] Function calls completed ({event_count} events processed). The agent may be generating a response...\n\n"
                yield f"data: [INFO] If no response appears, the agent may need explicit instructions to respond after function calls.\n\n"
            elif not has_yielded:
                yield f"data: [ERROR] No text response received after {event_count} events.\n\n"
            
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
            "/wrapped": "Generate personalized wrapped (uses data/my_viewing_history.csv)",
            "/chat/stream": "Streaming chat (SSE, uses data/my_viewing_history.csv)"
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


