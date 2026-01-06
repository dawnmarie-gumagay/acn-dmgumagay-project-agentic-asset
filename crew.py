"""
Ollama Cloud LLM Connection Factory
Provides LLM instances for CrewAI agents
"""
import os
from langchain_community.llms import Ollama
from config import Config


def get_ollama_llm(model=None):
    """
    Initialize Ollama Cloud LLM connection
    
    Args:
        model (str): Model name to use. Defaults to Config.DEFAULT_MODEL
        
    Returns:
        Ollama: Configured LLM instance
    """
    if model is None:
        model = Config.DEFAULT_MODEL
    
    return Ollama(
        base_url=Config.OLLAMA_BASE_URL,
        model=model,
        headers={
            "Authorization": f"Bearer {Config.OLLAMA_API_KEY}"
        }
    )


if __name__ == "__main__":
    # Test LLM connection
    try:
        Config.validate()
        print("Initializing Ollama Cloud connection...")
        llm = get_ollama_llm()
        print(f"✓ Ollama Cloud connection initialized successfully")
        print(f"  Model: {Config.DEFAULT_MODEL}")
        print(f"  Base URL: {Config.OLLAMA_BASE_URL}")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
