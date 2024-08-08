# from sqlalchemy import Integer
# from sqlalchemy.orm import Mapped, mapped_column
# from sqlalchemy import Enum as SQLAlchemyEnum
# from src.models import Base
# from src.schemas.custom_types import DeliveryOptionType
#
#
# class DeliveryOptionsOrm(Base):
#     __tablename__ = 'delivery_options'
#
#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True
#     )
#     delivery_option: Mapped[DeliveryOptionType] = mapped_column(
#         SQLAlchemyEnum(DeliveryOptionType),
#         nullable=False
#     )
