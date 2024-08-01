from fastapi import APIRouter, Depends

from src.repositories.buyer_repository import BuyerRepository
from src.routing.utils import get_buyer_information
from src.schemas.buyer import BuyerInformation

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post('/register_buyer', response_model=dict)
async def register_buyer(buyer_info: BuyerInformation = Depends(get_buyer_information)):
    buyer_id = await BuyerRepository.create_buyer(buyer_info)
    return {
        "status": "success",
        "buyer_id": buyer_id
    }
