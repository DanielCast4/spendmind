from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL format: postgresql://username:password@host/database_name
DATABASE_URL = "postgresql://username:password@localhost/expense_manager"

# Create the SQLAlchemy engine to manage connections to the PostgreSQL database
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

# Base class for all ORM models to inherit from
Base = declarative_base()

def get_db():
    """
    Provides a database session for interacting with the database.

    This function is typically used as a dependency in frameworks like FastAPI.
    It yields a database session and ensures it is closed after use.

    Yields:
        Session: SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
