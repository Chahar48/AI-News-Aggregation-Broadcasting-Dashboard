# backend/app/models/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

from app.config import get_settings

# -------------------------------------------------
# Load environment settings
# -------------------------------------------------
settings = get_settings()

# -------------------------------------------------
# SQLAlchemy Base
# -------------------------------------------------
Base = declarative_base()

# -------------------------------------------------
# Database Engine
# -------------------------------------------------
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,   # safe for dev + containers
    echo=False,
    future=True,
)

# -------------------------------------------------
# Session Factory
# -------------------------------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)

# -------------------------------------------------
# Dependency
# -------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# Schema initialization (DEV ONLY)
# -------------------------------------------------
def init_db():
    """
    Create all tables.
    Should be called ONCE on app startup.
    """
    from app.models import orm_models  # IMPORTANT: load models
    Base.metadata.create_all(bind=engine)
