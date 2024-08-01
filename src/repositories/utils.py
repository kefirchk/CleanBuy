from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.models import LocationOrm, CommissionRateOrm, PriceRangeOrm, DeliveryOptionsOrm, \
    PaymentOptionsOrm, BuyerOrm
from src.schemas.buyer import BuyerInformation


async def add_location(buyer_info: BuyerInformation, session: AsyncSession) -> int:
    location_orm = LocationOrm(**buyer_info.location.model_dump())
    session.add(location_orm)
    await session.commit()
    await session.refresh(location_orm)
    return location_orm.id


async def add_commission_rate(buyer_info: BuyerInformation, session: AsyncSession) -> int:
    commission_rate_orm = CommissionRateOrm(**buyer_info.commission_rate.model_dump())
    session.add(commission_rate_orm)
    await session.commit()
    await session.refresh(commission_rate_orm)
    return commission_rate_orm.id


async def add_price_range(buyer_info: BuyerInformation, session: AsyncSession) -> int:
    price_range_orm = PriceRangeOrm(**buyer_info.price_range.model_dump())
    session.add(price_range_orm)
    await session.commit()
    await session.refresh(price_range_orm)
    return price_range_orm.id


async def add_delivery_options(buyer_info: BuyerInformation, session: AsyncSession) -> int:
    delivery_options_orm = DeliveryOptionsOrm(**buyer_info.delivery_options.model_dump())
    session.add(delivery_options_orm)
    await session.commit()
    await session.refresh(delivery_options_orm)
    return delivery_options_orm.id


async def add_payment_options(buyer_info: BuyerInformation, session: AsyncSession) -> int:
    payment_options_orm = PaymentOptionsOrm(**buyer_info.payment_options.model_dump())
    session.add(payment_options_orm)
    await session.commit()
    await session.refresh(payment_options_orm)
    return payment_options_orm.id


async def create_tables_of_buyer(buyer_info, session):
    buyer_info_dict = buyer_info.model_dump()

    buyer_info_dict['location_id'] = await add_location(buyer_info, session)
    buyer_info_dict.pop('location')

    buyer_info_dict['commission_rate_id'] = await add_commission_rate(buyer_info, session)
    buyer_info_dict.pop('commission_rate')

    buyer_info_dict['price_range_id'] = await add_price_range(buyer_info, session)
    buyer_info_dict.pop('price_range')

    buyer_info_dict['delivery_options_id'] = await add_delivery_options(buyer_info, session)
    buyer_info_dict.pop('delivery_options')

    buyer_info_dict['payment_options_id'] = await add_payment_options(buyer_info, session)
    buyer_info_dict.pop('payment_options')

    return buyer_info_dict


def update_simple_attributes_of_buyer(buyer_orm: BuyerOrm, buyer_info: BuyerInformation):
    buyer_orm.import_countries = buyer_info.import_countries
    buyer_orm.product_segment = buyer_info.product_segment
    buyer_orm.prepayment_percentage = buyer_info.prepayment_percentage
    return buyer_orm


async def update_nested_objects_of_buyer(session: AsyncSession, buyer_orm: BuyerOrm, buyer_info: BuyerInformation):
    await session.execute(
        update(CommissionRateOrm)
        .where(CommissionRateOrm.id == buyer_orm.commission_rate_id)
        .values(min_rate=buyer_info.commission_rate.min_rate,
                max_rate=buyer_info.commission_rate.max_rate))

    await session.execute(
        update(PriceRangeOrm)
        .where(PriceRangeOrm.id == buyer_orm.price_range_id)
        .values(min_price=buyer_info.price_range.min_price,
                max_price=buyer_info.price_range.max_price))

    await session.execute(
        update(DeliveryOptionsOrm)
        .where(DeliveryOptionsOrm.id == buyer_orm.delivery_options_id)
        .values(included=buyer_info.delivery_options.included,
                not_included=buyer_info.delivery_options.not_included,
                negotiable=buyer_info.delivery_options.negotiable))

    await session.execute(
        update(PaymentOptionsOrm)
        .where(PaymentOptionsOrm.id == buyer_orm.payment_options_id)
        .values(cryptocurrency=buyer_info.payment_options.cryptocurrency,
                card_payment=buyer_info.payment_options.card_payment,
                on_delivery=buyer_info.payment_options.on_delivery,
                prepayment_100=buyer_info.payment_options.prepayment_100))

    await session.execute(
        update(LocationOrm)
        .where(LocationOrm.id == buyer_orm.location_id)
        .values(country=buyer_info.location.country,
                city=buyer_info.location.city))


async def delete_tables_of_buyer(session: AsyncSession, buyer_orm: BuyerOrm):
    await session.execute(
        delete(CommissionRateOrm)
        .where(CommissionRateOrm.id == buyer_orm.commission_rate_id)
    )

    await session.execute(
        delete(PriceRangeOrm)
        .where(PriceRangeOrm.id == buyer_orm.price_range_id)
    )

    await session.execute(
        delete(PaymentOptionsOrm)
        .where(PaymentOptionsOrm.id == buyer_orm.payment_options_id)
    )

    await session.execute(
        delete(DeliveryOptionsOrm)
        .where(DeliveryOptionsOrm.id == buyer_orm.delivery_options_id)
    )

    await session.execute(
        delete(LocationOrm)
        .where(LocationOrm.id == buyer_orm.location_id)
    )
