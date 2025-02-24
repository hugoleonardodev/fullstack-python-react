from pydantic import BaseModel, Field, UUID4
from typing import List
from datetime import datetime


class OrderBase(BaseModel):
    date: datetime
    product_ids: List[UUID4]
    total: float


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: UUID4 = Field(default_factory=UUID4, alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {UUID4: str}
