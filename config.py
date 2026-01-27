"""
Configuration Management for CrewAI DevOps Automation
Centralized settings for the agentic solution
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration class for the application"""

    # Ollama Cloud Settings
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "https://api.ollama.cloud")

    # Model Configuration
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama2:7b")

    # Logging Configuration
    VERBOSE_LEVEL = int(os.getenv("VERBOSE_LEVEL", "2"))
    LOG_FILE = "crew_execution.log"

    # Output Configuration
    OUTPUT_DIR = "outputs"

    # Agent Configuration
    ALLOW_DELEGATION = False

    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.OLLAMA_API_KEY:
            raise ValueError("OLLAMA_API_KEY is not set in .env file")
        if not Config.OLLAMA_BASE_URL:
            raise ValueError("OLLAMA_BASE_URL is not set in .env file")
        return True


if __name__ == "__main__":
    # Test configuration
    try:
        Config.validate()
        print("✓ Configuration validated successfully")
        print(f"  Model: {Config.DEFAULT_MODEL}")
        print(f"  Base URL: {Config.OLLAMA_BASE_URL}")
        print(f"  Output Dir: {Config.OUTPUT_DIR}")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
