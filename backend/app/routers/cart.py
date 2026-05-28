# backend/app/routers/cart.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..deps import get_current_active_user

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=List[dict])
def get_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == current_user.id)
        .all()
    )
    result = []
    for item in items:
        result.append(
            {
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product_name": item.product.name if item.product else None,
                "product_price": float(item.product.price)
                if item.product and item.product.price is not None
                else None,
            }
        )
    return result


@router.post("/add")
def add_to_cart(
    data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product or not product.is_active:
        raise HTTPException(status_code=404, detail="Product not found.")
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive.")
    if quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail="Quantity exceeds available stock.",
        )

    item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.user_id == current_user.id,
            models.CartItem.product_id == product_id,
        )
        .first()
    )
    if item:
        new_qty = item.quantity + quantity
        if new_qty > product.stock:
            raise HTTPException(
                status_code=400, detail="Quantity exceeds available stock."
            )
        item.quantity = new_qty
    else:
        item = models.CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity,
        )
        db.add(item)

    db.commit()
    return {"detail": "Item added to cart."}


@router.post("/remove")
def remove_from_cart(
    data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    product_id = data.get("product_id")

    item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.user_id == current_user.id,
            models.CartItem.product_id == product_id,
        )
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found.")

    db.delete(item)
    db.commit()
    return {"detail": "Item removed from cart."}


@router.post("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).delete()
    db.commit()
    return {"detail": "Cart cleared."}