from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base


class LocationOrm(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    country: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    city: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
