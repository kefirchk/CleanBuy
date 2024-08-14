from pydantic import BaseModel, Field, ConfigDict


class PriceRange(BaseModel):
    min_price: float = Field(default=1, gt=0, examples=[10, 20, 30])
    max_price: float = Field(default=1, gt=0, examples=[10, 20, 30])

    model_config = ConfigDict(from_attributes=True)

