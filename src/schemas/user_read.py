from typing_extensions import Self

from pydantic import Field, ConfigDict

from src.schemas.custom_types import RoleType
from src.schemas import User, BuyerInformation


class UserRead(User):
    id: int = Field(gt=0)
    role: RoleType = Field(default=RoleType.USER, examples=[RoleType.USER, RoleType.BUYER])
    buyer_information: BuyerInformation | None

    @classmethod
    def from_orm(cls, obj) -> Self:
        return cls(
            id=obj.id,
            username=obj.username,
            role=obj.role,
            email=obj.email,
            buyer_information=BuyerInformation.from_orm(obj.buyer_information) if obj.buyer_information else None
        )
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
