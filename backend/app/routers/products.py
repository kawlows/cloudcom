# backend/app/routers/products.py

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("", response_model=List[dict])
def list_products(
    q: Optional[str] = Query(None, description="Search query"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Product)

    if q:
        ilike_pattern = f"%{q}%"
        query = query.filter(models.Product.name.ilike(ilike_pattern))

    products = query.order_by(models.Product.id).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "stock": p.stock,
            "is_active": p.is_active,
            "created_at": p.created_at,
        }
        for p in products
    ]


@router.get("/{product_id}", response_model=dict)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    p = (
        db.query(models.Product)
        .filter(models.Product.id == product_id)
        .first()
    )
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": float(p.price),
        "stock": p.stock,
        "is_active": p.is_active,
        "created_at": p.created_at,
    }
