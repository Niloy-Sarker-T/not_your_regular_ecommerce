import random
import sys
import time
from pathlib import Path

import requests
from sqlalchemy import delete

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import Product  # noqa: E402


TERMS = [
    "shampoo",
    "soap",
    "toothpaste",
    "snacks",
    "beverages",
    "biscuits",
    "noodles",
    "cooking oil",
    "yogurt",
    "milk",
    "chips",
    "cola",
    "hand wash",
    "chocolate",
    "cereal",
]

CATEGORY_HINTS = {
    "shampoo": "Personal Care",
    "soap": "Soap",
    "toothpaste": "Toothpaste",
    "snacks": "Snacks",
    "beverages": "Beverages",
    "biscuits": "Biscuits",
    "noodles": "Noodles",
    "cooking oil": "Cooking Oil",
    "yogurt": "Dairy",
    "milk": "Dairy",
    "chips": "Snacks",
    "cola": "Beverages",
    "hand wash": "Personal Care",
    "chocolate": "Snacks",
    "cereal": "Breakfast",
}


def fetch_products(term: str, page_size: int = 25) -> list[dict]:
    for attempt in range(3):
        try:
            response = requests.get(
                "https://world.openfoodfacts.org/cgi/search.pl",
                params={
                    "search_terms": term,
                    "search_simple": 1,
                    "action": "process",
                    "json": 1,
                    "page_size": page_size,
                    "fields": "product_name,brands,categories,image_front_url,image_url,generic_name,quantity",
                },
                headers={"User-Agent": "smart-ecommerce-demo/1.0"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json().get("products", [])
        except requests.RequestException as exc:
            if attempt == 2:
                print(f"Skipping {term}: {exc}")
                return []
            time.sleep(1 + attempt)
    return []


def normalize(product: dict, term: str, rng: random.Random) -> Product | None:
    name = (product.get("product_name") or product.get("generic_name") or "").strip()
    if len(name) < 3:
        return None

    brand = (product.get("brands") or "Generic").split(",")[0].strip() or "Generic"
    image_url = product.get("image_front_url") or product.get("image_url") or ""
    categories = product.get("categories") or CATEGORY_HINTS.get(term, "Grocery")
    category = CATEGORY_HINTS.get(term) or categories.split(",")[0].strip() or "Grocery"
    quantity = product.get("quantity")
    description = f"{brand} {name}"
    if quantity:
        description += f" ({quantity})"

    return Product(
        name=name[:220],
        brand=brand[:160],
        category=category[:120],
        description=description,
        price=round(rng.uniform(1.5, 24.0), 2),
        stock=rng.randint(5, 50),
        image_url=image_url,
    )


def main() -> None:
    Base.metadata.create_all(bind=engine)
    rng = random.Random(2026)
    seen: set[str] = set()
    products: list[Product] = []

    for term in TERMS:
        print(f"Fetching {term}...")
        for raw in fetch_products(term):
            product = normalize(raw, term, rng)
            if not product:
                continue
            key = f"{product.brand.lower()}::{product.name.lower()}"
            if key in seen:
                continue
            seen.add(key)
            products.append(product)
            if len(products) >= 240:
                break
        if len(products) >= 240:
            break

    with SessionLocal() as db:
        db.execute(delete(Product))
        db.add_all(products)
        db.commit()

    print(f"Imported {len(products)} products into SQLite.")


if __name__ == "__main__":
    main()
