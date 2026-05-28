# etl/etl_config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adjust paths as needed if you move config
from backend.app.config import settings

# Main transactional DB (same as backend)
main_engine = create_engine(settings.DATABASE_URL, future=True)
MainSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=main_engine)

# Reporting DB
reporting_engine = create_engine(settings.REPORTING_DATABASE_URL, future=True)
ReportingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=reporting_engine
)