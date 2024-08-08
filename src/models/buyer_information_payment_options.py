from typing import List

from sqlalchemy import ForeignKey, Float, Enum as SQLAlchemyEnum, JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base, PriceRangeOrm, CommissionRateOrm, LocationOrm
from src.schemas.custom_types import ProductSegmentType, PaymentOptionType, DeliveryOptionType


class PaymentOptionsOrm(Base):
    __tablename__ = 'payment_options'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    payment_option: Mapped[PaymentOptionType] = mapped_column(
        SQLAlchemyEnum(PaymentOptionType),
        nullable=False
    )

    # Relationships:
    buyer_information: Mapped[List["BuyerInformationOrm"]] = relationship(
        "BuyerInformationOrm",
        back_populates="payment_options",
        secondary="buyer_information_payment_options",
        lazy="selectin",
        cascade="all, delete"
    )


class BuyerInformationOrm(Base):
    __tablename__ = 'buyer_information'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    import_countries: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False
    )
    product_segment: Mapped[ProductSegmentType] = mapped_column(
        SQLAlchemyEnum(ProductSegmentType),
        nullable=False
    )
    prepayment_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    delivery_options: Mapped[DeliveryOptionType] = mapped_column(
        SQLAlchemyEnum(DeliveryOptionType),
        nullable=False
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey('locations.id', ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    commission_rate_id: Mapped[int] = mapped_column(
        ForeignKey('commission_rates.id', ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    price_range_id: Mapped[int] = mapped_column(
        ForeignKey('price_ranges.id', ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    # delivery_options_id: Mapped[int] = mapped_column(
    #     ForeignKey('delivery_options.id', ondelete="CASCADE", onupdate="CASCADE"),
    #     nullable=False
    # )

    # Relationships
    location: Mapped[LocationOrm] = relationship(
        "LocationOrm",
        lazy="joined",
        cascade="all, delete"
    )
    commission_rate: Mapped[CommissionRateOrm] = relationship(
        "CommissionRateOrm",
        lazy="joined",
        cascade="all, delete"
    )
    price_range: Mapped[PriceRangeOrm] = relationship(
        "PriceRangeOrm",
        lazy="joined",
        cascade="all, delete"
    )
    # delivery_options: Mapped[DeliveryOptionsOrm] = relationship(
    #     "DeliveryOptionsOrm",
    #     lazy="joined"
    # )
    payment_options: Mapped[List["PaymentOptionsOrm"]] = relationship(
        "PaymentOptionsOrm",
        back_populates="buyer_information",
        secondary="buyer_information_payment_options",
        lazy="selectin",
        cascade="all, delete"
    )


class BuyerInformation_PaymentOptionsOrm(Base):
    __tablename__ = 'buyer_information_payment_options'

    buyer_information_id: Mapped[int] = mapped_column(
        ForeignKey('buyer_information.id', ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    payment_option_id: Mapped[int] = mapped_column(
        ForeignKey('payment_options.id', ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
