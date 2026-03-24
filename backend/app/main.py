from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai, auth
from app.routers.environment_router import router as environment_router
from fastapi import Depends
from sqlalchemy.orm import Session
from app.services.database import get_db

app = FastAPI(
    title="PrithviNet AI Backend",
    description="Minimal FastAPI backend for environmental assistant powered by Ollama Phi-3",
    version="1.0.0"
)

app.include_router(environment_router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(environment_router, prefix="/api/environment", tags=["Environment"])

# Include Routers
app.include_router(ai.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "PrithviNet AI API is running. Visit /docs for documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

app.include_router(environment_router)

@app.get("/db-test")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Supabase database connected successfully"}
