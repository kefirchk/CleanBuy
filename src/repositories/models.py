from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, Enum as SQLAlchemyEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from src.schemas.buyer import ProductSegmentType

Base = declarative_base()


class LocationOrm(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)


class CommissionRateOrm(Base):
    __tablename__ = 'commission_rates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    min_rate: Mapped[float] = mapped_column(Float, nullable=False)
    max_rate: Mapped[float] = mapped_column(Float, nullable=False)


class PriceRangeOrm(Base):
    __tablename__ = 'price_ranges'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    min_price: Mapped[float] = mapped_column(Float, nullable=False)
    max_price: Mapped[float] = mapped_column(Float, nullable=False)


class DeliveryOptionsOrm(Base):
    __tablename__ = 'delivery_options'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    included: Mapped[bool] = mapped_column(Boolean, default=False)
    not_included: Mapped[bool] = mapped_column(Boolean, default=False)
    negotiable: Mapped[bool] = mapped_column(Boolean, default=False)


class PaymentOptionsOrm(Base):
    __tablename__ = 'payment_options'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cryptocurrency: Mapped[bool] = mapped_column(Boolean, default=False)
    card_payment: Mapped[bool] = mapped_column(Boolean, default=False)
    on_delivery: Mapped[bool] = mapped_column(Boolean, default=False)
    prepayment_100: Mapped[bool] = mapped_column(Boolean, default=False)


class BuyerOrm(Base):
    __tablename__ = 'buyers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    import_countries: Mapped[list[str]] = mapped_column(JSON)
    product_segment: Mapped[ProductSegmentType] = mapped_column(SQLAlchemyEnum(ProductSegmentType), nullable=False)
    prepayment_percentage: Mapped[float] = mapped_column(Float, nullable=False)

    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('locations.id'), nullable=False)
    commission_rate_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('commission_rates.id'), nullable=False)
    price_range_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('price_ranges.id'), nullable=False)
    delivery_options_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('delivery_options.id'), nullable=False)
    payment_options_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('payment_options.id'), nullable=False)

    # Relationships
    location: Mapped[LocationOrm] = relationship("LocationOrm", lazy="selectin")
    commission_rate: Mapped[CommissionRateOrm] = relationship("CommissionRateOrm", lazy="selectin")
    price_range: Mapped[PriceRangeOrm] = relationship("PriceRangeOrm", lazy="selectin")
    delivery_options: Mapped[DeliveryOptionsOrm] = relationship("DeliveryOptionsOrm", lazy="selectin")
    payment_options: Mapped[PaymentOptionsOrm] = relationship("PaymentOptionsOrm", lazy="selectin")
