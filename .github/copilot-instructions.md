# AgenticAI-DevOps Copilot Instructions

## Project Overview
Multi-agent CrewAI system for comprehensive DevOps automation from natural language prompts. Currently generates Kubernetes manifests with self-healing capabilities, with roadmap to expand into full-scale DevOps project scaffolding (similar to Claude Code/Codex).

**Current State**: MVP proof-of-concept focused on K8s manifest generation
**Vision**: Full DevOps project generator - IaC, CI/CD pipelines, monitoring configs, security policies, and complete infrastructure setup
**LLM Provider**: Ollama Cloud (MVP) - architecture supports easy LLM switching via CrewAI's LLM wrapper

## Architecture

### Core Components
- **Agents** ([agents.py](../agents.py)): Four specialized agents (Requirements Analyzer, IaC Generator, Validator, Remediation)
- **Tasks** ([tasks.py](../tasks.py)): Sequential workflow definitions (analysis → generation → validation → healing)
- **Crew Orchestration**: Uses CrewAI's `Process.sequential` for deterministic execution order
- **Config** ([config.py](../config.py)): Centralized settings loaded from `.env` via python-dotenv

### Execution Modes
1. **Standard Mode** ([main.py](../main.py)): Generates manifest only (3 agents, 3 tasks)
2. **Self-Healing Mode** ([main_with_healing.py](../main_with_healing.py)): Adds monitoring → diagnosis → remediation cycle with simulated deployments
3. **Quick Demo** ([demo_healing_simple.py](../demo_healing_simple.py)): Pre-canned responses for fast demonstration

## Key Patterns

### LLM Initialization
All agents use CrewAI's `LLM` wrapper (not langchain-ollama directly):
```python
llm = LLM(
    model=f"ollama/{Config.DEFAULT_MODEL}",
    base_url=Config.OLLAMA_BASE_URL,
    api_key=Config.OLLAMA_API_KEY
)
```

### Task Dependencies
Tasks pass context implicitly through CrewAI's sequential process - no explicit output passing needed. The `expected_output` field documents what each task produces.

### Output Handling
- Results saved to `outputs/` with timestamps (`result_YYYYMMDD_HHMMSS.json`)
- YAML manifests extracted via simple string parsing (looks for `apiVersion` and `kind:`)
- All executions logged to `crew_execution.log`

### Configuration Validation
Always call `Config.validate()` before crew execution to ensure `OLLAMA_API_KEY` and `OLLAMA_BASE_URL` are set.

## Development Workflows

### Setup & Testing
```bash
# Environment setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.template .env  # Then add your OLLAMA_API_KEY

# Connection test (required first step)
python test_connection.py

# Run modes
python demo_healing_simple.py     # Quick demo (~5 seconds)
python main.py                    # Standard manifest generation
python main_with_healing.py       # Full healing workflow
```

### Adding New Agents
1. Define agent in [agents.py](../agents.py) with `llm`, `role`, `goal`, `backstory`
2. Set `allow_delegation=Config.ALLOW_DELEGATION` (currently False - no inter-agent communication)
3. Create corresponding task in [tasks.py](../tasks.py) with clear `description` and `expected_output`
4. Add task to crew initialization in execution script

### Using Prompt Templates
[prompt_templates.py](../prompt_templates.py) contains 40+ production-ready templates across 11 categories (see [PROMPT_TEMPLATES_SUMMARY.md](../PROMPT_TEMPLATES_SUMMARY.md)):
- Security scanning, cost optimization, monitoring setup
- CI/CD pipelines (GitHub Actions, GitLab, ArgoCD, Tekton)
- Network engineering (service mesh, ingress, network policies)
- Disaster recovery and database operations

**Integration Pattern**:
```python
from prompt_templates import get_prompt

task = Task(
    description=get_prompt(
        "CICD_GENERATOR_PROMPTS",
        "generate_github_actions",
        application_details=user_requirements
    ),
    agent=cicd_agent,
    expected_output="GitHub Actions workflow YAML"
)
```

**Roadmap**: Integrate these templates to expand from single-manifest generation to complete DevOps project scaffolding.

## Project Conventions

### File Naming
- `main.py` vs `main_with_healing.py`: Different execution modes, not versions
- `test_*.py`: Test scenarios (not pytest - manual execution)
- `demo_*.py`: Simplified demonstrations with mocked responses

