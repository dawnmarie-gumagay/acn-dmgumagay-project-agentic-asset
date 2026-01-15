# AgenticAI-DevOps 🚀

**Complete DevOps Project Generator** - Like Claude Code, but for Infrastructure

AI-Powered DevOps automation that generates **production-ready, complete project structures** - not just YAML files! Using CrewAI's multi-agent orchestration with Ollama Cloud, transform natural language requirements into deployable DevOps projects.

## 🎯 What This Does

**Instead of just generating Kubernetes YAML**, this tool generates:

✅ **Complete Project Structure** - Full directory layout with all necessary files  
✅ **Infrastructure as Code** - Terraform/Pulumi for cloud resources  
✅ **Kubernetes Manifests** - Deployments, services, configs for all components  
✅ **CI/CD Pipelines** - GitHub Actions/GitLab CI ready to run  
✅ **Monitoring Stack** - Prometheus, Grafana, alert rules  
✅ **Security Configurations** - RBAC, network policies, pod security  
✅ **Complete Documentation** - README, architecture diagrams, runbooks, deployment guides  
✅ **Utility Scripts** - Deploy, rollback, and maintenance scripts  

**Think of it as "Claude Code for DevOps" - but specialized for infrastructure and deployments!**

## 🌟 Key Features

### 🏗️ Complete Project Generation
- **Microservices Architecture**: Multi-service projects with service mesh
- **Monolithic Applications**: Single-service deployments
- **Multi-Environment**: Dev, staging, production configurations
- **Production-Ready**: Best practices baked in

### 🤖 AI-Powered Intelligence
- **8 Specialized Agents**: Architecture, Infrastructure, Security, Monitoring, CI/CD, Documentation, and more
- **Natural Language Input**: Describe what you need in plain English
- **Smart Recommendations**: AI suggests best practices and technologies
- **Self-Healing**: Automatic failure detection and remediation

### 📦 What Gets Generated

```
your-project/
├── services/                    # All microservices with Dockerfiles
│   ├── api-service/
│   │   ├── Dockerfile
│   │   ├── k8s/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── src/
│   │   └── tests/
│   ├── auth-service/
│   └── user-service/
├── infrastructure/              # Infrastructure as Code
│   ├── terraform/              # Complete Terraform configs
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── kubernetes.tf
│   └── k8s/                    # Base Kubernetes resources
│       ├── namespace.yaml
│       ├── network-policies.yaml
│       └── istio/              # Service mesh configs
├── monitoring/                  # Observability stack
│   ├── prometheus/
│   │   ├── prometheus-config.yaml
│   │   └── alert-rules.yaml
│   └── grafana/
│       └── dashboards/
├── .github/workflows/          # CI/CD pipelines
│   ├── ci-cd.yaml             # Build, test, deploy
│   └── security-scan.yaml     # Trivy, Snyk scanning
├── docs/                       # Complete documentation
│   ├── architecture.md         # System design
│   ├── deployment.md          # Step-by-step guide
│   └── runbook.md             # Operations guide
├── scripts/                    # Deployment automation
│   ├── deploy.sh              # Deployment script
│   └── rollback.sh            # Rollback script
├── README.md                   # Project overview
├── docker-compose.yaml         # Local development
├── .gitignore
└── project-metadata.json       # Generation details
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd acn-dmgumagay-project-agentic-asset

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env and add your OLLAMA_API_KEY
```

### Usage

#### Option 1: Simple Mode (Just K8s YAML)
```bash
# Generate just Kubernetes manifest
python main.py "Deploy a Node.js API with 3 replicas and Redis cache"
```

#### **Option 2: 🔥 Complete Project Mode** (Claude Code Style)
```bash
# Generate COMPLETE production-ready project
python main_project_generator.py "Create a microservices e-commerce platform with user, product, and payment services"

# Output saved to: ./generated-projects/project-YYYYMMDD-HHMMSS/
```

#### Advanced Options
```bash
# Customize output location
python main_project_generator.py \
  "Build a Python API with auth, database, monitoring, and CI/CD" \
  --output ./my-awesome-project \
  --template microservices

# Dry run to see what would be generated
python main_project_generator.py \
  "Your requirements here" \
  --dry-run

# Monolithic template
python main_project_generator.py \
  "Simple web application with database" \
  --template monolith
```

## 💡 Real-World Examples

### 1. E-Commerce Platform
```bash
python main_project_generator.py "Create a microservices e-commerce platform with user management, product catalog, shopping cart, payment processing, and order tracking services. Include API gateway, monitoring, and CI/CD."
```

**What You Get**:
- 5 microservices with complete Kubernetes configs
- Istio service mesh for traffic management
- Prometheus + Grafana monitoring
- GitHub Actions CI/CD pipeline
- Terraform for infrastructure
- Complete documentation

