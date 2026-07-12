# from random import Random

# from sqlalchemy import select
# from sqlalchemy.orm import Session

# from app.models import Product


# DEMO_PRODUCTS = [
#     ("Dove Daily Moisture Shampoo", "Dove", "Personal Care", "Gentle moisturizing shampoo for everyday hair care.", "https://images.openfoodfacts.org/images/products/871/256/106/4044/front_en.3.400.jpg"),
#     ("Nivea Creme Soft Soap", "Nivea", "Soap", "Creamy cleansing soap for soft skin.", "https://images.openfoodfacts.org/images/products/400/580/881/2807/front_en.3.400.jpg"),
#     ("Colgate Total Toothpaste", "Colgate", "Toothpaste", "Fluoride toothpaste for whole mouth protection.", "https://images.openfoodfacts.org/images/products/871/478/973/2062/front_en.3.400.jpg"),
#     ("Lay's Classic Salted Chips", "Lay's", "Snacks", "Crispy salted potato chips.", "https://images.openfoodfacts.org/images/products/002/840/005/8916/front_en.31.400.jpg"),
#     ("Coca-Cola Original Taste", "Coca-Cola", "Beverages", "Sparkling cola soft drink.", "https://images.openfoodfacts.org/images/products/544/900/000/0996/front_en.532.400.jpg"),
#     ("Oreo Original Biscuits", "Oreo", "Biscuits", "Chocolate sandwich biscuits with vanilla creme.", "https://images.openfoodfacts.org/images/products/762/221/044/9283/front_en.459.400.jpg"),
#     ("Maggi 2-Minute Noodles", "Maggi", "Noodles", "Instant noodles with masala seasoning.", "https://images.openfoodfacts.org/images/products/890/105/884/6313/front_en.23.400.jpg"),
#     ("Bertolli Olive Oil", "Bertolli", "Cooking Oil", "Extra virgin olive oil for cooking and dressing.", "https://images.openfoodfacts.org/images/products/800/247/002/4089/front_en.23.400.jpg"),
#     ("Danone Natural Yogurt", "Danone", "Dairy", "Plain natural yogurt.", "https://images.openfoodfacts.org/images/products/303/349/000/4521/front_en.89.400.jpg"),
#     ("Lifebuoy Hand Wash", "Lifebuoy", "Personal Care", "Antibacterial liquid hand wash.", "https://images.openfoodfacts.org/images/products/871/256/124/9724/front_en.11.400.jpg"),
#     ("Pepsi Cola", "Pepsi", "Beverages", "Refreshing cola drink.", "https://images.openfoodfacts.org/images/products/406/080/010/3338/front_en.74.400.jpg"),
#     ("Ritz Crackers", "Ritz", "Biscuits", "Buttery round snack crackers.", "https://images.openfoodfacts.org/images/products/762/221/010/0764/front_en.215.400.jpg"),
# ]


# def seed_demo_products(db: Session) -> None:
#     has_products = db.scalar(select(Product.id).limit(1))
#     if has_products:
#         return

#     rng = Random(42)
#     for index, (name, brand, category, description, image_url) in enumerate(DEMO_PRODUCTS, start=1):
#         db.add(
#             Product(
#                 name=name,
#                 brand=brand,
#                 category=category,
#                 description=description,
#                 price=round(rng.uniform(2.0, 18.0), 2),
#                 stock=rng.randint(5, 50),
#                 image_url=image_url,
#             )
#         )
#     db.commit()



import json
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models import Product

DATA_FILE = Path(__file__).resolve().parent.parent / "products.json"


def seed_demo_products(db: Session) -> None:
    # Delete all existing products
    db.execute(delete(Product))
    db.commit()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    for p in products:
        db.add(
            Product(
                name=p["name"],
                brand=p["brand"],
                category=p["category"],
                description=p["description"],
                price=p["price"],
                stock=p["stock"],
                image_url=p["image_url"],
            )
        )

    db.commit()

    print(f"Seeded {len(products)} products.")