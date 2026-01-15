# Test Suite for AgenticAI-DevOps

Comprehensive test suite using pytest for the CrewAI-based DevOps automation system.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Shared fixtures and configuration
├── test_agents.py              # Agent initialization and behavior tests
├── test_tasks.py               # Task creation and description tests
├── test_config.py              # Configuration management tests
├── test_integration.py         # End-to-end workflow tests
├── test_prompt_templates.py    # Prompt template tests
├── fixtures/
│   └── sample_manifests.py     # Reusable K8s manifest fixtures
└── README.md                   # This file
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_agents.py
```

### Run Specific Test Class
```bash
pytest tests/test_agents.py::TestAgentInitialization
```

### Run Specific Test Function
```bash
pytest tests/test_agents.py::TestAgentInitialization::test_requirements_analyzer_initialization
```

### Run with Coverage Report
```bash
pytest --cov=. --cov-report=html
# Open htmlcov/index.html to view coverage
```

### Run Tests by Marker
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run tests without VCR
pytest -m "not vcr"
```

## Test Categories

### Unit Tests (`test_agents.py`, `test_tasks.py`, `test_config.py`)
- **Purpose**: Test individual components in isolation
- **Speed**: Fast (< 1 second each)
- **LLM**: Fully mocked, no API calls
- **Focus**: Agent initialization, task creation, configuration validation

### Integration Tests (`test_integration.py`)
- **Purpose**: Test complete workflows end-to-end
- **Speed**: Moderate (1-5 seconds each)
- **LLM**: Mocked responses simulating real behavior
- **Focus**: Crew execution, task dependencies, output handling

### Prompt Template Tests (`test_prompt_templates.py`)
- **Purpose**: Test prompt retrieval and formatting
- **Speed**: Fast (< 1 second each)
- **LLM**: Not required
- **Focus**: Template integrity, variable substitution, integration patterns

## Test Fixtures

### Shared Fixtures (in `conftest.py`)
- `mock_llm`: Mocked LLM instance for testing without API calls
- `mock_config`: Pre-configured Config with test environment variables
- `sample_user_prompt`: Standard deployment request for testing
- `sample_kubernetes_manifest`: Valid K8s manifest for testing
- `sample_deployment_failure`: Failure scenario for self-healing tests
- `reset_output_dir`: Temporary directory for test outputs

### Manifest Fixtures (in `fixtures/sample_manifests.py`)
- `SIMPLE_DEPLOYMENT`: Basic nginx deployment
- `DEPLOYMENT_WITH_RESOURCES`: Manifest with resource limits and probes
- `DEPLOYMENT_WITH_SECURITY_CONTEXT`: Security-hardened deployment
- `OOMKILLED_STATUS`: OOMKilled failure scenario
- `CRASHLOOP_STATUS`: CrashLoopBackOff failure scenario
- `IMAGE_PULL_STATUS`: ImagePullBackOff failure scenario

## Test Markers

Markers help categorize and filter tests:

- `@pytest.mark.unit`: Fast unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.vcr`: Tests using VCR for API recording
- `@pytest.mark.slow`: Tests that take longer to run
- `@pytest.mark.mock_llm`: Tests requiring mocked LLM
- `@pytest.mark.real_llm`: Tests making actual API calls (use sparingly)

Example usage:
```python
@pytest.mark.unit
def test_agent_initialization():
    pass

@pytest.mark.integration
@pytest.mark.slow
def test_full_workflow():
    pass
```

## Mocking Strategy

### LLM Mocking
All tests use mocked LLMs to avoid API costs and ensure deterministic results:

```python
@patch('agents.llm')
def test_with_mock(mock_llm):
    mock_llm.call.return_value = "Expected response"
    # Test code here
```

### Environment Mocking
Use `monkeypatch` fixture to mock environment variables:

```python
def test_config(monkeypatch):
    monkeypatch.setenv("OLLAMA_API_KEY", "test-key")
    # Test code here
```

## Coverage Goals

- **Target**: 80%+ overall coverage
- **Critical Paths**: 100% coverage for core workflows (agents, tasks, config)
- **Integration**: 70%+ coverage for main.py and main_with_healing.py

View coverage report:
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Using VCR.py (Advanced)

VCR.py records actual LLM API interactions for replay in tests, reducing costs and improving speed.

### Installation
```bash
pip install vcrpy pytest-vcr
```

### Usage
```python
@pytest.mark.vcr()
def test_with_real_api():
    # First run: Records actual API call to cassette
    # Subsequent runs: Replays from cassette
    result = crew.kickoff()
    assert result is not None
```

Cassettes are stored in `tests/cassettes/` (git-ignored).

## Best Practices

1. **Isolate Tests**: Each test should be independent
2. **Mock External Calls**: Never hit real APIs in CI/CD
3. **Use Fixtures**: Reuse common test data via fixtures
4. **Clear Names**: Test names should describe what they test
5. **Fast Tests**: Keep unit tests under 1 second
6. **Assertions**: Include meaningful assertions with clear messages
7. **Cleanup**: Use fixtures with `yield` for automatic cleanup

## Continuous Integration

Tests run automatically on every commit via GitHub Actions (when configured).

Example CI command:
```bash
pytest --cov=. --cov-report=xml --cov-report=term
```

## Troubleshooting

### Tests Fail with "Config Not Found"
Ensure `.env` exists or use `mock_config` fixture:
```python
def test_something(mock_config):
    # Test code here
```

### Import Errors
Run from project root:
```bash
cd /path/to/project
pytest tests/
```

### Slow Tests
Use parallel execution:
```bash
pip install pytest-xdist
pytest -n auto  # Run with auto-detected CPU cores
```

### Coverage Not Generated
Ensure pytest-cov is installed:
```bash
pip install pytest-cov
```

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure tests pass: `pytest`
3. Check coverage: `pytest --cov`
4. Add docstrings to test classes/functions
5. Update this README if adding new test categories

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [CrewAI testing examples](https://github.com/crewaiinc/crewai/tree/main/tests)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
