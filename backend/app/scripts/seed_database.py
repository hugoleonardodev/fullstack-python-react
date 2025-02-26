import os
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import random

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def seed_database():
    # Clear existing collections
    db.categories.delete_many({})
    db.products.delete_many({})
    db.orders.delete_many({})
    
    print("Creating categories...")
    categories = [
        {"_id": ObjectId(), "name": "Eletrônicos"},
        # {"_id": ObjectId(), "name": "Móveis"},
        {"_id": ObjectId(), "name": "Livros"},
        {"_id": ObjectId(), "name": "Roupas"},
        # {"_id": ObjectId(), "name": "Alimentos"}
    ]
    db.categories.insert_many(categories)
    
    print("Creating products...")
    products = []
    
    # Electronics products
    for i in range(3):
        products.append({
            "_id": ObjectId(),
            "name": f"Produto Eletrônico {i+1}",
            "description": f"Descrição do produto eletrônico {i+1}",
            "price": round(random.uniform(100, 5000), 2),
            "category_ids": [categories[0]["_id"]],
            "image_url": f"https://example.com/images/electronics/{i+1}.jpg"
        })
    
    # # Furniture products
    # for i in range(3):
    #     products.append({
    #         "_id": ObjectId(),
    #         "name": f"Móvel {i+1}",
    #         "description": f"Descrição do móvel {i+1}",
    #         "price": round(random.uniform(200, 3000), 2),
    #         "category_ids": [categories[1]["_id"]],
    #         "image_url": f"https://example.com/images/furniture/{i+1}.jpg"
    #     })
    
    # Books
    for i in range(3):
        products.append({
            "_id": ObjectId(),
            "name": f"Livro {i+1}",
            "description": f"Descrição do livro {i+1}",
            "price": round(random.uniform(20, 150), 2),
            "category_ids": [categories[1]["_id"]],
            "image_url": f"https://example.com/images/books/{i+1}.jpg"
        })
    
    # Clothes
    for i in range(3):
        products.append({
            "_id": ObjectId(),
            "name": f"Roupa {i+1}",
            "description": f"Descrição da roupa {i+1}",
            "price": round(random.uniform(50, 500), 2),
            "category_ids": [categories[2]["_id"]],
            "image_url": f"https://example.com/images/clothes/{i+1}.jpg"
        })
    
    # # Food
    # for i in range(3):
    #     products.append({
    #         "_id": ObjectId(),
    #         "name": f"Alimento {i+1}",
    #         "description": f"Descrição do alimento {i+1}",
    #         "price": round(random.uniform(5, 100), 2),
    #         "category_ids": [categories[4]["_id"]],
    #         "image_url": f"https://example.com/images/food/{i+1}.jpg"
    #     })
    
    # # Multi-category products
    # for i in range(3):
    #     random_categories = random.sample([cat["_id"] for cat in categories], 2)
    #     products.append({
    #         "_id": ObjectId(),
    #         "name": f"Produto Multi-categoria {i+1}",
    #         "description": f"Produto que pertence a múltiplas categorias {i+1}",
    #         "price": round(random.uniform(100, 1000), 2),
    #         "category_ids": random_categories,
    #         "image_url": f"https://example.com/images/multi/{i+1}.jpg"
    #     })
    
    db.products.insert_many(products)
    
    print("Creating orders...")
    orders = []
    
    # Generate 50 random orders over the last 30 days
    for i in range(12):
        # Random date in the last 30 days
        order_date = datetime.now() - timedelta(days=random.randint(0, 30))
        
        # Select 1-5 random products
        products_from_db = list(db.products.aggregate([
            {"$sample": {"size": random.randint(1, 5)}}
        ]))
        print("products_from_db", products_from_db)
        # order_products = random.sample(products_from_db, random.randint(1, 5))
        product_ids = [str(p["_id"]) for p in products_from_db]
        
        category_ids = [str(p["category_ids"][0]) for p in products_from_db]

        print("product_ids", product_ids)
        # Calculate total
        total = sum(p["price"] for p in products_from_db)
        
        print("total", total)
        
        orders.append({
            "_id": ObjectId(),
            "date": order_date,
            "product_ids": product_ids,
            "category_ids": category_ids,
            "total": round(total, 2)
        })
    
    db.orders.insert_many(orders)
    
    print("Database seeded successfully!")
    print("\nCategory IDs for frontend reference:")
    for category in categories:
        print(f"{category['name']}: {category['_id']}")


if __name__ == "__main__":
    seed_database()