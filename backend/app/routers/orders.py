# backend/app/routers/orders.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_active_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/checkout",
    response_model=schemas.OrderRead,
    status_code=status.HTTP_201_CREATED,
)
def checkout(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    cart_items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == current_user.id)
        .all()
    )
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty.")

    total_amount = 0.0
    for item in cart_items:
        if not item.product or not item.product.is_active:
            raise HTTPException(
                status_code=400,
                detail=f"Product {item.product_id} is not available.",
            )
        if item.quantity > item.product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {item.product_id}.",
            )
        total_amount += float(item.product.price) * item.quantity

    order = models.Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status="pending",
    )
    db.add(order)
    db.flush()  # get order.id before committing

    order_items = []
    for item in cart_items:
        product = item.product
        # decrement stock
        product.stock -= item.quantity

        oi = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            line_total=float(product.price) * item.quantity,
        )
        db.add(oi)
        order_items.append(oi)

    # Clear cart
    db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).delete()

    db.commit()
    db.refresh(order)

    # attach items for response
    order.items = order_items
    return order


@router.get("/", response_model=List[schemas.OrderRead])
def list_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.id)
        .order_by(models.Order.created_at.desc())
        .all()
    )
    return orders


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    order = (
        db.query(models.Order)
        .filter(
            models.Order.id == order_id,
            models.Order.user_id == current_user.id,
        )
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order