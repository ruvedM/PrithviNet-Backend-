from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.ai import ChatRequest, ChatResponse, HealthResponse
from app.services.ollama_service import OllamaService, MODEL_NAME

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = await OllamaService.generate_response(request.message)
    if reply.startswith("Error:"):
        raise HTTPException(status_code=503, detail=reply)
    return ChatResponse(reply=reply)

@router.post("/stream")
async def stream_chat(request: ChatRequest):
    return StreamingResponse(
        OllamaService.stream_response(request.message),
        media_type="text/event-stream"
    )

@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", model=MODEL_NAME)
