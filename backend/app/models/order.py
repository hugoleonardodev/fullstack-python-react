from pydantic import BaseModel, Field
from bson import ObjectId
from .base import PyObjectId
from typing import List
from datetime import datetime


class OrderBase(BaseModel):
    date: datetime
    product_ids: List[PyObjectId]
    total: float


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
