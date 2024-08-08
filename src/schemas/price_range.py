from pydantic import BaseModel, Field


class PriceRange(BaseModel):
    min_price: float = Field(default=1, gt=0, examples=[10, 20, 30])
    max_price: float = Field(default=1, gt=0, examples=[10, 20, 30])

    class Config:
        from_attributes = True  # orm_mode
