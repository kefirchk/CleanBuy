import json
from typing import List, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select, func

from src.chat import Message
from src.chat import ChatParticipantsOrm, ChatOrm, generate_chat_id
from src.database import new_session
from src.chat import MessageOrm, conn_manager
from src.users_crud.models import UserOrm


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/id")
async def get_chat_id(user1_id: int, user2_id: int) -> Dict[str, int]:
    async with new_session() as session:
        query = select(ChatParticipantsOrm.chat_id).filter(
            ChatParticipantsOrm.user_id.in_([user1_id, user2_id])
        ).group_by(ChatParticipantsOrm.chat_id).having(
            func.count(ChatParticipantsOrm.chat_id) == 2
        )

        result = await session.execute(query)
        chat_id = result.scalar_one_or_none()

        if chat_id is None:
            # Create a new chat
            chat = ChatOrm(chat_type="PERSONAL")
            session.add(chat)
            await session.commit()

            # Add participants
            session.add(ChatParticipantsOrm(chat_id=chat.id, user_id=user1_id))
            session.add(ChatParticipantsOrm(chat_id=chat.id, user_id=user2_id))
            await session.commit()

            chat_id = chat.id

        print("RETURN CHAT_ID:", chat_id)
        return {"chat_id": chat_id}


@router.get("/last_messages/{chat_id}")
async def get_last_messages(chat_id: int, message_limit: int = 10) -> List:
    async with new_session() as session:
        query = (
            select(
                MessageOrm.message,
                MessageOrm.timestamp,
                MessageOrm.sender_id,
                UserOrm.username  # Здесь добавляем username
            )
            .join(UserOrm, MessageOrm.sender_id == UserOrm.id)  # Объединяем таблицы по sender_id
            .where(MessageOrm.chat_id == chat_id)  # Фильтруем по chat_id
            .order_by(MessageOrm.id.desc())
            .limit(message_limit)
        )
        result = await session.execute(query)
        messages = result.fetchall()
        messages.reverse()

        # Преобразуем в список словарей с нужной структурой
        messages_list = [
            {
                "message": msg.message,
                "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "sender_id": msg.sender_id,
                "username": msg.username,  # Включаем username в результат
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
            print("--------> RECEIVE MESSAGE:", data)

            # Parse message
            try:
                message_data = json.loads(data)
                chat_id = message_data.get('chat_id')
                sender_id = message_data.get('sender_id')
                content = message_data.get('message')
                username = message_data.get('username')
                timestamp = message_data.get('timestamp')

                if chat_id is None or sender_id is None or content is None:
                    continue

                # Save message to database
                async with new_session() as session:
                    new_message = MessageOrm(
                        message=content,
                        sender_id=sender_id,
                        chat_id=chat_id
                    )
                    session.add(new_message)
                    await session.commit()

                await conn_manager.broadcast(
                    json.dumps({
                        "chat_id": chat_id,
                        "sender_id": sender_id,
                        "message": content,
                        "username": username,
                        "timestamp": timestamp
                    }),
                    exclude_conn=[websocket]
                )

            except json.JSONDecodeError:
                continue

    except WebSocketDisconnect:
        conn_manager.disconnect(websocket)
        print(f"Client #{client_id} left the chat")
