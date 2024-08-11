from src.models import BuyerInformationOrm
from src.repositories import BuyerInformationRepo
from src.schemas import BuyerInformation, Location, PriceRange, CommissionRate


async def test_update_buyer_information(mocker):
    mock_location = mocker.MagicMock(spec=Location)
    mock_price_range = mocker.MagicMock(spec=PriceRange)
    mock_commission_rate = mocker.MagicMock(spec=CommissionRate)

    buyer_info_orm = mocker.MagicMock(spec=BuyerInformationOrm)
    buyer_info_orm.location = mock_location
    buyer_info_orm.price_range = mock_price_range
    buyer_info_orm.commission_rate = mock_commission_rate

    updated_buyer_info = mocker.MagicMock(spec=BuyerInformation)
    updated_buyer_info.location = mock_location
    updated_buyer_info.price_range = mock_price_range
    updated_buyer_info.commission_rate = mock_commission_rate
    updated_buyer_info.import_countries = ['USA', 'Canada']
    updated_buyer_info.product_segment = 'PREMIUM'
    updated_buyer_info.delivery_options = 'EXPRESS'
    updated_buyer_info.prepayment_percentage = 70.0

    mock_location.country = 'NewCountry'
    mock_location.city = 'NewCity'
    mock_price_range.min_price = 200.0
    mock_price_range.max_price = 6000.0
    mock_commission_rate.min_rate = 20.0
    mock_commission_rate.max_rate = 30.0

    updated_buyer_info_orm = await BuyerInformationRepo.update_buyer_information(buyer_info_orm, updated_buyer_info)

    assert updated_buyer_info_orm == buyer_info_orm
    assert buyer_info_orm.location.country == updated_buyer_info.location.country
    assert buyer_info_orm.location.city == updated_buyer_info.location.city
    assert buyer_info_orm.price_range.min_price == updated_buyer_info.price_range.min_price
    assert buyer_info_orm.price_range.max_price == updated_buyer_info.price_range.max_price
    assert buyer_info_orm.commission_rate.min_rate == updated_buyer_info.commission_rate.min_rate
    assert buyer_info_orm.commission_rate.max_rate == updated_buyer_info.commission_rate.max_rate
    assert buyer_info_orm.import_countries == updated_buyer_info.import_countries
    assert buyer_info_orm.product_segment == updated_buyer_info.product_segment
    assert buyer_info_orm.delivery_options == updated_buyer_info.delivery_options
    assert buyer_info_orm.prepayment_percentage == updated_buyer_info.prepayment_percentage
