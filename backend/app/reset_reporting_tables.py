# backend/app/reset_reporting_tables.py
from sqlalchemy import text

from backend.app.database import reporting_engine


def reset_reporting_tables():
    with reporting_engine.connect() as conn:
        # Drop tables if they exist
        conn.execute(text("DROP TABLE IF EXISTS top_product_daily CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS daily_sales CASCADE;"))
        conn.commit()
        print("Dropped daily_sales and top_product_daily tables")


if __name__ == "__main__":
    reset_reporting_tables()