"""Product models"""
from typing import List, Optional
from pydantic import BaseModel, Field
# from bson import ObjectId
from .base import PyObjectId


class ProductBase(BaseModel):
    """Product base schema"""
    name: str
    description: str
    price: float
    category_ids: List[PyObjectId]
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    """Product create schema"""
    name: str
    description: str
    price: float
    category_ids: List[str]
    image_url: Optional[str] = None


class Product(ProductBase):
    """Product schema"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        """Product config"""
        populate_by_name = True
        json_encoders = {PyObjectId: lambda x: str(x)}
