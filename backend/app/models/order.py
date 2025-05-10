"""Order models"""
from pydantic import BaseModel, Field
from .base import PyObjectId
from typing import List
from datetime import datetime


class OrderBase(BaseModel):
    """Order base schema"""
    date: datetime
    product_ids: List[PyObjectId]
    total: float
    # category_ids: List[PyObjectId]


class OrderCreate(OrderBase):
    """Order create schema"""
    date: str
    product_ids: List[str]
    total: str
    # category_ids: List[str]


class Order(OrderBase):
    """Order schema"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        """Order config"""
        populate_by_name = True
        json_encoders = {PyObjectId: lambda x: str(x)}
