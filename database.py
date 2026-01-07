import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get database URL from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/dbname"
)

# Fix for Render's postgres:// vs postgresql:// format
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"✅ Connecting to database...")

engine = create_engine(
    DATABASE_URL, 
    echo=False,  # Set to False in production
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600  # Recycle connections after 1 hour
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()