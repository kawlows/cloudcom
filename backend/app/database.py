# backend/app/database.py

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.config import settings


# Base class for ORM models
Base = declarative_base()

# Main transactional DB engine and session
engine = create_engine(
    settings.database_url,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Reporting DB engine and session (for analytics)
reporting_engine = create_engine(
    settings.reporting_database_url,
    future=True,
)

ReportingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=reporting_engine,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_reporting_db() -> Generator[Session, None, None]:
    db = ReportingSessionLocal()
    try:
        yield db
    finally:
        db.close()
