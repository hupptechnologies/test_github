from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from .database import AsyncSessionLocal
from .models import Message
from .services.ai_service import stream_chat_completion

async def save_message(db: AsyncSession, role: str, content: str):
    msg = Message(role=role, content=content)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async with AsyncSessionLocal() as db:
        try:
            while True:
                data = await websocket.receive_json()
                user_content = data.get('content')
                
                if not user_content:
                    await websocket.send_json({"error": "No content provided"})
                    continue
                
                # Persist user message
                await save_message(db, 'user', user_content)
                
                # Send user message confirmation
                await websocket.send_json({"role": "user", "content": user_content})
                
                # Stream AI response
                ai_content = ""
                await websocket.send_json({"role": "ai", "content": "", "loading": True})
                
                try:
                    async for delta in stream_chat_completion(user_content):
                        ai_content += delta
                        await websocket.send_json({"role": "ai", "content": ai_content, "loading": True})
                    
                    # Persist AI message
                    await save_message(db, 'ai', ai_content)
                    await websocket.send_json({"role": "ai", "content": ai_content, "loading": False})
                    
                except Exception as ai_error:
                    await websocket.send_json({"error": f"AI service error: {str(ai_error)}", "loading": False})
                    
        except WebSocketDisconnect:
            print("WebSocket disconnected")
        except Exception as e:
            await websocket.send_json({"error": f"WebSocket error: {str(e)}", "loading": False}) 