### Agent Communication
- `ALLOW_DELEGATION = False`: Agents work independently in sequence
- No tool usage configured - agents work with prompts only
- Context passing is implicit through CrewAI's Process.sequential

### Error Handling
Self-healing simulates common Kubernetes failures:
- OOMKilled (Exit 137) → Increase memory limits
- CrashLoopBackOff → Fix configuration/health checks
- ImagePullBackOff → Correct image name/add pull secrets
- Insufficient resources → Reduce requests or scale down

See [test_healing.py](../test_healing.py) for all failure scenarios.

## Testing Strategy

### CrewAI Testing Framework
Use **pytest** with CrewAI's testing utilities:

```python
# tests/test_agents.py
import pytest
from crewai import Agent, Task, Crew
from unittest.mock import Mock, patch

def test_requirements_analyzer():
    """Test agent output parsing and validation"""
    task = create_analysis_task("Deploy nginx")
    # Mock LLM responses for deterministic testing
    with patch('agents.llm') as mock_llm:
        mock_llm.return_value = "Structured response"
        result = task.execute()
        assert "nginx" in result.lower()

def test_crew_workflow():
    """Integration test for full workflow"""
    crew = Crew(agents=[...], tasks=[...], process=Process.sequential)
    result = crew.kickoff()
    assert "apiVersion" in str(result)
```

**Test Structure**:
- Unit tests: Individual agent/task behavior with mocked LLMs
- Integration tests: Full crew workflows with real/mocked LLM
- Fixtures: Reusable test data in `tests/fixtures/`
- Run: `pytest tests/ -v --cov=. --cov-report=html`

**Current Gap**: Existing `test_*.py` files are manual scripts, not pytest - migration needed.

## External Dependencies

### Required Services
- **LLM Provider**: Ollama Cloud (MVP) - API key required in `.env`
  - Architecture supports swapping to OpenAI, Anthropic, Azure OpenAI via CrewAI's LLM abstraction
  - Change via `Config.DEFAULT_MODEL` and LLM initialization in [agents.py](../agents.py)
- **Kubernetes Cluster**: Currently simulated; real cluster integration planned
  - Future: Use `kubectl` or official Kubernetes Python client
  - Consider namespaced deployments for multi-tenant scenarios

### Python Packages
- `crewai>=1.7.2`: Multi-agent orchestration framework
- `langchain-ollama`: LLM integration (not used directly - wrapped by CrewAI)
- `litellm`: LLM provider abstraction layer
- `python-dotenv`: Environment variable management
- `pytest` (add to requirements): Testing framework for CrewAI workflows

## Expansion Roadmap

### Phase 1: Current (Kubernetes Manifests)
- ✅ Requirements analysis → YAML generation → validation → self-healing
- ✅ 40+ prompt templates documented but not integrated

### Phase 2: Full DevOps Project Generation
**Goal**: Generate complete, deployable DevOps projects from single prompt

**Planned Capabilities**:
1. **Infrastructure Setup**: Terraform/Pulumi modules for cloud resources
2. **CI/CD Pipelines**: GitHub Actions, GitLab CI, Jenkins, ArgoCD configs
3. **Monitoring Stack**: Prometheus, Grafana, ELK stack configurations
4. **Security Layer**: RBAC policies, network policies, Vault integration
5. **Documentation**: Auto-generated README, runbooks, architecture diagrams

**Implementation Approach**:
- Create specialized agents (SecurityAgent, MonitoringAgent, CICDAgent)
- Integrate prompt templates from [prompt_templates.py](../prompt_templates.py)
- Hierarchical task dependencies: base infra → app deployment → monitoring → CI/CD
- Output complete project directory structure (not just single files)

### Phase 3: Real Kubernetes Integration
- Replace `simulate_deployment()` with actual `kubectl` or K8s Python client
- Real-time pod monitoring for self-healing (not simulated failures)
- Multi-cluster support for production/staging separation

## Important Notes
- CrewAI execution is synchronous - expect 2-5 minute runs for full workflows
- Verbose output controlled by `VERBOSE_LEVEL` in `.env` (0=quiet, 2=detailed)
- Deployments currently simulated - real K8s integration planned (Phase 3)
- Results in `outputs/` directory are not git-tracked
- LLM provider easily swappable - don't hard-code Ollama-specific logic
