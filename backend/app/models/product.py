from pydantic import BaseModel, Field
from bson import ObjectId
from .base import PyObjectId
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_ids: List[PyObjectId]
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
