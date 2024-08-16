from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.chat import ChatType
from src.database import Base


class MessageOrm(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    message: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    timestamp: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
    sender_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    chat_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ChatOrm(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    chat_type: Mapped[ChatType] = mapped_column(
        SQLAlchemyEnum(ChatType),
        nullable=False
    )


class ChatParticipantsOrm(Base):
    __tablename__ = "chats_users"

    chat_id: Mapped[int] = mapped_column(
        ForeignKey('chats.id', ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
