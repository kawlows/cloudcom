# backend/create_reporting_tables.py
from app.reporting_models import create_reporting_tables

if __name__ == "__main__":
    create_reporting_tables()
    print("Reporting tables created.")