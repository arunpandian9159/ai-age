import os
from dotenv import load_dotenv

# Load environment variables
import logging
logger = logging.getLogger(__name__)

# Try to load from .env.local first, then .env
env_files = [".env.local", ".env"]
env_loaded = False

for env_file in env_files:
    if load_dotenv(env_file):
        logger.info(f"Loaded environment variables from {env_file}")
        env_loaded = True
        break

if not env_loaded:
    logger.warning("No environment file found. Using system environment variables.")

class Settings:
    # API Configuration
    TRIPXPLO_API_BASE = "https://api.tripxplo.com/v1/api"
    TRIPXPLO_EMAIL = os.getenv("TRIPXPLO_EMAIL")
    TRIPXPLO_PASSWORD = os.getenv("TRIPXPLO_PASSWORD")
    
    # OpenRouter/OpenAI Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324"
    
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