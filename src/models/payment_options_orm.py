# from typing import List
#
# from sqlalchemy import Integer, Enum as SQLAlchemyEnum
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.models import Base, BuyerInformationOrm
# from src.schemas.custom_types import PaymentOptionType


# class PaymentOptionsOrm(Base):
#     __tablename__ = 'payment_options'
#
#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True
#     )
#     payment_option: Mapped[PaymentOptionType] = mapped_column(
#         SQLAlchemyEnum(PaymentOptionType),
#         nullable=False
#     )
#
#     # Relationships:
#     buyer_information: Mapped[List[BuyerInformationOrm]] = relationship(
#         "BuyerInformationOrm",
#         back_populates="payment_options",
#         secondary="buyer_information_payment_options",
#         lazy="selectin"
#     )
