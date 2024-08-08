from pydantic import Field

from src.schemas import User, BuyerInformation


class UserUpdate(User):
    password: str | None = Field(default=None)
    buyer_information: BuyerInformation | None
