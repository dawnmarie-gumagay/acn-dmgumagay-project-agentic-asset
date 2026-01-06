"""
Connection Test Script
Validates Ollama Cloud API connectivity and configuration
"""
from crew import get_ollama_llm
from config import Config


def test_ollama_connection():
    """Test Ollama Cloud LLM connection"""
    print("\n" + "=" * 60)
    print("Testing Ollama Cloud Connection")
    print("=" * 60 + "\n")
    
    try:
        # Validate configuration
        print("1. Validating configuration...")
        Config.validate()
        print("   ✓ Configuration valid")
        print(f"     - Model: {Config.DEFAULT_MODEL}")
        print(f"     - Base URL: {Config.OLLAMA_BASE_URL}")
        print(f"     - API Key: {'*' * 20}{Config.OLLAMA_API_KEY[-4:]}")
        
        # Initialize LLM
        print("\n2. Initializing LLM connection...")
        llm = get_ollama_llm()
        print("   ✓ LLM instance created")
        
        # Test with a simple prompt
        print("\n3. Testing with simple prompt...")
        test_prompt = "Say 'Connection successful!' and nothing else."
        response = llm.invoke(test_prompt)
        print(f"   ✓ Response received: {response}")
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED - Connection is working!")
        print("=" * 60 + "\n")
        return True
        
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("\nPlease check your .env file and ensure:")
        print("  - OLLAMA_API_KEY is set")
        print("  - OLLAMA_BASE_URL is set")
        return False
        
    except Exception as e:
        print(f"\n✗ Connection Test Failed: {e}")
        print("\nPossible issues:")
        print("  - Invalid API key")
        print("  - Network connectivity problems")
        print("  - Ollama Cloud service unavailable")
        print("  - Model not available")
        return False


if __name__ == "__main__":
    test_ollama_connection()
