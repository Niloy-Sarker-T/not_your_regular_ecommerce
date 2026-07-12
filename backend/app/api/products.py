from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=schemas.ProductList)
def products(
    q: str | None = None,
    category: str | None = None,
    limit: int = Query(default=24, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    items, total = crud.list_products(db, q=q, category=category, limit=limit, offset=offset)
    return schemas.ProductList(items=items, total=total, limit=limit, offset=offset)


@router.get("/{product_id}", response_model=schemas.ProductOut)
def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
