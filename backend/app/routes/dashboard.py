import os
from fastapi import APIRouter, Body, HTTPException, status
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from ..models.base import PyObjectId

router = APIRouter()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# MongoDB connection (replace with your actual connection)
client = MongoClient(MONGO_URI)
db = client[DB_NAME]


class CategoryFilter(BaseModel):
    category: str

@router.get("/", response_model=dict)
async def get_dashboard_stats():
    return {
        'hello': 'dashboard'
    }


@router.post("/orders-by-category", response_description="Get orders by category ID")
async def get_orders_by_category(category_filter: CategoryFilter = Body(...)):
    # try:
    # Convert string ID to ObjectId
    # try:
    category_id = PyObjectId(category_filter.category)
    # except Exception:
    #     raise HTTPException(status_code=400, detail="Invalid category ID format")
    
    # Verify category exists
    category = db.categories.find_one({"_id": category_id})
    if not category:
        raise HTTPException(status_code=404, detail=f"Category with ID '{category_filter.category}' not found")
    
    pipeline = [
        {
            "$addFields": {
                "objectIdProductIds": {
                    "$map": {
                        "input": "$product_ids",
                        "as": "id",
                        "in": { "$toObjectId": "$$id" }
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "objectIdProductIds",
                "foreignField": "_id",
                "as": "product_details"
            }
        },
        # {
        #     "$match": {
        #         "product_details.category_ids": { "$in": [category_obj_id] }
        #     }
        # },
        {
            "$project": {
                "_id": 1,
                "date": 1,
                "product_ids": 1,
                "total": 1,
                "product_details": 1
            }
        },
        {
            "$match": {
                "product_details.category_ids": category_filter.category
            }
        },
    ]
    
    # Execute the aggregation pipeline
    result = list(db.orders.aggregate(pipeline))
    
    # Return the results with count
    return {
        "category_id": str(category_filter.category),
        "category_name": category["name"],
        "total_orders": len(result),
        "orders": result
    }
        
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
   