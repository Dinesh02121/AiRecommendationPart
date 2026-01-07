import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY is missing from environment variables")

print(f"✅ Environment: {ENVIRONMENT}")
print(f"✅ API Key loaded: {bool(OPENAI_API_KEY)}")
print(f"✅ API Key prefix: {OPENAI_API_KEY[:10]}..." if OPENAI_API_KEY else "❌ No API key")