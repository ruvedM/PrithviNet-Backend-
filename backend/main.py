
from fastapi import FastAPI
from app.routers.compliance_router import router as compliance_router

app = FastAPI()
app.include_router(compliance_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
