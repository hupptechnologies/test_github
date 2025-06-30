from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router
from .ws import websocket_endpoint
from .database import init_db
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Chat Backend is running"}

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket_endpoint(websocket)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 