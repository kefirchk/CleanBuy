from pydantic import BaseModel, Field, ConfigDict


class Location(BaseModel):
    country: str = Field(default="Belarus", examples=["Belarus", "Russia"])
    city: str = Field(default="Minsk", examples=["Minsk", "Moscow", "New York"])

    model_config = ConfigDict(from_attributes=True)
