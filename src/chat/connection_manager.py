from fastapi import WebSocket
from sqlalchemy import insert

from src.chat import MessageOrm
from src.database import new_session


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.connection = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @classmethod
    async def send_personal_message(cls, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, exclude_conn: list = None):
        if exclude_conn is None:
            exclude_conn = []
        for connection in self.active_connections:
            if connection not in exclude_conn:
                await connection.send_text(message)

    @staticmethod
    async def add_message_to_db(message: str):
        async with new_session() as session:
            stmt = insert(MessageOrm).values(
                message=message
            )
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()
