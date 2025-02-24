from pydantic import BaseModel, Field, UUID4
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_ids: List[UUID4]
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: UUID4 = Field(default_factory=UUID4, alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {UUID4: str}
