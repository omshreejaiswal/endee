import os
import warnings
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Warn if API key is not set
if not GROQ_API_KEY:
    warnings.warn(
        "GROQ_API_KEY not found in .env file. "
        "API calls will use fallback demo responses. "
        "Please set GROQ_API_KEY in your .env file for full functionality. "
        "Get one at: https://console.groq.com/",
        RuntimeWarning
    )

# Endee Vector Database Configuration
ENDEE_HOST = os.getenv("ENDEE_HOST", "http://localhost:19530")
ENDEE_USE_FALLBACK = os.getenv("ENDEE_USE_FALLBACK", "true").lower() == "true"

# Application Configuration
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
