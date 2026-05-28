# backend/app/routers/analytics.py
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database import get_reporting_db
from backend.app.reporting_models import DailySales, TopProductDaily

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("/daily-sales", response_model=list[dict])
def get_daily_sales(
    start_date: date = Query(..., description="Start date (inclusive)"),
    end_date: date = Query(..., description="End date (inclusive)"),
    db: Session = Depends(get_reporting_db),
):
    rows: List[DailySales] = (
        db.query(DailySales)
        .filter(DailySales.date >= start_date, DailySales.date <= end_date)
        .order_by(DailySales.date)
        .all()
    )

    return [
        {
            "date": row.date,
            "total_orders": row.total_orders,
            "total_revenue": float(row.total_revenue),
            "total_items": row.total_items,
        }
        for row in rows
    ]


@router.get("/top-products", response_model=list[dict])
def get_top_products(
    target_date: date = Query(..., description="Date to get top products for"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_reporting_db),
):
    rows: List[TopProductDaily] = (
        db.query(TopProductDaily)
        .filter(TopProductDaily.date == target_date)
        .order_by(TopProductDaily.total_quantity.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "product_id": row.product_id,
            "product_name": row.product_name,
            "total_quantity": row.total_quantity,
            "revenue": float(row.revenue),
        }
        for row in rows
    ]