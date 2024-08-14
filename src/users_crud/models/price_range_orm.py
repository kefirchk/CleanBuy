from sqlalchemy import Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class PriceRangeOrm(Base):
    __tablename__ = 'price_ranges'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    min_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    max_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
