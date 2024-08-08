from pydantic import BaseModel, Field


class Location(BaseModel):
    country: str = Field(default="Belarus", examples=["Belarus", "Russia"])
    city: str = Field(default="Minsk", examples=["Minsk", "Moscow", "New York"])

    class Config:
        from_attributes = True  # orm_mode