from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services.serializers import serialize_cart

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=schemas.CartOut)
def get_cart(db: Session = Depends(get_db)):
    return serialize_cart(*crud.cart_summary(db))


@router.post("", response_model=schemas.CartOut)
def add_item(payload: schemas.CartAdd, db: Session = Depends(get_db)):
    product = crud.get_product(db, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock <= 0:
        raise HTTPException(status_code=400, detail="Product is out of stock")
    crud.add_to_cart(db, product, payload.quantity)
    return serialize_cart(*crud.cart_summary(db))


@router.patch("/{product_id}", response_model=schemas.CartOut)
def update_item(product_id: int, payload: schemas.CartUpdate, db: Session = Depends(get_db)):
    crud.update_cart_quantity(db, product_id, payload.quantity)
    return serialize_cart(*crud.cart_summary(db))


@router.delete("/{product_id}", response_model=schemas.CartOut)
def remove_item(product_id: int, db: Session = Depends(get_db)):
    crud.remove_from_cart(db, product_id)
    return serialize_cart(*crud.cart_summary(db))


@router.post("/checkout", response_model=schemas.CheckoutOut)
def checkout(db: Session = Depends(get_db)):
    _, total, item_count = crud.cart_summary(db)
    if item_count == 0:
        raise HTTPException(status_code=400, detail="Cart is empty")
    crud.clear_cart(db)
    return schemas.CheckoutOut(message="Checkout complete. Thanks for shopping!", total=total, item_count=item_count)
