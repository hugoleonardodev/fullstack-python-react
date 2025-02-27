"""Category models"""
from pydantic import BaseModel, Field
from .base import PyObjectId


class CategoryBase(BaseModel):
    """Category base schema"""
    name: str


class CategoryCreate(CategoryBase):
    """Category create schema"""
    pass


class Category(CategoryBase):
    """Category schema"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        """Category config"""
        populate_by_name = True
        json_encoders = {PyObjectId: lambda x: str(x)}
