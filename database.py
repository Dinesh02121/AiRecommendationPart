import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable is not set")

# Fix for Render's postgres:// vs postgresql:// format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Add SSL mode for Supabase if not already present
if "supabase" in DATABASE_URL and "sslmode" not in DATABASE_URL:
    separator = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL += f"{separator}sslmode=require"

print(f"✅ Connecting to Supabase database...")

# Create engine with Supabase-optimized settings
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,          
    pool_recycle=300,             
    pool_size=5,                 
    max_overflow=10,             
    connect_args={
        "connect_timeout": 10,    
        "keepalives": 1,          
        "keepalives_idle": 30,
        "keepalives_interval": 10, # Seconds between keepalives
        "keepalives_count": 5,    # Number of keepalives before disconnect
    }
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
