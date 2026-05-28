# backend/app/reporting_models.py

from sqlalchemy import Column, Date, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class DailySales(Base):
    __tablename__ = "daily_sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, nullable=False)
    total_orders = Column(Integer, nullable=False)
    total_revenue = Column(Numeric(12, 2), nullable=False)
    total_items = Column(Integer, nullable=False)


class TopProductDaily(Base):
    __tablename__ = "top_product_daily"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    total_quantity = Column(Integer, nullable=False)
    total_revenue = Column(Numeric(12, 2), nullable=False)
