"""Database session configuration."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import (
    SQLALCHEMY_DATABASE_URL,
    SQLALCHEMY_ECHO,
    SQLALCHEMY_POOL_SIZE,
    SQLALCHEMY_MAX_OVERFLOW,
    SQLALCHEMY_POOL_RECYCLE,
    SQLALCHEMY_POOL_PRE_PING,
)

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=SQLALCHEMY_ECHO,
    pool_size=SQLALCHEMY_POOL_SIZE,
    max_overflow=SQLALCHEMY_MAX_OVERFLOW,
    pool_recycle=SQLALCHEMY_POOL_RECYCLE,
    pool_pre_ping=SQLALCHEMY_POOL_PRE_PING,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables():
    """Create all tables in database."""
    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    """Drop all tables from database (FOR TESTING ONLY)."""
    Base.metadata.drop_all(bind=engine)
