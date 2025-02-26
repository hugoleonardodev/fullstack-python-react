# backend/app/routes/products.py
import json
from typing import List, Optional
from fastapi import APIRouter, Request, HTTPException, status, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from ..models.product import Product

router = APIRouter()


@router.post("/", response_model=Product)
async def create_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_ids: str = Form(...),  # JSON string de IDs
    image: Optional[UploadFile] = File(None)
):
    # Parsear category_ids de JSON string para lista
    try:
        category_ids_list = json.loads(category_ids)
    except:
        raise HTTPException(status_code=400, detail="Invalid category_ids format")
    
    # Criar objeto do produto
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "category_ids": category_ids_list,
        "image_url": None
    }
    
    # Upload da imagem se fornecida
    if image:
        image_url = await request.app.s3_service.upload_file(image)
        product_data["image_url"] = image_url
    
    # Inserir produto no banco de dados
    product = jsonable_encoder(product_data)
    new_product = await request.app.mongodb["products"].insert_one(product)
    created_product = await request.app.mongodb["products"].find_one(
        {"_id": new_product.inserted_id}
    )
    return created_product


@router.put("/{id}", response_model=Product)
async def update_product(
    id: str,
    request: Request,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category_ids: Optional[str] = Form(None),  # JSON string de IDs
    image: Optional[UploadFile] = File(None)
):
    # Construir o dicionário de atualização
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if price is not None:
        update_data["price"] = price
    if category_ids is not None:
        try:
            update_data["category_ids"] = json.loads(category_ids)
        except:
            raise HTTPException(status_code=400, detail="Invalid category_ids format")
    
    # Upload da imagem se fornecida
    if image:
        image_url = await request.app.s3_service.upload_file(image)
        update_data["image_url"] = image_url
    
    # Atualizar o produto no banco de dados
    if update_data:
        update_result = await request.app.mongodb["products"].update_one(
            {"_id": id}, {"$set": update_data}
        )
        if update_result.modified_count == 0:
            # Verificar se o produto existe
            if (await request.app.mongodb["products"].find_one({"_id": id})) is None:
                raise HTTPException(status_code=404, detail=f"Product {id} not found")
    
    # Retornar o produto atualizado
    updated_product = await request.app.mongodb["products"].find_one({"_id": id})
    if updated_product is None:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")
    return updated_product


@router.get("/", response_model=List[Product])
async def list_products(request: Request):
    products = await request.app.mongodb["products"].find().to_list(1000)
    return products


@router.get("/{id}", response_model=Product)
async def get_product(id: str, request: Request):
    if (product := await request.app.mongodb["products"].find_one({"_id": id})) is not None:
        return product
    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.delete("/{id}", response_model=dict)
async def delete_product(id: str, request: Request):
    delete_result = await request.app.mongodb["products"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return {"message": f"Product {id} deleted"}
    raise HTTPException(status_code=404, detail=f"Product {id} not found")
