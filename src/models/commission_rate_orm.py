from sqlalchemy import Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class CommissionRateOrm(Base):
    __tablename__ = 'commission_rates'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    min_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    max_rate: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
