# AgenticAI-DevOps

AI-Powered DevOps Automation using CrewAI and Ollama Cloud - A proof-of-concept agentic solution for automated Kubernetes deployment generation.

## Overview

This project demonstrates an agentic AI solution that automates DevOps tasks through a single-prompt interface. Using CrewAI's multi-agent orchestration with Ollama Cloud LLM, it can analyze deployment requirements and generate production-ready Kubernetes manifests.

## Features

- 🤖 **Multi-Agent System**: Specialized AI agents for requirements analysis, IaC generation, and validation
- 📝 **Single-Prompt Operation**: Input your deployment needs in natural language
- 🚀 **Kubernetes Manifest Generation**: Automatically creates deployment YAML files
- � **Self-Healing Capability**: Detects failures and automatically applies remediation fixes
- 💾 **File Output**: Saves results and generated manifests with timestamps
- 📊 **Detailed Logging**: Tracks execution flow and performance metrics
- ✅ **Validation**: Ensures generated manifests follow best practices
- 🔄 **Retry Logic**: Exponential backoff for deployment retry attempts

## Architecture

### Agents
1. **Requirements Analyzer**: Extracts deployment specifications from user prompts
2. **IaC Generator**: Creates Kubernetes deployment manifests
3. **Validator**: Validates generated configurations for correctness
4. **Remediation Agent**: Diagnoses failures and applies automated fixes

### Workflow

**Standard Mode:**
```
User Prompt → Analysis → Generation → Validation → YAML Output
```

**Self-Healing Mode:**
```
User Prompt → Analysis → Generation → Validation → Deploy → Monitor
             ↓ (If failure detected)
          Diagnose → Remediate → Retry Deploy → Monitor → Success
```

## Prerequisites

- Python 3.10 < 3.14
- pip package manager
- Ollama Cloud account and API key
- Git (for version control)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AgenticAI-DevOps
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.template` to `.env`:
```bash
copy .env.template .env  # Windows
cp .env.template .env    # macOS/Linux
```

Edit `.env` and add your Ollama Cloud credentials:
```env
OLLAMA_API_KEY=your_actual_api_key_here
OLLAMA_BASE_URL=https://api.ollama.cloud
DEFAULT_MODEL=llama2:7b
VERBOSE_LEVEL=2
```

### 5. Test Connection
```bash
python test_connection.py
```

You should see:
```
✓ ALL TESTS PASSED - Connection is working!
```

## Usage

### Basic Usage (Standard Mode)

Run the main script to generate manifests:
```bash
python main.py
```

### Self-Healing Mode

Run with automatic failure detection and remediation:
```bash
python main_with_healing.py
```

This mode will:
1. Generate and validate the manifest
2. Simulate deployment
3. Monitor for failures
4. Automatically diagnose issues
5. Apply fixes and retry (up to 3 attempts)
6. Log all remediation actions

### Custom Prompts

Provide custom deployment requirements as command-line arguments:
```bash
python main_with_healing.py "Deploy a Node.js app with 5 replicas, 1Gi memory, 500m CPU"
```

Or edit the script and modify the `user_prompt` variable:
```python
user_prompt = "Deploy a Java Spring Boot application with 3 replicas, needs 512Mi memory and 500m CPU"
```

### Example Prompts

```python
# Simple deployment
"Deploy a Node.js application on port 3000"

# With resource specs
"Create a Python Flask app deployment with 2 replicas, 256Mi memory, port 8080"

# Complex deployment
"Deploy a Java microservice with 5 replicas, 1Gi memory, 1000m CPU, expose port 8080 and 9090"
```

## Output

The system generates files in the `outputs/` directory:

### Standard Mode Output

1. **result_TIMESTAMP.json**: Complete execution details
   ```json
   {
     "timestamp": "2026-01-07T14:30:00",
     "user_prompt": "...",
     "execution_time_seconds": 45.32,
     "model": "llama2:7b",
     "result": "..."
   }
   ```

2. **deployment_TIMESTAMP.yaml**: Generated Kubernetes manifest
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: java-app
   spec:
     replicas: 3
     ...
   ```

### Self-Healing Mode Output

1. **remediation_log_TIMESTAMP.json**: Detailed healing audit log
   ```json
   {
     "timestamp": "2026-01-07T15:00:00",
     "user_prompt": "Deploy a Java Spring Boot app...",
     "max_retries": 3,
     "attempts": [
       {
         "attempt_number": 1,
         "deployment_status": "FAILED - OOMKilled",
         "healing_attempted": true,
         "diagnosis": "Memory limit too low",
         "remediation": "Increased memory from 512Mi to 1Gi"
       },
       {
         "attempt_number": 2,
         "deployment_status": "SUCCESS",
         "result": "SUCCESS"
       }
     ],
     "final_status": "SUCCESS",
     "total_attempts": 2,
     "execution_time_seconds": 180.5
   }
   ```

