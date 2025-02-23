from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from ..models.category import Category, CategoryCreate

router = APIRouter()


@router.post("/", response_model=Category)
async def create_category(request: Request, category: CategoryCreate = Body(...)):
    category = jsonable_encoder(category)
    new_category = await request.app.mongodb["categories"].insert_one(category)
    created_category = await request.app.mongodb["categories"].find_one(
        {"_id": new_category.inserted_id}
    )
    return created_category


@router.get("/", response_model=List[Category])
async def list_categories(request: Request):
    categories = await request.app.mongodb["categories"].find().to_list(1000)
    return categories


@router.get("/{id}", response_model=Category)
async def get_category(id: str, request: Request):
    if (category := await request.app.mongodb["categories"].find_one({"_id": id})) is not None:
        return category
    raise HTTPException(status_code=404, detail=f"Category {id} not found")


@router.put("/{id}", response_model=Category)
async def update_category(id: str, request: Request, category: CategoryCreate = Body(...)):
    category = {k: v for k, v in category.dict().items() if v is not None}
    
    if len(category) >= 1:
        update_result = await request.app.mongodb["categories"].update_one(
            {"_id": id}, {"$set": category}
        )
        if update_result.modified_count == 1:
            if (updated_category := await request.app.mongodb["categories"].find_one({"_id": id})) is not None:
                return updated_category

    if (existing_category := await request.app.mongodb["categories"].find_one({"_id": id})) is not None:
        return existing_category

    raise HTTPException(status_code=404, detail=f"Category {id} not found")


@router.delete("/{id}", response_model=dict)
async def delete_category(id: str, request: Request):
    delete_result = await request.app.mongodb["categories"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return {"message": f"Category {id} deleted"}
    raise HTTPException(status_code=404, detail=f"Category {id} not found")
