from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.recommend import router
from database import engine
from models import Base
import os

app = FastAPI(title="AI Project Recommendation Service")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

# Parse multiple origins
allowed_origins = []

# Add frontend URLs
if FRONTEND_URL:
    if "," in FRONTEND_URL:
        allowed_origins.extend([url.strip() for url in FRONTEND_URL.split(",")])
    else:
        allowed_origins.append(FRONTEND_URL)

# Add backend URL
if BACKEND_URL:
    allowed_origins.append(BACKEND_URL)

# For development only
if os.getenv("ENVIRONMENT") == "development":
    allowed_origins.extend([
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
    ])

print(f"✅ CORS Allowed Origins: {allowed_origins}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    print("🚀 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

# Include API routes
app.include_router(router, prefix="/api/ai")

@app.get("/")
def read_root():
    return {
        "status": "AI Project Recommendation Service is running",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ai-recommendation"}