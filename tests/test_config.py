"""
Unit tests for configuration management
Tests Config class and environment variable handling
"""
import pytest
import os
from config import Config


class TestConfigValidation:
    """Test configuration validation"""
    
    def test_config_validate_with_valid_settings(self, mock_config):
        """Test config validation passes with valid settings"""
        assert Config.validate() == True
    
    def test_config_requires_api_key(self):
        """Test config has API key requirement"""
        from config import Config
        
        # Verify API key is checked in validate method
        original_key = Config.OLLAMA_API_KEY
        Config.OLLAMA_API_KEY = None
        
        try:
            with pytest.raises(ValueError, match="OLLAMA_API_KEY"):
                Config.validate()
        finally:
            Config.OLLAMA_API_KEY = original_key
    
    def test_config_requires_base_url(self):
        """Test config has base URL requirement"""
        from config import Config
        
        # Verify base URL is checked in validate method
        original_url = Config.OLLAMA_BASE_URL
        Config.OLLAMA_BASE_URL = None
        
        try:
            with pytest.raises(ValueError, match="OLLAMA_BASE_URL"):
                Config.validate()
        finally:
            Config.OLLAMA_BASE_URL = original_url


class TestConfigDefaults:
    """Test configuration default values"""
    
    def test_default_model(self, mock_config):
        """Test default model configuration"""
        assert Config.DEFAULT_MODEL is not None
        assert "llama" in Config.DEFAULT_MODEL.lower() or Config.DEFAULT_MODEL != ""
    
    def test_default_verbose_level(self, mock_config):
        """Test default verbose level"""
        assert Config.VERBOSE_LEVEL >= 0
        assert Config.VERBOSE_LEVEL <= 2
    
    def test_default_output_dir(self, mock_config):
        """Test default output directory"""
        assert Config.OUTPUT_DIR == "outputs" or Config.OUTPUT_DIR.endswith("outputs")
    
    def test_default_log_file(self, mock_config):
        """Test default log file"""
        assert Config.LOG_FILE == "crew_execution.log"
    
    def test_allow_delegation_disabled(self, mock_config):
        """Test that agent delegation is disabled by default"""
        assert Config.ALLOW_DELEGATION == False


class TestConfigEnvironmentVariables:
    """Test environment variable loading"""
    
    def test_config_loads_from_env(self, monkeypatch):
        """Test Config loads values from environment variables"""
        monkeypatch.setenv("OLLAMA_API_KEY", "custom-key-123")
        monkeypatch.setenv("OLLAMA_BASE_URL", "https://custom.ollama.cloud")
        monkeypatch.setenv("DEFAULT_MODEL", "llama3:70b")
        monkeypatch.setenv("VERBOSE_LEVEL", "1")
        
        import importlib
        import config as config_module
        importlib.reload(config_module)
        
        assert config_module.Config.OLLAMA_API_KEY == "custom-key-123"
        assert config_module.Config.OLLAMA_BASE_URL == "https://custom.ollama.cloud"
        assert config_module.Config.DEFAULT_MODEL == "llama3:70b"
        assert config_module.Config.VERBOSE_LEVEL == 1
    
    def test_verbose_level_converts_to_int(self, monkeypatch):
        """Test VERBOSE_LEVEL is converted to integer"""
        monkeypatch.setenv("OLLAMA_API_KEY", "test")
        monkeypatch.setenv("VERBOSE_LEVEL", "2")
        
        import importlib
        import config as config_module
        importlib.reload(config_module)
        
        assert isinstance(config_module.Config.VERBOSE_LEVEL, int)
        assert config_module.Config.VERBOSE_LEVEL == 2
