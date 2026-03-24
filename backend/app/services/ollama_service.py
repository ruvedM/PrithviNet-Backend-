import httpx
import json
import logging
from typing import AsyncGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "phi3"
# Enforced conciseness in system prompt
SYSTEM_PROMPT = (
    "You are an environmental monitoring assistant. "
    "Provide concise, precise answers limited to 3-4 sentences max. "
    "Avoid long explanations and excessive formatting."
)

class OllamaService:
    @staticmethod
    async def generate_response(message: str) -> str:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": MODEL_NAME,
            "prompt": f"System: {SYSTEM_PROMPT}\nUser: {message}\nAssistant:",
            "stream": False,
            "options": {
                "num_predict": 120,  # Limit max tokens
                "temperature": 0.2   # Lower temperature for precision
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                reply = data.get("response", "").strip()
                # Remove excessive newlines
                return " ".join(reply.splitlines())
            except httpx.ConnectError:
                logger.error("Could not connect to Ollama server.")
                return "Error: Could not connect to Ollama. Is it running?"
            except Exception as e:
                logger.error(f"Error calling Ollama: {str(e)}")
                return f"Error: {str(e)}"

    @staticmethod
    async def stream_response(message: str) -> AsyncGenerator[str, None]:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": MODEL_NAME,
            "prompt": f"System: {SYSTEM_PROMPT}\nUser: {message}\nAssistant:",
            "stream": True,
            "options": {
                "num_predict": 120,
                "temperature": 0.2
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                async with client.stream("POST", url, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        if chunk:
                            yield f"data: {json.dumps({'text': chunk})}\n\n"
                        if data.get("done"):
                            break
            except httpx.ConnectError:
                yield f"data: {json.dumps({'error': 'Ollama connection error'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
