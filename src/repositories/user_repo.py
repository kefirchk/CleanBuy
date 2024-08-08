from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import NoResultFound

from src.auth.utils import get_password_hash
from src.database import new_session
from src.models import UserOrm, BuyerInformationOrm, LocationOrm, CommissionRateOrm, PriceRangeOrm, PaymentOptionsOrm
from src.repositories import BuyerInformationRepo
from src.schemas import UserCreate, UserUpdate, BuyerInformation
from src.schemas.custom_types import RoleType


class UserRepo:
    @staticmethod
    async def create_user(user_create: UserCreate) -> UserOrm | None:
        other_user = await UserRepo.get_user(username=user_create.username)
        if other_user:
            return None

        buyer_information_data = user_create.buyer_information.dict() if user_create.buyer_information else None
        buyer_information_orm = None

        if user_create.role == RoleType.BUYER:
            if buyer_information_data:
                buyer_information_orm = BuyerInformationOrm(
                    location=LocationOrm(**buyer_information_data['location']),
                    import_countries=buyer_information_data['import_countries'],  # убедитесь, что это список
                    product_segment=buyer_information_data['product_segment'],
                    commission_rate=CommissionRateOrm(**buyer_information_data['commission_rate']),
                    price_range=PriceRangeOrm(**buyer_information_data['price_range']),
                    delivery_options=buyer_information_data['delivery_options'],
                    # DeliveryOptionsOrm(delivery_option=user_create.buyer_information.delivery_options.delivery_option.value),
                    payment_options=[
                        PaymentOptionsOrm(payment_option=opt) for opt in buyer_information_data['payment_options']
                    ],
                    prepayment_percentage=buyer_information_data['prepayment_percentage']
                )
        user_orm = UserOrm(
            username=user_create.username,
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
            role=user_create.role.value,
            buyer_information=buyer_information_orm
        )

        async with new_session() as session:
            session.add(user_orm)
            await session.commit()
            await session.refresh(user_orm)

        return user_orm

    @staticmethod
    async def get_user(user_id: int = None, username: str = None) -> UserOrm | None:
        if user_id:
            query = select(UserOrm).options(
                joinedload(UserOrm.buyer_information)
            ).where(UserOrm.id == user_id)
        else:
            query = select(UserOrm).options(
                joinedload(UserOrm.buyer_information)
            ).where(UserOrm.username == username)

        async with new_session() as session:
            try:
                result = await session.execute(query)
                user_orm = result.scalar_one()

            except NoResultFound:
                return None

        return user_orm

    @classmethod
    async def get_users(cls) -> List[UserOrm] | None:
        async with new_session() as session:
            # TODO: add pagination

            query = select(UserOrm).options(joinedload(UserOrm.buyer_information))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def __update_user_attributes(cls, user_orm: UserOrm, user_update: UserUpdate):
        user_update_dict = user_update.dict(
            exclude_none=True,
            exclude_unset=True,
            exclude={'buyer_information'}
        )
        if 'password' in user_update_dict:
            user_orm.hashed_password = get_password_hash(user_update.password)
            user_update_dict.pop('password')
        for key, value in user_update_dict.items():
            setattr(user_orm, key, value)
        return user_orm

    @classmethod
    async def __update_payment_options(
            cls,
            session: AsyncSession,
            user_orm: UserOrm,
            user_update: UserUpdate
    ):
        user_orm.buyer_information.payment_options.clear()

        # Добавление новых опций оплаты, если они существуют и валидны
        valid_payment_options = []
        for option_type in user_update.buyer_information.payment_options:
            # stmt = select(PaymentOptionsOrm).filter_by(payment_option=option_type)
            # result = await session.execute(stmt)
            # payment_option = result.scalar_one_or_none()

            # if payment_option is None:
            payment_option = PaymentOptionsOrm(payment_option=option_type)
            session.add(payment_option)
            await session.commit()
            await session.refresh(payment_option)

            #if payment_option:  # Убеждаемся, что payment_option не None
            valid_payment_options.append(payment_option)

        user_orm.buyer_information.payment_options.extend(valid_payment_options)
        return user_orm

    @classmethod
    async def update_user(cls, user_id: int, user_update: UserUpdate) -> UserOrm | None:
        async with new_session() as session:
            # Получаем пользователя и загружаем связанные объекты
            stmt = select(UserOrm).options(
                selectinload(UserOrm.buyer_information).selectinload(BuyerInformationOrm.payment_options)).filter_by(
                id=user_id)
            result = await session.execute(stmt)
            user_orm = result.scalar_one_or_none()

            if user_orm:
                # Обновляем основные поля пользователя
                user_orm = await cls.__update_user_attributes(user_orm=user_orm, user_update=user_update)

                # Проверка роли пользователя
                if user_orm.role == RoleType.BUYER and user_update.buyer_information:
                    if not user_orm.buyer_information:
                        # Если у пользователя нет BuyerInformationOrm, создаем новый
                        user_orm.buyer_information = BuyerInformationOrm()

                    buyer_info_orm: BuyerInformationOrm = user_orm.buyer_information
                    updated_buyer_info = user_update.buyer_information

                    # Обновление вложенных объектов
                    buyer_info_orm = await BuyerInformationRepo.update_buyer_information(
                        buyer_info_orm, updated_buyer_info
                    )

                    # Обновление опций оплаты
                    user_orm = await cls.__update_payment_options(session, user_orm, user_update)

                else:
                    # Если роль пользователя не BUYER, удаляем информацию о покупателе
                    user_orm.buyer_information = None

                # Сохраняем изменения
                await session.commit()

            return user_orm

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        user_orm = await UserRepo.get_user(user_id=user_id)
        if user_orm:
            async with new_session() as session:
                await session.delete(user_orm)
                await session.commit()
                return True
        else:
            return False
