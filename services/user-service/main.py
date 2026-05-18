from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="user-service")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "user-service"}

app.include_router(router)