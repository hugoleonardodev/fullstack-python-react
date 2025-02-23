from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from ..models.product import Product, ProductCreate

router = APIRouter()


@router.post("/", response_model=Product)
async def create_product(request: Request, product: ProductCreate = Body(...)):
    product = jsonable_encoder(product)
    new_product = await request.app.mongodb["products"].insert_one(product)
    created_product = await request.app.mongodb["products"].find_one(
        {"_id": new_product.inserted_id}
    )
    return created_product


@router.get("/", response_model=List[Product])
async def list_products(request: Request):
    products = await request.app.mongodb["products"].find().to_list(1000)
    return products


@router.get("/{id}", response_model=Product)
async def get_product(id: str, request: Request):
    if (product := await request.app.mongodb["products"].find_one({"_id": id})) is not None:
        return product
    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.put("/{id}", response_model=Product)
async def update_product(id: str, request: Request, product: ProductCreate = Body(...)):
    product = {k: v for k, v in product.dict().items() if v is not None}
    
    if len(product) >= 1:
        update_result = await request.app.mongodb["products"].update_one(
            {"_id": id}, {"$set": product}
        )
        if update_result.modified_count == 1:
            if (updated_product := await request.app.mongodb["products"].find_one({"_id": id})) is not None:
                return updated_product

    if (existing_product := await request.app.mongodb["products"].find_one({"_id": id})) is not None:
        return existing_product

    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.delete("/{id}", response_model=dict)
async def delete_product(id: str, request: Request):
    delete_result = await request.app.mongodb["products"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return {"message": f"Product {id} deleted"}
    raise HTTPException(status_code=404, detail=f"Product {id} not found")
