from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from src.database import new_session
from src.chat import MessageOrm, conn_manager


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/last_messages")
async def get_last_messages(message_limit: int = 10):
    async with new_session() as session:
        query = select(MessageOrm).order_by(MessageOrm.id.desc()).limit(message_limit)
        result = await session.execute(query)
        messages = list(result.all())
        messages.reverse()
        messages_list = [msg[0].as_dict() for msg in messages]
        return messages_list


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await conn_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data:
                await conn_manager.send_personal_message(f"You wrote: {data}", websocket)
                await conn_manager.broadcast(f"Client #{client_id} says: {data}", exclude_conn=[websocket])
                await conn_manager.add_message_to_db(message=data)
    except WebSocketDisconnect:
        conn_manager.disconnect(websocket)
        await conn_manager.broadcast(f"Client #{client_id} left the chat")
