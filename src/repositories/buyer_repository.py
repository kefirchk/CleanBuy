from typing import List, Optional

from sqlalchemy import select

from src.repositories.models import BuyerOrm
from src.repositories.utils import create_tables_of_buyer, update_simple_attributes_of_buyer, \
    update_nested_objects_of_buyer, delete_tables_of_buyer
from src.schemas.buyer import BuyerInformation, Buyer
from src.database import new_session
from src.services.model_converter import ModelConverter


class BuyerRepository:
    @classmethod
    async def create_buyer(cls, buyer_info: BuyerInformation) -> int:
        async with new_session() as session:
            buyer_info_dict = await create_tables_of_buyer(buyer_info, session)
            buyer = BuyerOrm(**buyer_info_dict)
            session.add(buyer)
            await session.commit()
            await session.refresh(buyer)
            return buyer.id

    @classmethod
    async def get_buyer(cls, buyer_id: int) -> Optional[BuyerOrm]:
        async with new_session() as session:
            result = await session.execute(select(BuyerOrm).where(BuyerOrm.id == buyer_id))
            return result.scalars().first()

    @classmethod
    async def get_buyers(cls) -> Optional[List[BuyerOrm]]:
        async with new_session() as session:
            result = await session.execute(select(BuyerOrm))
            return result.scalars().all()

    @classmethod
    async def update_buyer(cls, buyer_id: int, buyer_info: BuyerInformation) -> Optional[Buyer]:
        async with new_session() as session:
            result = await session.execute(select(BuyerOrm).where(BuyerOrm.id == buyer_id))
            buyer_orm = result.scalars().first()
            if buyer_orm:
                buyer_orm = update_simple_attributes_of_buyer(buyer_orm, buyer_info)
                await update_nested_objects_of_buyer(session, buyer_orm, buyer_info)
                await session.commit()
                await session.refresh(buyer_orm)
                return buyer_orm
            return None

    @classmethod
    async def delete_buyer(cls, buyer_id: int) -> bool:
        async with new_session() as session:
            buyer_orm = await cls.get_buyer(buyer_id)
            if buyer_orm:
                await session.delete(buyer_orm)
                await delete_tables_of_buyer(session, buyer_orm)
                await session.commit()
                return True
            return False
