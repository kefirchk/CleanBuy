# from pydantic import BaseModel, Field
#
# from src.schemas.custom_types import DeliveryOptionType
#
#
# class DeliveryOptions(BaseModel):
#     delivery_option: DeliveryOptionType = Field(default=DeliveryOptionType.INCLUDED)
#
#     class Config:
#         from_attributes = True  # orm_mode
