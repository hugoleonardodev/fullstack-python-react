from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from ..models.order import Order, OrderCreate

router = APIRouter()


@router.post("/", response_model=Order)
async def create_order(request: Request, order: OrderCreate = Body(...)):
    order = jsonable_encoder(order)
    new_order = await request.app.mongodb["orders"].insert_one(order)
    created_order = await request.app.mongodb["orders"].find_one(
        {"_id": new_order.inserted_id}
    )
    return created_order


@router.get("/", response_model=List[Order])
async def list_orders(request: Request):
    orders = await request.app.mongodb["orders"].find().to_list(1000)
    return orders


@router.get("/{id}", response_model=Order)
async def get_order(id: str, request: Request):
    if (order := await request.app.mongodb["orders"].find_one({"_id": id})) is not None:
        return order
    raise HTTPException(status_code=404, detail=f"Order {id} not found")


@router.put("/{id}", response_model=Order)
async def update_order(id: str, request: Request, order: OrderCreate = Body(...)):
    order = {k: v for k, v in order.dict().items() if v is not None}
    
    if len(order) >= 1:
        update_result = await request.app.mongodb["orders"].update_one(
            {"_id": id}, {"$set": order}
        )
        if update_result.modified_count == 1:
            if (updated_order := await request.app.mongodb["orders"].find_one({"_id": id})) is not None:
                return updated_order

    if (existing_order := await request.app.mongodb["orders"].find_one({"_id": id})) is not None:
        return existing_order

    raise HTTPException(status_code=404, detail=f"Order {id} not found")


@router.delete("/{id}", response_model=dict)
async def delete_order(id: str, request: Request):
    delete_result = await request.app.mongodb["orders"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return {"message": f"Order {id} deleted"}
    raise HTTPException(status_code=404, detail=f"Order {id} not found")