### 2. SaaS Application
```bash
python main_project_generator.py "Build a multi-tenant SaaS application with authentication service, user dashboard, analytics engine, and notification service. Needs RBAC and multi-environment support."
```

**What You Get**:
- Multi-service architecture with tenant isolation
- Complete RBAC and security policies
- Environment-specific configurations (dev, staging, prod)
- Monitoring and alerting
- Deployment automation

### 3. Data Processing Pipeline
```bash
python main_project_generator.py "Create a data processing pipeline with ingestion service, processing workers using Kubernetes jobs, and REST API for accessing results. Include monitoring and failure handling."
```

**What You Get**:
- Kubernetes Jobs for data processing
- StatefulSets for data storage
- Message queue configurations
- Monitoring for job completion
- Error handling and retry logic

### 4. Real-Time Chat Application
```bash
python main_project_generator.py "Build a real-time chat application with WebSocket support, message persistence, user authentication, and presence tracking. Scale to 10k concurrent users."
```

**What You Get**:
- WebSocket-enabled services
- Redis for session management
- Horizontal pod autoscaling
- Load balancing configuration
- Performance monitoring

## 🏛️ Architecture

### 8 Specialized AI Agents

| Agent | Role | Responsibilities |
|-------|------|-----------------|
| **Architecture Agent** 🏗️ | Solutions Architect | Designs system architecture, selects technology stack, defines patterns |
| **Infrastructure Agent** ☁️ | Cloud Engineer | Generates Terraform/Pulumi, provisions cloud resources |
| **IaC Generator** 📦 | DevOps Engineer | Creates Kubernetes manifests, Helm charts, Kustomize overlays |
| **CI/CD Agent** 🔄 | Pipeline Engineer | Builds GitHub Actions/GitLab CI, deployment strategies |
| **Monitoring Agent** 📊 | SRE | Sets up Prometheus, Grafana, defines SLOs, alert rules |
| **Security Agent** 🔒 | Security Engineer | Implements RBAC, network policies, security scanning |
| **Documentation Agent** 📚 | Technical Writer | Writes README, architecture docs, runbooks, guides |
| **Validator Agent** ✅ | QA Engineer | Validates all configurations for correctness and best practices |

### Multi-Phase Workflow

```
┌─────────────────────────────────────────────────────────┐
│          Phase 1: AI-Powered Analysis                    │
│                                                          │
│  User Requirements (Natural Language)                    │
│            ↓                                             │
│  ┌──────────────────────────────────┐                  │
│  │   Architecture Agent Analyzes     │                  │
│  │   - Pattern selection              │                  │
│  │   - Service decomposition          │                  │
│  │   - Tech stack recommendations     │                  │
│  └──────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│          Phase 2: Parallel Generation                    │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │Infrastructure│  │  Kubernetes  │  │    CI/CD     │ │
│  │     IaC      │  │  Manifests   │  │   Pipelines  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Monitoring  │  │   Security   │  │Documentation │ │
│  │    Setup     │  │   Policies   │  │   & Guides   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│          Phase 3: Project Assembly                       │
│                                                          │
│  - Create directory structure                            │
│  - Place generated files                                 │
│  - Add scripts and utilities                             │
│  - Generate project metadata                             │
└─────────────────────────────────────────────────────────┘
                        ↓
              Complete Deployable Project
```

## 📋 Available Templates

### 1. Microservices Template
**Best for**: Complex applications, scalable systems, service-oriented architecture

**Includes**:
- Multiple services with independent deployments
- Istio service mesh for traffic management
- API gateway configuration
- Service-to-service authentication (mTLS)
- Circuit breakers and retries
- Distributed tracing

**Command**:
```bash
python main_project_generator.py "Your requirements" --template microservices
```

### 2. Monolithic Template
**Best for**: Simple applications, MVPs, single-service deployments

**Includes**:
- Single service deployment
- Basic Kubernetes resources
- CI/CD pipeline
- Monitoring setup
- Documentation

**Command**:
```bash
python main_project_generator.py "Your requirements" --template monolith
```

## 🛠️ Project Modes

### Mode 1: Simple YAML Generator (`main.py`)
Generates only Kubernetes manifests - lightweight and fast

```bash
python main.py "Deploy Redis with persistence"
```

**Output**: Single YAML file in `outputs/`

### Mode 2: Complete Project Generator (`main_project_generator.py`)
Generates full production-ready project structure

```bash
python main_project_generator.py "Your requirements"
```

**Output**: Complete project directory with 20-50+ files

### Mode 3: Self-Healing Deployment (`main_with_healing.py`)
Includes automatic failure detection and remediation

