import re

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app import models


def list_products(db: Session, q: str | None = None, category: str | None = None, limit: int = 24, offset: int = 0):
    stmt = select(models.Product)
    count_stmt = select(func.count(models.Product.id))

    filters = []
    if q:
        needle = f"%{q.strip()}%"
        filters.append(
            or_(
                models.Product.name.ilike(needle),
                models.Product.brand.ilike(needle),
                models.Product.category.ilike(needle),
                models.Product.description.ilike(needle),
            )
        )
    if category:
        filters.append(models.Product.category.ilike(f"%{category.strip()}%"))

    for condition in filters:
        stmt = stmt.where(condition)
        count_stmt = count_stmt.where(condition)

    stmt = stmt.order_by(models.Product.name).limit(limit).offset(offset)
    return db.scalars(stmt).all(), db.scalar(count_stmt) or 0


def get_product(db: Session, product_id: int):
    return db.get(models.Product, product_id)


def search_first_product(db: Session, name: str | None):
    if not name:
        return None
    products, _ = list_products(db, q=name, limit=1)
    if products:
        return products[0]

    tokens = {token.rstrip("s") for token in re.findall(r"[a-z0-9]+", name.lower()) if len(token) > 2}
    if not tokens:
        return None

    candidates = db.scalars(select(models.Product)).all()
    scored = []
    for product in candidates:
        haystack = f"{product.name} {product.brand} {product.category}".lower()
        score = sum(1 for token in tokens if token in haystack)
        if score:
            scored.append((score, product))
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[0][1] if scored else None


def cart_summary(db: Session):
    items = db.scalars(select(models.CartItem).order_by(models.CartItem.id)).all()
    total = sum(item.quantity * item.product.price for item in items)
    item_count = sum(item.quantity for item in items)
    return items, round(total, 2), item_count


def add_to_cart(db: Session, product: models.Product, quantity: int):
    quantity = max(1, quantity)
    item = db.scalar(select(models.CartItem).where(models.CartItem.product_id == product.id))
    if item:
        item.quantity = min(product.stock, item.quantity + quantity)
    else:
        item = models.CartItem(product_id=product.id, quantity=min(product.stock, quantity))
        db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_cart_quantity(db: Session, product_id: int, quantity: int):
    item = db.scalar(select(models.CartItem).where(models.CartItem.product_id == product_id))
    if not item:
        return None
    if quantity <= 0:
        db.delete(item)
        db.commit()
        return None
    item.quantity = min(item.product.stock, quantity)
    db.commit()
    db.refresh(item)
    return item


def remove_from_cart(db: Session, product_id: int):
    item = db.scalar(select(models.CartItem).where(models.CartItem.product_id == product_id))
    if item:
        db.delete(item)
        db.commit()
    return item


def clear_cart(db: Session):
    for item in db.scalars(select(models.CartItem)).all():
        db.delete(item)
    db.commit()
