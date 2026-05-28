# etl/extract_transactions.py
from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from .etl_config import MainSessionLocal
from backend.app import models


def extract_orders_since(
    db: Session,
    since: datetime | None = None,
) -> List[Dict[str, Any]]:
    """
    Extract orders with their items, user, and products.

    If 'since' is provided, filter orders created_at >= since.
    """
    query = db.query(models.Order).join(models.User).options()

    if since is not None:
        query = query.filter(models.Order.created_at >= since)

    orders = query.all()

    results: List[Dict[str, Any]] = []

    for order in orders:
        order_dict: Dict[str, Any] = {
            "id": order.id,
            "user_id": order.user_id,
            "user_email": order.user.email,
            "user_full_name": order.user.full_name,
            "total_amount": float(order.total_amount),
            "status": order.status,
            "created_at": order.created_at,
            "items": [],
        }

        for item in order.items:
            order_dict["items"].append(
                {
                    "product_id": item.product_id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price),
                    "line_total": float(item.line_total),
                }
            )

        results.append(order_dict)

    return results


def main():
    db = MainSessionLocal()
    try:
        orders = extract_orders_since(db)  # full extract for now
        print(f"Extracted {len(orders)} orders.")
        # For debugging you could write to a JSON file, but for our pipeline
        # we'll call extract_orders_since() directly from transform_load_reporting.py
    finally:
        db.close()


if __name__ == "__main__":
    main()