```bash
python main_with_healing.py "Your requirements"
```

**Output**: YAML + deployment simulation + healing logs

## 📖 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[copilot-instructions.md](.github/copilot-instructions.md)** - Project conventions and patterns
- **[PROMPT_TEMPLATES_SUMMARY.md](PROMPT_TEMPLATES_SUMMARY.md)** - 40+ AI prompt templates
- **Generated Projects** - Each project includes complete documentation

## 🧪 Testing

```bash
# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Test connection to Ollama
python test_connection.py

# Demo self-healing (quick)
python demo_healing_simple.py
```

## 🔧 Configuration

Edit `.env` file:

```bash
# Ollama Cloud Configuration
OLLAMA_API_KEY=your-api-key-here
OLLAMA_BASE_URL=https://api.ollama.cloud

# Model Selection
DEFAULT_MODEL=llama2:7b

# Logging
VERBOSE_LEVEL=2  # 0=quiet, 1=normal, 2=detailed
```

## 📊 Prompt Templates

The project includes **40+ production-ready prompt templates** across 11 categories:

- Requirements Analysis
- Infrastructure Generation
- Security Scanning
- Cost Optimization
- Monitoring Setup
- CI/CD Pipeline Generation
- Network Engineering
- Database Operations
- Disaster Recovery
- And more...

See [PROMPT_TEMPLATES_SUMMARY.md](PROMPT_TEMPLATES_SUMMARY.md) for complete list.

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional project templates (serverless, data pipelines)
- More cloud providers (AWS, GCP, Azure-specific configs)
- Enhanced AI prompts
- Additional CI/CD platforms (Jenkins, CircleCI)
- Database operator integrations
- Service mesh alternatives (Linkerd, Consul)

## 📈 Roadmap

### Phase 1: MVP ✅
- [x] Basic Kubernetes manifest generation
- [x] Self-healing capability
- [x] Multi-agent architecture

### Phase 2: Complete Project Generation ✅ (CURRENT)
- [x] Full project structure generation
- [x] Infrastructure as Code (Terraform)
- [x] CI/CD pipelines
- [x] Monitoring and observability
- [x] Security configurations
- [x] Complete documentation

### Phase 3: Real Kubernetes Integration (PLANNED)
- [ ] Actual kubectl deployment
- [ ] Real-time health monitoring
- [ ] Multi-cluster support
- [ ] Helm chart generation
- [ ] GitOps integration (ArgoCD, Flux)

### Phase 4: Advanced Features (FUTURE)
- [ ] Cost optimization recommendations
- [ ] Performance tuning
- [ ] Compliance checking (PCI-DSS, HIPAA)
- [ ] Multi-cloud support
- [ ] Visual architecture diagrams
- [ ] Interactive project customization

## ⚡ Performance

- **Simple YAML Generation**: ~30-60 seconds
- **Complete Project Generation**: ~2-5 minutes
- **Files Generated**: 20-50+ files per project
- **Directories Created**: 10-20 per project

## 🆚 Comparison with Other Tools

| Feature | This Tool | kubectl | Helm | Claude Code |
|---------|-----------|---------|------|-------------|
| Complete Project Structure | ✅ | ❌ | ❌ | ✅ |
| Infrastructure Code (Terraform) | ✅ | ❌ | ❌ | ✅ |
| CI/CD Pipelines | ✅ | ❌ | ❌ | ✅ |
| Monitoring Setup | ✅ | ❌ | ❌ | Partial |
| Security Configurations | ✅ | Partial | Partial | ✅ |
| Natural Language Input | ✅ | ❌ | ❌ | ✅ |
| Complete Documentation | ✅ | ❌ | ❌ | ✅ |
| Self-Healing | ✅ | ❌ | ❌ | ❌ |
| **DevOps Specialized** | ✅ | ✅ | ✅ | ❌ |

## 🐛 Troubleshooting

### Issue: "OLLAMA_API_KEY is not set"
**Solution**: Copy `.env.template` to `.env` and add your API key

### Issue: "No module named 'crewai'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: Generated project is empty
**Solution**: Check logs in `project_generator.log` for errors

### Issue: Terraform syntax errors
**Solution**: Run `terraform fmt` in the terraform directory

## 📝 License

[Add your license here]

## 👥 Authors

- **Dawn Marie Gumagay** - Initial development

## 🙏 Acknowledgments

- CrewAI for multi-agent orchestration
- Ollama Cloud for LLM inference
- Kubernetes community for best practices
- Open source DevOps tools community

---

**Ready to generate production-ready DevOps projects in minutes instead of days?**

```bash
python main_project_generator.py "Create your amazing project here"
```

🚀 **Happy deploying!**
