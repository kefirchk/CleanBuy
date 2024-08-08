from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    username: str = Field(default=None, examples=["alex", "bo$$$"])
    email: EmailStr | None