2. **healed_deployment_TIMESTAMP.yaml**: Final corrected manifest with fixes applied

## Project Structure

```
AgenticAI-DevOps/
├── .env                      # Environment variables (not in git)
├── .env.template             # Template for environment setup
├── .gitignore               # Git ignore rules
├── requirements.txt          # Python dependencies
├── config.py                # Configuration management
├── crew.py                  # LLM connection factory
├── agents.py                # Agent definitions (4 agents)
├── tasks.py                 # Task definitions (includes healing tasks)
├── main.py                  # Main orchestrator (standard mode)
├── main_with_healing.py     # Self-healing orchestrator
├── test_connection.py       # Connection test script
├── test_healing.py          # Failure scenario documentation
├── outputs/                 # Generated results (not in git)
│   ├── result_*.json
│   ├── deployment_*.yaml
│   ├── remediation_log_*.json
│   └── healed_deployment_*.yaml
└── crew_execution.log       # Execution logs
```

## Configuration

### Model Selection

Edit `DEFAULT_MODEL` in `.env`:
- `llama2:7b` - Faster, good for POC (recommended)
- `llama2` - Default variant
- `llama2:13b` - Better quality, slower

### Verbosity Levels

Set `VERBOSE_LEVEL` in `.env`:
- `0` - Minimal output
- `1` - Standard output
- `2` - Detailed logs (recommended for debugging)

### Self-Healing Configuration

The self-healing system uses:
- **Max Retries**: 3 attempts (configurable in `main_with_healing.py`)
- **Backoff Strategy**: Exponential (1s, 2s, 4s, 8s max)
- **Supported Failure Types**:
  - OOMKilled (Out of Memory)
  - CrashLoopBackOff (Configuration errors)
  - ImagePullBackOff (Image not found)
  - Pending (Resource constraints)
  - Liveness/Readiness probe failures

### Extending Self-Healing

To connect to a real Kubernetes cluster, modify `simulate_deployment()` in `main_with_healing.py`:

```python
from kubernetes import client, config

def simulate_deployment(manifest, retry_count=0):
    # Load kubeconfig
    config.load_kube_config()
    
    # Create API client
    api = client.AppsV1Api()
    
    # Apply manifest
    # ... (implementation details)
    
    return success, status
```

## Troubleshooting

### "OLLAMA_API_KEY is not set"
- Check that `.env` file exists
- Verify API key is correctly set in `.env`
- Ensure no extra spaces around the key

### "Connection failed"
- Verify API key is valid
- Check internet connectivity
- Confirm Ollama Cloud service status
- Try using test_connection.py to isolate the issue
- Try via curl command:
```
curl -H "Authorization: Bearer $OLLAMA_API_KEY" -X POST https://api.ollama.cloud/api/generate -d '{"model": "gpt-oss:120b-cloud", "prompt": "test"}'
```

### "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### Slow Performance
- Use smaller model (llama2:7b)
- Reduce VERBOSE_LEVEL to 1 or 0
- Check Ollama Cloud rate limits

## Development

### Running Tests
```bash
# Test connection to Ollama Cloud
python test_connection.py

# View failure scenarios documentation
python test_healing.py

# Test self-healing workflow
python main_with_healing.py
```

### Checking Configuration
```bash
python config.py
```

### Testing LLM Connection
```bash
python crew.py
```

## Roadmap

### Phase 1 (Completed) ✅
- ✅ Basic multi-agent setup
- ✅ Kubernetes manifest generation
- ✅ File output capability
- ✅ Logging and monitoring
- ✅ Self-healing capabilities (Simulated)
- ✅ Failure detection and remediation
- ✅ Retry logic with exponential backoff
- ✅ Audit logging for healing actions

### Phase 2 (Future) 🚧
- [ ] Real Kubernetes cluster integration (kubectl/API)
- [ ] Multiple cloud providers (AWS, Azure, GCP)
- [ ] Terraform support
- [ ] CI/CD pipeline integration
- [ ] Web interface for user interactions
- [ ] Advanced monitoring and alerting
- [ ] Performance optimization (parallel agents)
- [ ] Integration with Accenture-approved LLMs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Use "black *.py" to format code for consistency
6. Submit a pull request

## License

[Add appropriate license]

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review CrewAI documentation
3. Contact the team lead

## Acknowledgments

- CrewAI Framework
- Ollama Cloud
- LangChain Community

---

**Status**: Proof of Concept (POC)  
**Last Updated**: January 7, 2026
