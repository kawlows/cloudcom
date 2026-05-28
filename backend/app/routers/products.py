# backend/app/routers/products.py
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_active_user

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[schemas.ProductRead])
def list_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    q: Optional[str] = None,
):
    query = db.query(models.Product).filter(models.Product.is_active.is_(True))
    if q:
        query = query.filter(models.Product.name.ilike(f"%{q}%"))
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product)
        .filter(models.Product.id == product_id, models.Product.is_active.is_(True))
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product


@router.post(
    "/", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED
)
def create_product(
    product_in: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    product = models.Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        stock=product_in.stock,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(
    product_id: int,
    product_in: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    # Soft delete
    product.is_active = False
    db.add(product)
    db.commit()
    return