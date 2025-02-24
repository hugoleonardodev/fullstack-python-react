from pydantic import BaseModel, Field
from bson import ObjectId
from .base import PyObjectId


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
