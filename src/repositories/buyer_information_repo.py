from src.models import BuyerInformationOrm
from src.schemas import BuyerInformation


class BuyerInformationRepo:
    @staticmethod
    async def update_buyer_information(
            buyer_info_orm: BuyerInformationOrm,
            updated_buyer_info: BuyerInformation
    ):
        # Обновление вложенных объектов
        buyer_info_orm.location.country = updated_buyer_info.location.country
        buyer_info_orm.location.city = updated_buyer_info.location.city

        buyer_info_orm.price_range.min_price = updated_buyer_info.price_range.min_price
        buyer_info_orm.price_range.max_price = updated_buyer_info.price_range.max_price

        buyer_info_orm.commission_rate.min_rate = updated_buyer_info.commission_rate.min_rate
        buyer_info_orm.commission_rate.max_rate = updated_buyer_info.commission_rate.max_rate

        buyer_info_orm.import_countries = updated_buyer_info.import_countries
        buyer_info_orm.product_segment = updated_buyer_info.product_segment
        buyer_info_orm.delivery_options = updated_buyer_info.delivery_options
        buyer_info_orm.prepayment_percentage = updated_buyer_info.prepayment_percentage

        return buyer_info_orm


