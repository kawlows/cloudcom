# backend/app/etl_to_reporting.py
from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal, ReportingSessionLocal, reporting_engine
from backend.app import models
from backend.app.reporting_models import DailySales, TopProductDaily
from backend.app.database import Base


def init_reporting_schema():
    # Create reporting tables only in the reporting DB
    Base.metadata.create_all(bind=reporting_engine, tables=[DailySales.__table__, TopProductDaily.__table__])


def run_daily_etl(target_date: date | None = None):
    if target_date is None:
        target_date = date.today()

    main_db: Session = SessionLocal()
    reporting_db: Session = ReportingSessionLocal()

    try:
        # Ensure tables exist
        init_reporting_schema()

        # Clear existing rows for that date (idempotent ETL)
        reporting_db.query(DailySales).filter(DailySales.date == target_date).delete()
        reporting_db.query(TopProductDaily).filter(TopProductDaily.date == target_date).delete()

        # Aggregate daily sales from orders + order_items
        daily_sales_row = (
            main_db.query(
                func.count(models.Order.id).label("total_orders"),
                func.coalesce(func.sum(models.Order.total_amount), 0).label("total_revenue"),
                func.coalesce(func.sum(models.OrderItem.quantity), 0).label("total_items"),
            )
            .join(models.OrderItem, models.OrderItem.order_id == models.Order.id)
            .filter(func.date(models.Order.created_at) == target_date)
            .one()
        )

        daily = DailySales(
            date=target_date,
            total_orders=int(daily_sales_row.total_orders or 0),
            total_revenue=daily_sales_row.total_revenue or 0,
            total_items=int(daily_sales_row.total_items or 0),
        )
        reporting_db.add(daily)

        # Top products by quantity for that day
        top_products_rows = (
            main_db.query(
                models.Product.id.label("product_id"),
                models.Product.name.label("product_name"),
                func.coalesce(func.sum(models.OrderItem.quantity), 0).label("total_quantity"),
                func.coalesce(
                    func.sum(models.OrderItem.quantity * models.OrderItem.unit_price), 0
                ).label("revenue"),
            )
            .join(models.OrderItem, models.OrderItem.product_id == models.Product.id)
            .join(models.Order, models.Order.id == models.OrderItem.order_id)
            .filter(func.date(models.Order.created_at) == target_date)
            .group_by(models.Product.id, models.Product.name)
            .order_by(func.sum(models.OrderItem.quantity).desc())
            .limit(10)
            .all()
        )

        for row in top_products_rows:
            tp = TopProductDaily(
                date=target_date,
                product_id=row.product_id,
                product_name=row.product_name,
                total_quantity=int(row.total_quantity or 0),
                revenue=row.revenue or 0,
            )
            reporting_db.add(tp)

        reporting_db.commit()
        print(f"ETL completed for {target_date}")
    except Exception as e:
        reporting_db.rollback()
        print(f"ETL failed: {e}")
        raise
    finally:
        main_db.close()
        reporting_db.close()


if __name__ == "__main__":
    run_daily_etl()