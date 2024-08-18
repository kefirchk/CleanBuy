from sqlalchemy import select, func

from src.chat.models import FileOrm
from src.database import new_session
from src.chat import ChatType, Message, MessageOrm, ChatOrm, ChatParticipantsOrm
from src.users_crud.models import UserOrm


class ChatRepo:
    @staticmethod
    async def create_chat(user1_id: int, user2_id: int, chat_type: ChatType):
        async with new_session() as session:
            chat = ChatOrm(chat_type=chat_type.value)
            session.add(chat)
            await session.commit()

            session.add(ChatParticipantsOrm(chat_id=chat.id, user_id=user1_id))
            session.add(ChatParticipantsOrm(chat_id=chat.id, user_id=user2_id))
            await session.commit()

    @staticmethod
    async def get_chat_id(user1_id: int, user2_id: int):
        async with new_session() as session:
            query = select(ChatParticipantsOrm.chat_id).filter(
                ChatParticipantsOrm.user_id.in_([user1_id, user2_id])
            ).group_by(ChatParticipantsOrm.chat_id).having(
                func.count(ChatParticipantsOrm.chat_id) == 2
            )

            result = await session.execute(query)
            chat_id = result.scalar_one_or_none()

            return chat_id

    @staticmethod
    async def get_messages(chat_id: int):
        async with new_session() as session:
            query = (
                select(
                    MessageOrm.message,
                    MessageOrm.timestamp,
                    MessageOrm.sender_id,
                    MessageOrm.file,
                    UserOrm.username,
                    FileOrm.file_url,
                    FileOrm.filename,
                    FileOrm.file_size,
                    FileOrm.file_type
                )
                .join(UserOrm, MessageOrm.sender_id == UserOrm.id)
                .outerjoin(FileOrm, MessageOrm.file_id == FileOrm.id)
                .where(MessageOrm.chat_id == chat_id)
                .order_by(MessageOrm.id.desc())
            )
            result = await session.execute(query)
            messages = result.fetchall()
            messages.reverse()

            return messages

    @staticmethod
    async def save_message(message: Message):
        async with new_session() as session:
            file_orm = FileOrm(**message.file.model_dump())
            new_message = MessageOrm(
                message=message.message,
                sender_id=message.sender_id,
                chat_id=message.chat_id,
                file=file_orm
            )
            session.add(new_message)
            await session.commit()
