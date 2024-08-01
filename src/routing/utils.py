from typing import List

from fastapi import Form

from src.schemas.buyer import BuyerInformation, ProductSegmentType, Location, CommissionRate, PriceRange, \
    DeliveryOptions, PaymentOptions


def get_buyer_information(
    country: str = Form(example="USA", description="The buyer's country"),
    city: str = Form(example="New York", description="The buyer's city"),
    import_countries: List[str] = Form(),
    product_segment: ProductSegmentType = Form(),
    min_rate: float = Form(ge=0, le=100),
    max_rate: float = Form(ge=0, le=100),
    min_price: float = Form(ge=0),
    max_price: float = Form(ge=0),
    included: bool = Form(),
    not_included: bool = Form(),
    negotiable: bool = Form(),
    cryptocurrency: bool = Form(),
    card_payment: bool = Form(),
    on_delivery: bool = Form(),
    prepayment_100: bool = Form(),
    prepayment_percentage: float = Form(ge=0, le=100)
) -> BuyerInformation:
    return BuyerInformation(
        location=Location(country=country, city=city),
        import_countries=import_countries,
        product_segment=product_segment,
        commission_rate=CommissionRate(min_rate=min_rate, max_rate=max_rate),
        price_range=PriceRange(min_price=min_price, max_price=max_price),
        delivery_options=DeliveryOptions(
            included=included,
            not_included=not_included,
            negotiable=negotiable,
        ),
        payment_options=PaymentOptions(
            cryptocurrency=cryptocurrency,
            card_payment=card_payment,
            on_delivery=on_delivery,
            prepayment_100=prepayment_100,
        ),
        prepayment_percentage=prepayment_percentage
    )