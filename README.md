# AgenticAI-DevOps

AI-Powered DevOps Automation using CrewAI and Ollama Cloud - A proof-of-concept agentic solution for automated Kubernetes deployment generation.

## Overview

This project demonstrates an agentic AI solution that automates DevOps tasks through a single-prompt interface. Using CrewAI's multi-agent orchestration with Ollama Cloud LLM, it can analyze deployment requirements and generate production-ready Kubernetes manifests.

## Features

- 🤖 **Multi-Agent System**: Specialized AI agents for requirements analysis, IaC generation, and validation
- 📝 **Single-Prompt Operation**: Input your deployment needs in natural language
- 🚀 **Kubernetes Manifest Generation**: Automatically creates deployment YAML files
- 💾 **File Output**: Saves results and generated manifests with timestamps
- 📊 **Detailed Logging**: Tracks execution flow and performance metrics
- ✅ **Validation**: Ensures generated manifests follow best practices

## Architecture

### Agents
1. **Requirements Analyzer**: Extracts deployment specifications from user prompts
2. **IaC Generator**: Creates Kubernetes deployment manifests
3. **Validator**: Validates generated configurations for correctness

### Workflow
```
User Prompt → Analysis → Generation → Validation → YAML Output
```

## Prerequisites

- Python 3.10 or higher
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

### Basic Usage

Run the main script:
```bash
python main.py
```

### Custom Prompts

Edit `main.py` and modify the `user_prompt` variable:
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

The system generates two files in the `outputs/` directory:

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

## Project Structure

```
AgenticAI-DevOps/
├── .env                    # Environment variables (not in git)
├── .env.template           # Template for environment setup
├── .gitignore             # Git ignore rules
├── requirements.txt        # Python dependencies
├── config.py              # Configuration management
├── crew.py                # LLM connection factory
├── agents.py              # Agent definitions
├── tasks.py               # Task definitions
├── main.py                # Main orchestrator
├── test_connection.py     # Connection test script
├── outputs/               # Generated results (not in git)
│   ├── result_*.json
│   └── deployment_*.yaml
└── crew_execution.log     # Execution logs
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
python test_connection.py
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

### Phase 1 (Current)
- ✅ Basic multi-agent setup
- ✅ Kubernetes manifest generation
- ✅ File output capability
- ✅ Logging and monitoring

### Phase 2 (Future)
- [ ] Self-healing capabilities
- [ ] Multiple cloud providers
- [ ] Terraform support
- [ ] CI/CD pipeline integration
- [ ] Web interface
- [ ] Real deployment execution

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

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
