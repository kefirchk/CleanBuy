from enum import Enum
from pydantic import BaseModel, Field
from typing import List


class ProductSegmentType(Enum):
    LUXURY = "LUXURY"
    PREMIUM = "PREMIUM"
    NICHE = "NICHE"
    MASS_MARKET = "MASS MARKET"
    BUDGET = "BUDGET"
    SEASONAL = "SEASONAL"
    ALL = "ALL"


class PriceRange(BaseModel):
    min_price: float = Field(gt=0)
    max_price: float = Field(gt=0)


class Location(BaseModel):
    country: str = Field(example="Belarus")
    city: str = Field(example="Minsk")


class CommissionRate(BaseModel):
    min_rate: float = Field(ge=0, le=100)
    max_rate: float = Field(ge=0, le=100)


class DeliveryOptions(BaseModel):
    included: bool
    not_included: bool
    negotiable: bool


class PaymentOptions(BaseModel):
    cryptocurrency: bool
    card_payment: bool
    on_delivery: bool
    prepayment_100: bool


class BuyerInformation(BaseModel):
    location: Location
    import_countries: List[str] = Field(example=["USA", "UK"])
    product_segment: ProductSegmentType
    commission_rate: CommissionRate
    price_range: PriceRange
    delivery_options: DeliveryOptions
    payment_options: PaymentOptions
    prepayment_percentage: float = Field(ge=0, le=100)


class Buyer(BuyerInformation):
    id: int
