from typing import Self

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.users_crud.schemas.custom_types import RoleType
from src.users_crud.schemas import BuyerInformation


class User(BaseModel):
    username: str = Field(default=None, examples=["alex", "bo$$$"])
    email: EmailStr | None


class UserCreate(User):
    password: str = Field(default=None, examples=["1234", "qwerty"])
    role: RoleType = Field(default=RoleType.USER, examples=[RoleType.USER, RoleType.BUYER])
    buyer_information: BuyerInformation | None = Field(
        description="If your 'role' is USER, then you do not need to fill in this field."
    )


class UserUpdate(User):
    password: str | None = Field(default=None)
    buyer_information: BuyerInformation | None


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
