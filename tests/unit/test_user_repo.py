from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserOrm, PaymentOptionsOrm, BuyerInformationOrm
from src.repositories import UserRepo, BuyerInformationRepo
from src.schemas import UserCreate, UserUpdate
from src.schemas.custom_types import PaymentOptionType, RoleType
from tests.unit.conftest import new_session_test


async def test_create_user_existing_user(mocker, user_create_data):
    mock_get_user = mocker.patch(
        'src.repositories.user_repo.UserRepo.get_user',
        new_callable=AsyncMock,
        return_value=UserOrm(username="existing_user")
    )
    user_create = UserCreate(**user_create_data)
    result = await UserRepo.create_user(user_create)

    assert result is None
    mock_get_user.assert_called_once_with(username="existing_user")


async def test_create_user_success(mocker, buyer_create_data):
    mock_get_user = mocker.patch(
        'src.repositories.user_repo.UserRepo.get_user',
        new_callable=AsyncMock,
        return_value=None
    )
    mocker.patch(
        'src.repositories.user_repo.new_session',
        new_session_test
    )
    user_create = UserCreate(**buyer_create_data)
    result = await UserRepo.create_user(user_create)

    assert result is not None
    assert result.username == user_create.username
    assert result.email == user_create.email
    assert result.role == user_create.role.value

    mock_get_user.assert_called_once_with(username=user_create.username)

    async with new_session_test() as session:
        user_from_db = await session.get(UserOrm, result.id)
        assert user_from_db is not None
        assert user_from_db.username == user_create.username
        assert user_from_db.email == user_create.email


async def test_get_user_by_id(mocker):
    user_id = 1
    user_orm = UserOrm(id=user_id, username="test_user")

    mocker.patch(
        'src.repositories.user_repo.new_session',
        new_session_test
    )
    mock_result = mocker.Mock()
    mock_result.scalar_one.return_value = user_orm
    mocker.patch(
        'sqlalchemy.ext.asyncio.AsyncSession.execute',
        return_value=mock_result
    )
    result = await UserRepo.get_user(user_id=user_id)

    assert result == user_orm
    mock_result.scalar_one.assert_called_once()


async def test_get_user_by_username(mocker):
    username = "test_user"
    user_orm = UserOrm(id=1, username=username)

    mocker.patch(
        'src.repositories.user_repo.new_session',
        new_session_test
    )
    mock_result = mocker.Mock()
    mock_result.scalar_one.return_value = user_orm
    mocker.patch(
        'sqlalchemy.ext.asyncio.AsyncSession.execute',
        return_value=mock_result
    )
    result = await UserRepo.get_user(username=username)

    assert result == user_orm
    mock_result.scalar_one.assert_called_once()


async def test_get_user_not_found(mocker):
    username = "non_existent_user"

    mocker.patch(
        'src.repositories.user_repo.new_session',
        new_session_test
    )
    mock_execute = mocker.patch(
        'sqlalchemy.ext.asyncio.AsyncSession.execute',
        side_effect=NoResultFound
    )
    result = await UserRepo.get_user(username=username)

    assert result is None
    mock_execute.assert_called_once()


async def test_get_users(mocker):
    user_orm_1 = UserOrm(id=1, username="user1")
    user_orm_2 = UserOrm(id=2, username="user2")
    expected_users = [user_orm_1, user_orm_2]

    mocker.patch(
        'src.repositories.user_repo.new_session',
        new_session_test
    )
    mock_result = mocker.Mock()
    mock_result.scalars.return_value.all.return_value = expected_users
    mocker.patch(
        'sqlalchemy.ext.asyncio.AsyncSession.execute',
        return_value=mock_result
    )
    result = await UserRepo.get_users()

    assert result == expected_users
    mock_result.scalars.return_value.all.assert_called_once()


async def test_update_user_attributes_password(mocker):
    user_orm = UserOrm(id=1, username="user1", hashed_password="old_hashed_password")
    user_update = UserUpdate(
        email="email@example.com",
        password="new_password",
        buyer_information=None
    )

    mock_get_password_hash = mocker.patch(
        'src.repositories.user_repo.get_password_hash',
        return_value="new_hashed_password"
    )
    updated_user = await UserRepo._UserRepo__update_user_attributes(user_orm, user_update)

    assert updated_user.hashed_password == "new_hashed_password"
    mock_get_password_hash.assert_called_once_with("new_password")


async def test_update_user_attributes_other_fields(mocker):
    user_orm = UserOrm(id=1, username="user1", email="old_email@example.com")
    user_update = UserUpdate(
        email="new_email@example.com",
        username="new_user1",
        buyer_information=None
    )
    updated_user = await UserRepo._UserRepo__update_user_attributes(user_orm, user_update)

    assert updated_user.email == "new_email@example.com"
    assert updated_user.username == "new_user1"


