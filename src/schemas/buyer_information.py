from typing import List

from pydantic import BaseModel, Field

from src.schemas import Location, CommissionRate, PriceRange
from src.schemas.custom_types import ProductSegmentType, PaymentOptionType, DeliveryOptionType


class BuyerInformation(BaseModel):
    location: Location
    import_countries: List[str] = Field(example=["USA", "UK"])
    product_segment: ProductSegmentType
    commission_rate: CommissionRate
    price_range: PriceRange
    delivery_options: DeliveryOptionType
    payment_options: List[PaymentOptionType] = Field(
        default=[PaymentOptionType.CARD_PAYMENT, PaymentOptionType.ON_DELIVERY]
    )
    prepayment_percentage: float = Field(ge=0, le=100)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            delivery_options=obj.delivery_options,
            payment_options=[PaymentOptionType(option_obj.payment_option) for option_obj in obj.payment_options],
            product_segment=obj.product_segment,
            price_range=obj.price_range,
            import_countries=obj.import_countries,
            prepayment_percentage=obj.prepayment_percentage,
            location=obj.location,
            commission_rate=obj.commission_rate
        )

    class Config:
        from_attributes = True  # orm_mode
