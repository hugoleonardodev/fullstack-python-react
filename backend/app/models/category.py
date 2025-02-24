from pydantic import BaseModel, Field, UUID4


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: UUID4 = Field(default_factory=UUID4, alias="_id")
    
    class Config:
        populate_by_name = True
        json_encoders = {UUID4: str}