async def test_update_payment_options(mocker, user_update_data):
    payment_option_1 = PaymentOptionsOrm(payment_option=PaymentOptionType.CRYPTOCURRENCY)
    payment_option_2 = PaymentOptionsOrm(payment_option=PaymentOptionType.PREPAYMENT_100)
    buyer_information_orm = BuyerInformationOrm(payment_options=[payment_option_1, payment_option_2])
    user_orm = UserOrm(id=1, username="user1", buyer_information=buyer_information_orm)

    user_update = UserUpdate(**user_update_data)

    mock_commit = mocker.patch.object(AsyncSession, 'commit', return_value=None)
    mock_refresh = mocker.patch.object(AsyncSession, 'refresh', return_value=None)

    async with new_session_test() as session:
        updated_user = await UserRepo._UserRepo__update_payment_options(session, user_orm, user_update)

    assert mock_commit.call_count == len(user_update.buyer_information.payment_options)
    assert mock_refresh.call_count == len(user_update.buyer_information.payment_options)
    assert len(updated_user.buyer_information.payment_options) == len(user_update.buyer_information.payment_options)

    expected_payment_options = {opt.payment_option for opt in updated_user.buyer_information.payment_options}
    actual_payment_options = set(user_update.buyer_information.payment_options)
    assert expected_payment_options == actual_payment_options


async def test_update_user(mocker, user_update_data):
    payment_option_1 = PaymentOptionsOrm(payment_option="ON_DELIVERY")
    payment_option_2 = PaymentOptionsOrm(payment_option="CARD_PAYMENT")
    buyer_information_orm = BuyerInformationOrm(payment_options=[payment_option_1, payment_option_2])
    user_update = UserUpdate(**user_update_data)
    user_orm = UserOrm(
        id=1,
        username="user1",
        role="BUYER",
        buyer_information=buyer_information_orm
    )
    mock_session = mocker.MagicMock(spec=AsyncSession)

    mock_execute = mocker.patch(
        'src.repositories.user_repo.AsyncSession.execute',
        return_value=mocker.MagicMock(
            scalar_one_or_none=lambda: user_orm
        )
    )
    mock_commit = mocker.patch(
        'src.repositories.user_repo.AsyncSession.commit',
        return_value=None
    )
    mock_update_user_attributes = mocker.patch(
        'src.repositories.user_repo.UserRepo._UserRepo__update_user_attributes',
        return_value=user_orm
    )
    mock_update_buyer_information = mocker.patch(
        'src.repositories.user_repo.BuyerInformationRepo.update_buyer_information',
        return_value=buyer_information_orm
    )
    mock_update_payment_options = mocker.patch(
        'src.repositories.user_repo.UserRepo._UserRepo__update_payment_options',
        return_value=user_orm
    )
    updated_user = await UserRepo.update_user(1, user_update)

    assert updated_user == user_orm
    mock_update_user_attributes.assert_called_once_with(user_orm=user_orm, user_update=user_update)
    mock_update_buyer_information.assert_called_once_with(buyer_information_orm, user_update.buyer_information)
    mock_commit.assert_called_once()


async def test_delete_user(mocker):
    user_id = 1
    user_orm = AsyncMock()
    mock_get_user = mocker.patch(
        'src.repositories.user_repo.UserRepo.get_user',
        return_value=user_orm
    )
    mock_delete = mocker.patch(
        'src.repositories.user_repo.AsyncSession.delete',
        return_value=None
    )
    mock_commit = mocker.patch(
        'src.repositories.user_repo.AsyncSession.commit',
        return_value=None
    )
    mock_new_session = mocker.patch(
        'src.repositories.user_repo.new_session',
        return_value=new_session_test()
    )
    result = await UserRepo.delete_user(user_id)

    assert result is True

    mock_get_user.assert_called_once_with(user_id=user_id)
    mock_new_session.assert_called_once()
    mock_delete.assert_called_once_with(user_orm)
    mock_commit.assert_called_once()


async def test_delete_user_no_user(mocker):
    user_id = 1
    mock_get_user = mocker.patch(
        'src.repositories.user_repo.UserRepo.get_user',
        return_value=None
    )
    mock_new_session = mocker.patch(
        'src.repositories.user_repo.new_session',
        return_value=new_session_test()
    )
    mock_delete = mocker.patch(
        'src.repositories.user_repo.AsyncSession.delete',
        return_value=None
    )
    mock_commit = mocker.patch(
        'src.repositories.user_repo.AsyncSession.commit',
        return_value=None
    )

    result = await UserRepo.delete_user(user_id)

    assert result is False

    mock_get_user.assert_called_once_with(user_id=user_id)
    mock_new_session.assert_not_called()
    mock_delete.assert_not_called()
    mock_commit.assert_not_called()
