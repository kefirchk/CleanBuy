from src.repositories.models import BuyerOrm
from src.schemas.buyer import Location, CommissionRate, PriceRange, PaymentOptions, DeliveryOptions, Buyer


class ModelConverter:
    @classmethod
    async def buyerOrm_to_buyerSchema(cls, buyer_orm: BuyerOrm) -> Buyer:
        location = Location(
            country=buyer_orm.location.country,
            city=buyer_orm.location.city
        )

        commission_rate = CommissionRate(
            min_rate=buyer_orm.commission_rate.min_rate,
            max_rate=buyer_orm.commission_rate.max_rate
        )

        price_range = PriceRange(
            min_price=buyer_orm.price_range.min_price,
            max_price=buyer_orm.price_range.max_price
        )

        delivery_options = DeliveryOptions(
            included=buyer_orm.delivery_options.included,
            not_included=buyer_orm.delivery_options.not_included,
            negotiable=buyer_orm.delivery_options.negotiable
        )

        payment_options = PaymentOptions(
            cryptocurrency=buyer_orm.payment_options.cryptocurrency,
            card_payment=buyer_orm.payment_options.card_payment,
            on_delivery=buyer_orm.payment_options.on_delivery,
            prepayment_100=buyer_orm.payment_options.prepayment_100
        )

        return Buyer(
            id=buyer_orm.id,
            location=location,
            import_countries=buyer_orm.import_countries,
            product_segment=buyer_orm.product_segment,
            commission_rate=commission_rate,
            price_range=price_range,
            delivery_options=delivery_options,
            payment_options=payment_options,
            prepayment_percentage=buyer_orm.prepayment_percentage
        )
