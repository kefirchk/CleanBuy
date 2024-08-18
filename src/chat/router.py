import json
from typing import List, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.chat.schemas import File
from src.chat import ChatType, Message, ChatRepo, conn_manager


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/id")
async def get_chat_id(user1_id: int, user2_id: int) -> Dict[str, int]:
    chat_id = await ChatRepo.get_chat_id(user1_id, user2_id)
    if chat_id is None:
        chat = await ChatRepo.create_chat(user1_id, user2_id, ChatType.PERSONAL)
        chat_id = chat.id

    return {"chat_id": chat_id}


@router.get("/last_messages/{chat_id}")
async def get_last_messages(chat_id: int) -> List:
    messages = await ChatRepo.get_messages(chat_id)
    messages_list = [
        {
            "message": msg.message,
            "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "sender_id": msg.sender_id,
            "username": msg.username,
            "file": {
                "file_url": msg.file_url,
                "filename": msg.filename,
                "file_size": msg.file_size,
                "file_type": msg.file_type
            } if msg.file_url else None
        }
        for msg in messages
    ]
    return messages_list


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await conn_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print("[INFO] Receive message:", data)
            try:
                data_dict: dict = json.loads(data)
                data_dict['file'] = File(**data_dict['file'])
                msg = Message(**data_dict)

                if msg.message is None and msg.file_url is None:
                    continue

                # if msg.file_url:
                #     # Если есть файл, то загружаем его на S3

                await ChatRepo.save_message(msg)
                await conn_manager.broadcast(data, exclude_conn=[websocket])

            except json.JSONDecodeError:
                continue

    except WebSocketDisconnect:
        conn_manager.disconnect(websocket)
        print(f"Client #{client_id} left the chat")
