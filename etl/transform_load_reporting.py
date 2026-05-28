# etl/transform_load_reporting.py

from typing import Any, Dict, List, Tuple
from datetime import date

from sqlalchemy.orm import Session

from .etl_config import MainSessionLocal, ReportingSessionLocal
from .extract_transactions import extract_orders_since
from backend.app.reporting_models import DailySales, TopProductDaily


def aggregate_daily_sales(orders: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Returns a dict keyed by date string (YYYY-MM-DD) with aggregated metrics
    for DailySales.
    """
    daily: Dict[str, Dict[str, Any]] = {}

    for order in orders:
        order_date = order["created_at"].date()
        date_key = order_date.isoformat()

        if date_key not in daily:
            daily[date_key] = {
                "date": order_date,
                "total_orders": 0,
                "total_items": 0,
                "total_revenue": 0.0,
            }

        daily[date_key]["total_orders"] += 1
        daily[date_key]["total_revenue"] += order["total_amount"]

        for item in order["items"]:
            daily[date_key]["total_items"] += item["quantity"]

    return daily


def aggregate_top_products_daily(
    orders: List[Dict[str, Any]]
) -> Dict[Tuple[date, int], Dict[str, Any]]:
    """
    Returns a dict keyed by (date, product_id) with aggregated metrics
    for TopProductDaily.
    """
    products: Dict[Tuple[date, int], Dict[str, Any]] = {}

    for order in orders:
        order_date = order["created_at"].date()

        for item in order["items"]:
            key = (order_date, item["product_id"])

            if key not in products:
                products[key] = {
                    "date": order_date,
                    "product_id": item["product_id"],
                    "product_name": item["product_name"],
                    "total_quantity": 0,
                    "revenue": 0.0,
                }

            products[key]["total_quantity"] += item["quantity"]
            products[key]["revenue"] += item["line_total"]

    return products


def load_daily_sales(db: Session, daily: Dict[str, Dict[str, Any]]) -> None:
    """
    Upsert aggregated daily sales into the DailySales table.
    """
    for _, data in daily.items():
        existing = (
            db.query(DailySales)
            .filter(DailySales.date == data["date"])
            .first()
        )

        if existing:
            existing.total_orders = data["total_orders"]
            existing.total_items = data["total_items"]
            existing.total_revenue = data["total_revenue"]
        else:
            row = DailySales(
                date=data["date"],
                total_orders=data["total_orders"],
                total_items=data["total_items"],
                total_revenue=data["total_revenue"],
            )
            db.add(row)


def load_top_products_daily(
    db: Session, products: Dict[Tuple[date, int], Dict[str, Any]]
) -> None:
    """
    Upsert aggregated per-day per-product metrics into TopProductDaily.
    """
    for _, data in products.items():
        existing = (
            db.query(TopProductDaily)
            .filter(
                TopProductDaily.date == data["date"],
                TopProductDaily.product_id == data["product_id"],
            )
            .first()
        )

        if existing:
            existing.product_name = data["product_name"]
            existing.total_quantity = data["total_quantity"]
            existing.revenue = data["revenue"]
        else:
            row = TopProductDaily(
                date=data["date"],
                product_id=data["product_id"],
                product_name=data["product_name"],
                total_quantity=data["total_quantity"],
                revenue=data["revenue"],
            )
            db.add(row)


def main() -> None:
    # Extract from main DB
    main_db = MainSessionLocal()
    try:
        orders = extract_orders_since(main_db)
        print(f"ETL: extracted {len(orders)} orders.")
    finally:
        main_db.close()

    # Aggregate in memory
    daily = aggregate_daily_sales(orders)
    top_products = aggregate_top_products_daily(orders)

    # Load into reporting DB
    rep_db = ReportingSessionLocal()
    try:
        load_daily_sales(rep_db, daily)
        load_top_products_daily(rep_db, top_products)
        rep_db.commit()
        print("Reporting tables updated.")
    except Exception:
        rep_db.rollback()
        raise
    finally:
        rep_db.close()


if __name__ == "__main__":
    main()