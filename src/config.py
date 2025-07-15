import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.local")

class Settings:
    # API Configuration
    TRIPXPLO_API_BASE = "https://api.tripxplo.com/v1/api"
    TRIPXPLO_EMAIL = os.getenv("TRIPXPLO_EMAIL")
    TRIPXPLO_PASSWORD = os.getenv("TRIPXPLO_PASSWORD")
    
    # OpenRouter/OpenAI Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL = "deepseek/deepseek-chat"
    
    # FastAPI Configuration
    APP_NAME = "TripXplo AI"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS Configuration
    ALLOWED_ORIGINS = ["*"]  # In production, specify exact origins
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()

# Validate required environment variables
if not settings.TRIPXPLO_EMAIL or not settings.TRIPXPLO_PASSWORD:
    raise ValueError("TRIPXPLO_EMAIL and TRIPXPLO_PASSWORD must be set in environment variables")

if not settings.OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY must be set in environment variables")