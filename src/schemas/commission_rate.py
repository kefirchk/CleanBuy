from pydantic import BaseModel, Field


class CommissionRate(BaseModel):
    min_rate: float = Field(default=1, ge=0, le=100)
    max_rate: float = Field(default=100, ge=0, le=100)

    class Config:
        from_attributes = True  # orm_mode
