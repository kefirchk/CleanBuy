from fastapi import APIRouter, HTTPException, Depends

from src.repositories.buyer_repository import BuyerRepository
from src.routing.utils import get_buyer_information
from src.schemas.buyer import BuyerInformation, Buyer
from src.services.model_converter import ModelConverter

router = APIRouter(
    prefix="/buyer",
    tags=["Buyer Operations"]
)


@router.get('/all')
async def get_buyers():
    buyers_orm = await BuyerRepository.get_buyers()
    if not buyers_orm:
        raise HTTPException(status_code=404, detail="Buyers not found")
    buyers = []
    for buyer in buyers_orm:
        converted_buyer = await ModelConverter.buyerOrm_to_buyerSchema(buyer)
        buyers.append(converted_buyer)
    return buyers


@router.get('/{buyer_id}', response_model=Buyer)
async def get_buyer(buyer_id: int):
    buyer_orm = await BuyerRepository.get_buyer(buyer_id)
    if buyer_orm is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    buyer = await ModelConverter.buyerOrm_to_buyerSchema(buyer_orm)
    return buyer


@router.put('/{buyer_id}', response_model=dict)
async def update_buyer(buyer_id: int, buyer_info: BuyerInformation = Depends(get_buyer_information)):
    buyer_orm = await BuyerRepository.update_buyer(buyer_id, buyer_info)
    if buyer_orm is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return {
        "status": "success",
        "buyer_id": buyer_orm.id,
    }


@router.delete('/{buyer_id}', response_model=dict)
async def delete_buyer(buyer_id: int):
    is_deleted = await BuyerRepository.delete_buyer(buyer_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return {
        "status": "success",
        "message": "Buyer deleted successfully."
    }
