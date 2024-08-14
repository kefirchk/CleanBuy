from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import NoResultFound

from src.database import new_session
from src.users_crud.models import UserOrm, BuyerInformationOrm, LocationOrm, CommissionRateOrm, PriceRangeOrm, \
    PaymentOptionsOrm
from src.users_crud.repositories import BuyerInformationRepo
from src.users_crud.schemas import UserCreate, UserUpdate
from src.users_crud.schemas.custom_types import RoleType
from src.auth import get_password_hash


class UserRepo:
    @staticmethod
    async def create_user(user_create: UserCreate) -> UserOrm | None:
        other_user = await UserRepo.get_user(username=user_create.username)
        if other_user:
            return None

        buyer_information_data = user_create.buyer_information.model_dump( ) if user_create.buyer_information else None
        buyer_information_orm = None

        if user_create.role == RoleType.BUYER:
            if buyer_information_data:
                buyer_information_orm = BuyerInformationOrm(
                    location=LocationOrm(**buyer_information_data['location']),
                    import_countries=buyer_information_data['import_countries'],
                    product_segment=buyer_information_data['product_segment'],
                    commission_rate=CommissionRateOrm(**buyer_information_data['commission_rate']),
                    price_range=PriceRangeOrm(**buyer_information_data['price_range']),
                    delivery_options=buyer_information_data['delivery_options'],
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
        user_update_dict = user_update.model_dump(
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
        valid_payment_options = []
        for option_type in user_update.buyer_information.payment_options:
            payment_option = PaymentOptionsOrm(payment_option=option_type)
            session.add(payment_option)
            await session.commit()
            await session.refresh(payment_option)
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
                user_orm = await cls.__update_user_attributes(user_orm=user_orm, user_update=user_update)

                if user_orm.role == RoleType.BUYER and user_update.buyer_information:
                    if not user_orm.buyer_information:
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
                    user_orm.buyer_information = None

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
