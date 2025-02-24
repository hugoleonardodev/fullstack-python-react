# backend/app/scripts/seed_data.py
import sys
import os
import asyncio
import random
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Adicionar o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Número de registros a serem criados
NUM_CATEGORIES = 5
NUM_PRODUCTS = 20
NUM_ORDERS = 10

# Categorias de exemplo
CATEGORY_NAMES = [
    "Eletrônicos", "Roupas", "Livros", "Casa e Jardim", "Esportes"
]

# Produtos de exemplo (nomes e descrições)
PRODUCT_DATA = [
    {"name": "Smartphone XYZ", "description": "Um smartphone de última geração"},
    {"name": "Laptop Ultra", "description": "Laptop leve e poderoso"},
    {"name": "Camiseta Casual", "description": "Camiseta confortável para o dia a dia"},
    {"name": "Calça Jeans", "description": "Calça jeans resistente"},
    {"name": "Clean Code", "description": "Livro sobre boas práticas de programação"},
    {"name": "Design Patterns", "description": "Livro sobre padrões de design de software"},
    {"name": "Conjunto de Panelas", "description": "Kit com 5 panelas antiaderentes"},
    {"name": "Jogo de Cama", "description": "Jogo de cama king size 100% algodão"},
    {"name": "Bola de Futebol", "description": "Bola de futebol profissional"},
    {"name": "Kit de Yoga", "description": "Kit com tapete e acessórios para yoga"},
    {"name": "Monitor 4K", "description": "Monitor de alta resolução 4K"},
    {"name": "Teclado Mecânico", "description": "Teclado mecânico para gamers"},
    {"name": "Blusa de Frio", "description": "Blusa de frio para dias frios"},
    {"name": "Bermuda", "description": "Bermuda confortável para o verão"},
    {"name": "Python Fluente", "description": "Livro sobre programação Python"},
    {"name": "JavaScript: The Good Parts", "description": "Livro sobre boas práticas em JavaScript"},
    {"name": "Cafeteira", "description": "Cafeteira elétrica programável"},
    {"name": "Ventilador", "description": "Ventilador de mesa potente e silencioso"},
    {"name": "Raquete de Tênis", "description": "Raquete de tênis profissional"},
    {"name": "Bicicleta", "description": "Bicicleta para exercícios"}
]


async def connect_with_retry():
    """Retry MongoDB connection until successful."""
    retries = 1
    delay = 5  # seconds
    for attempt in range(retries):
        try:
            client = AsyncIOMotorClient(MONGO_URI)
            await client.server_info()  # Check if MongoDB is reachable
            print("Connected to MongoDB!")
            return client
        except Exception as e:
            print(f"MongoDB connection failed ({attempt + 1}/{retries}): {e}")
            await asyncio.sleep(delay)
    raise Exception("MongoDB is not available after multiple retries.")


async def seed_database():
    # Conectar ao MongoDB
    client = await connect_with_retry()
    db = client[DB_NAME]
    
    # Limpar as coleções existentes
    await db.categories.delete_many({})
    await db.products.delete_many({})
    await db.orders.delete_many({})
    
    print("Populando categorias...")
    # Inserir categorias
    category_ids = []
    for name in CATEGORY_NAMES[:NUM_CATEGORIES]:
        result = await db.categories.insert_one({"name": name})
        category_ids.append(str(result.inserted_id))
        print(f"Categoria criada: {name}")
    
    print("\nPopulando produtos...")
    # Inserir produtos
    product_ids = []
    for i in range(min(NUM_PRODUCTS, len(PRODUCT_DATA))):
        product = PRODUCT_DATA[i]
        # Associar a 1-3 categorias aleatórias
        product_categories = random.sample(
            category_ids, 
            random.randint(1, min(3, len(category_ids)))
        )
        product_data = {
            "name": product["name"],
            "description": product["description"],
            "price": round(random.uniform(10.0, 1000.0), 2),
            "category_ids": product_categories,
            "image_url": f"http://localhost:4566/product-images/placeholder-{i+1}.jpg"
        }
        result = await db.products.insert_one(product_data)
        product_ids.append(str(result.inserted_id))
        print(f"Produto criado: {product['name']} - R$ {product_data['price']}")
    
    print("\nPopulando pedidos...")
    # Inserir pedidos
    today = datetime.now()
    for i in range(NUM_ORDERS):
        # Data entre hoje e 30 dias atrás
        order_date = today - timedelta(days=random.randint(0, 30))
        # Selecionar 1-5 produtos aleatórios
        order_products = random.sample(
            product_ids, 
            random.randint(1, min(5, len(product_ids)))
        )
        
        # Consultar os preços dos produtos para calcular o total
        total = 0
        for product_id in order_products:
            product = await db.products.find_one({"_id": product_id})
            if product:
                total += product["price"]
        
        order_data = {
            "date": order_date,
            "product_ids": order_products,
            "total": round(total, 2)
        }
        result = await db.orders.insert_one(order_data)
        print(f"Pedido criado: {result.inserted_id} - Total: R$ {order_data['total']}")
    
    print("\nPopulação do banco de dados concluída!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
