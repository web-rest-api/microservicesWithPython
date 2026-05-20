from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="activity-service")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "activity-service"}

app.include_router(router)