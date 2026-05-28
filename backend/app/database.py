# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.app.config import settings


engine = create_engine(
    settings.database_url,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
