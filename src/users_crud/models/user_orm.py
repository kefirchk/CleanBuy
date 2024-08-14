from pydantic import EmailStr
from sqlalchemy import Integer, String, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.users_crud.models import BuyerInformationOrm
from src.users_crud.schemas.custom_types import RoleType


class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    role: Mapped[RoleType] = mapped_column(
        SQLAlchemyEnum(RoleType),
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False
    )
    email: Mapped[EmailStr] = mapped_column(
        String(length=320),
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024),
        nullable=False
    )
    buyer_information_id: Mapped[int] = mapped_column(
        ForeignKey("buyer_information.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True
    )

    # Relationships:
    buyer_information: Mapped[BuyerInformationOrm] = relationship(
        "BuyerInformationOrm",
        lazy="joined",
        cascade="all, delete"
    )
