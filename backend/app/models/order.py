from pydantic import BaseModel, Field
# from bson import ObjectId
from .base import PyObjectId
from typing import List
from datetime import datetime


class OrderBase(BaseModel):
    date: datetime
    product_ids: List[PyObjectId]
    total: float
    category_ids: List[PyObjectId]


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: lambda x: str(x)}
