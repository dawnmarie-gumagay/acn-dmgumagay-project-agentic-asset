"""
Pytest configuration and shared fixtures
"""
import pytest
from unittest.mock import Mock, patch
from crewai import Agent, Task, Crew, Process
from crewai import LLM


@pytest.fixture
def mock_llm():
    """Mock LLM for deterministic testing without API calls"""
    with patch('agents.llm') as mock:
        mock_instance = Mock(spec=LLM)
        mock_instance.call.return_value = "Mocked LLM response"
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_ollama_response():
    """Mock typical Ollama API response structure"""
    return {
        "model": "llama2:7b",
        "created_at": "2026-01-14T00:00:00Z",
        "response": "Mocked agent response",
        "done": True
    }


@pytest.fixture
def sample_user_prompt():
    """Sample user prompt for testing"""
    return "Deploy a Java Spring Boot application with 3 replicas, needs 512Mi memory and 500m CPU"


@pytest.fixture
def sample_kubernetes_manifest():
    """Sample valid Kubernetes manifest for testing"""
    return """apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-app
  labels:
    app: test-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
    spec:
      containers:
      - name: app
        image: test-app:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
"""


@pytest.fixture
def sample_deployment_failure():
    """Sample deployment failure status for self-healing tests"""
    return {
        "type": "OOMKilled",
        "exit_code": 137,
        "status": """
        Deployment Status: FAILED
        Pod Status:
        - test-app-78f5d4d7c-abc12: OOMKilled (Exit Code: 137)
        - test-app-78f5d4d7c-def34: OOMKilled (Exit Code: 137)
        
        Error: Pods killed due to out of memory.
        Current memory limit: 512Mi
        Observed memory usage: 650Mi
        """
    }


@pytest.fixture
def mock_config(monkeypatch):
    """Mock Config with test values"""
    monkeypatch.setenv("OLLAMA_API_KEY", "test-key-12345")
    monkeypatch.setenv("OLLAMA_BASE_URL", "https://test.ollama.cloud")
    monkeypatch.setenv("DEFAULT_MODEL", "llama2:7b")
    monkeypatch.setenv("VERBOSE_LEVEL", "0")
    
    from config import Config
    Config.validate()
    return Config


@pytest.fixture(autouse=True)
def reset_output_dir(tmp_path, monkeypatch):
    """Use temporary directory for outputs in tests"""
    test_output_dir = tmp_path / "outputs"
    test_output_dir.mkdir()
    monkeypatch.setattr("config.Config.OUTPUT_DIR", str(test_output_dir))
    return test_output_dir


@pytest.fixture
def clean_test_environment(monkeypatch):
    """Ensure clean environment for each test"""
    # Set test-specific environment variables
    monkeypatch.setenv("TESTING", "true")
    yield
    # Cleanup happens automatically with monkeypatch
