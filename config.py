import os
from dotenv import load_dotenv

# Load variables from your .env file
load_dotenv()

# Load and Clean Environment Variables
# .strip() is used to remove any accidental whitespace from the .env file
AZURE_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "").strip()
AZURE_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "").strip()
AZURE_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "").strip()
AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME", "").strip()
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "").strip()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "").strip()

# Validation Step
def validate_config():
    """Checks if critical Azure variables are loaded."""
    if not all([AZURE_ENDPOINT, AZURE_KEY, AZURE_API_VERSION, AZURE_DEPLOYMENT_NAME]):
        raise ValueError(
            "Azure configuration is missing! Please ensure your .env file is in the project root "
            "and contains all required AZURE_* variables."
        )
    print("Configuration loaded and validated successfully.")