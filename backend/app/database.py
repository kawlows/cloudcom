# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# Main transactional DB
engine = create_engine(settings.DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Reporting DB (analytics)
reporting_engine = create_engine(settings.REPORTING_DATABASE_URL, future=True)
ReportingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=reporting_engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_reporting_db():
    db = ReportingSessionLocal()
    try:
        yield db
    finally:
        db.close()