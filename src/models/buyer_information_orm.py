# from typing import List
#
# from sqlalchemy import Integer, JSON, Enum as SQLAlchemyEnum, Float, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.models import Base
# from src.models.commission_rate_orm import CommissionRateOrm
# from src.models.delivery_options_orm import DeliveryOptionsOrm
# from src.models.location_orm import LocationOrm
# from src.models.payment_options_orm import PaymentOptionsOrm
# from src.models.price_range_orm import PriceRangeOrm
# from src.schemas.custom_types import ProductSegmentType


# class BuyerInformationOrm(Base):
#     __tablename__ = 'buyer_information'
#
#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True
#     )
#     import_countries: Mapped[list[str]] = mapped_column(
#         JSON,
#         nullable=False
#     )
#     product_segment: Mapped[ProductSegmentType] = mapped_column(
#         SQLAlchemyEnum(ProductSegmentType),
#         nullable=False
#     )
#     prepayment_percentage: Mapped[float] = mapped_column(
#         Float,
#         nullable=False
#     )
#     location_id: Mapped[int] = mapped_column(
#         ForeignKey('locations.id', ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False
#     )
#     commission_rate_id: Mapped[int] = mapped_column(
#         ForeignKey('commission_rates.id', ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False
#     )
#     price_range_id: Mapped[int] = mapped_column(
#         ForeignKey('price_ranges.id', ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False
#     )
#     delivery_options_id: Mapped[int] = mapped_column(
#         ForeignKey('delivery_options.id', ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False
#     )
#     payment_options_id: Mapped[int] = mapped_column(
#         ForeignKey('payment_options.id', ondelete="CASCADE", onupdate="CASCADE"),
#         nullable=False
#     )
#
#     # Relationships
#     location: Mapped[LocationOrm] = relationship(
#         "LocationOrm",
#         lazy="joined"
#     )
#     commission_rate: Mapped[CommissionRateOrm] = relationship(
#         "CommissionRateOrm",
#         lazy="joined"
#     )
#     price_range: Mapped[PriceRangeOrm] = relationship(
#         "PriceRangeOrm",
#         lazy="joined"
#     )
#     delivery_options: Mapped[DeliveryOptionsOrm] = relationship(
#         "DeliveryOptionsOrm",
#         lazy="joined"
#     )
#     payment_options: Mapped[List[PaymentOptionsOrm]] = relationship(
#         "PaymentOptionsOrm",
#         back_populates="buyer_information",
#         secondary="buyer_information_payment_options",
#         lazy="selectin"
#     )
