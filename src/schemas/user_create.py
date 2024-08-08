from pydantic import Field

from src.schemas import User, BuyerInformation
from src.schemas.custom_types import RoleType


class UserCreate(User):
    password: str = Field(default=None, examples=["1234", "qwerty"])
    role: RoleType = Field(default=RoleType.USER, examples=[RoleType.USER, RoleType.BUYER])
    buyer_information: BuyerInformation | None = Field(
        description="If your 'role' is USER, then you do not need to fill in this field."
    )
