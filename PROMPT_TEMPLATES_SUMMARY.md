# DevOps Agent Prompt Templates - Summary

## Overview
This document provides a comprehensive summary of all available prompt templates for DevOps automation agents. These templates support various roles from infrastructure provisioning to security scanning and disaster recovery.

---

## 📊 Template Categories

### Total Categories: 11
### Total Prompts: 40+

---

## 1. 🔍 Requirements Analyzer Prompts

**Category:** `REQUIREMENTS_ANALYZER_PROMPTS`  
**Purpose:** Extract and structure deployment specifications from user requirements

| Prompt Name | Purpose |
|------------|---------|
| `analyze_deployment` | Analyzes user requirements to extract application details, container config, resource requirements, scaling parameters, networking needs, and dependencies. Outputs structured JSON. |
| `analyze_microservices` | Analyzes microservices architecture requirements including service dependencies, communication patterns, data storage, and service mesh needs. |
| `analyze_migration` | Analyzes legacy application migration requirements, identifies containerization strategy, stateful/stateless components, and migration phases. |

---

## 2. 🏗️ IaC Generator Prompts

**Category:** `IAC_GENERATOR_PROMPTS`  
**Purpose:** Generate Infrastructure as Code configurations for various platforms

| Prompt Name | Purpose |
|------------|---------|
| `generate_kubernetes_manifest` | Generates production-ready Kubernetes YAML manifests with deployments, services, resource limits, health probes, and security contexts. |
| `generate_helm_chart` | Creates complete Helm chart structure including Chart.yaml, values.yaml, templates, and helper functions. |
| `generate_terraform` | Generates Terraform configuration for Kubernetes resources with provider setup, variables, and outputs. |
| `generate_kustomize` | Creates Kustomize overlay structure for multi-environment deployments (dev, staging, prod). |

---

## 3. ✅ Validator Prompts

**Category:** `VALIDATOR_PROMPTS`  
**Purpose:** Validate configurations for correctness, security, and best practices

| Prompt Name | Purpose |
|------------|---------|
| `validate_kubernetes` | Validates Kubernetes manifests for YAML syntax, required fields, resource configs, labels, probes, and deprecated APIs. |
| `validate_security` | Performs security validation checking for non-root users, read-only filesystems, privilege escalation, capabilities, and security contexts. Reports risks with severity levels. |
| `validate_best_practices` | Validates against Kubernetes best practices including health checks, QoS, labels, rolling updates, pod disruption budgets, and anti-affinity rules. |

---

## 4. 🔧 Remediation Prompts

**Category:** `REMEDIATION_PROMPTS`  
**Purpose:** Diagnose deployment failures and provide automated fixes

| Prompt Name | Purpose |
|------------|---------|
| `diagnose_crashloop` | Diagnoses CrashLoopBackOff errors by analyzing pod status, logs, startup errors, missing dependencies, and health check failures. Provides root cause and fix. |
| `diagnose_oom` | Diagnoses OOMKilled (Out of Memory) errors, analyzes memory usage patterns, identifies leaks, and recommends appropriate resource limits. |
| `diagnose_image_pull` | Diagnoses ImagePullBackOff errors checking image names, registry access, authentication, and network connectivity. |
| `auto_remediate` | Automatically remediates deployment issues with detailed diagnosis, automated fix (kubectl patch), verification steps, and prevention recommendations. |

---

## 5. 🔐 Security Scanner Prompts

**Category:** `SECURITY_SCANNER_PROMPTS`  
**Purpose:** Scan for vulnerabilities and generate security configurations

| Prompt Name | Purpose |
|------------|---------|
| `scan_vulnerabilities` | Performs comprehensive security scans for container vulnerabilities, exposed secrets, insecure configs, missing RBAC, and compliance violations. Provides CVE details and remediation. |
| `generate_rbac` | Generates RBAC configurations including ServiceAccounts, Roles, ClusterRoles, and bindings following the principle of least privilege. |
| `scan_secrets` | Scans configuration files for hardcoded secrets (API keys, passwords, DB strings, credentials). Recommends proper secret management. |

---

## 6. 💰 Cost Optimizer Prompts

**Category:** `COST_OPTIMIZER_PROMPTS`  
**Purpose:** Analyze and optimize cloud resource costs

| Prompt Name | Purpose |
|------------|---------|
| `analyze_costs` | Analyzes resource costs identifying over-provisioned resources, under-utilized deployments, idle resources, and spot instance opportunities. Provides cost breakdown and savings estimates. |
| `optimize_resources` | Optimizes resource allocation recommending right-sized requests/limits, HPA/VPA configurations, and cluster autoscaler settings. |
| `storage_optimization` | Optimizes storage costs analyzing storage classes, volume reclaim policies, snapshot strategies, and unused volumes. |

---

## 7. 📈 Monitoring Setup Prompts

**Category:** `MONITORING_SETUP_PROMPTS`  
**Purpose:** Generate monitoring, alerting, and SLO configurations

| Prompt Name | Purpose |
|------------|---------|
| `generate_monitoring` | Generates comprehensive monitoring setup including Prometheus ServiceMonitors, Grafana dashboards, alert rules, log aggregation, and tracing configs. Covers RED and USE metrics. |
| `generate_alerts` | Creates alerting rules for production readiness covering error rates, response times, pod restarts, resource saturation, deployment failures, and certificate expiration. |
| `slo_configuration` | Defines Service Level Objectives (SLOs), Service Level Indicators (SLIs), error budgets, and SLO violation alerts following SRE best practices. |

---

## 8. 🚀 CI/CD Generator Prompts

**Category:** `CICD_GENERATOR_PROMPTS`  
**Purpose:** Generate CI/CD pipeline configurations for various platforms

| Prompt Name | Purpose |
|------------|---------|
| `generate_github_actions` | Generates GitHub Actions workflows with build, test, container build/push, security scanning, Kubernetes deployment, and rollback procedures. |
| `generate_gitlab_ci` | Creates GitLab CI/CD pipelines with stages for build, test, analysis, security scanning, deployment, smoke tests, and performance tests. |
| `generate_argocd` | Generates ArgoCD application configurations for GitOps including sync policies, multi-environment strategy, health checks, and notifications. |
| `generate_tekton` | Creates Tekton Pipelines with task definitions, pipeline ordering, triggers, workspace configs, and secret handling. |

---

## 9. 🆘 Disaster Recovery Prompts

**Category:** `DISASTER_RECOVERY_PROMPTS`  
**Purpose:** Generate backup strategies and disaster recovery plans

| Prompt Name | Purpose |
|------------|---------|
| `generate_backup_strategy` | Generates comprehensive DR strategy including Velero backups, PV backup policies, database backups, runbooks, and RTO/RPO definitions. |
| `generate_failover` | Creates multi-region failover configuration covering multi-cluster deployment, traffic management, data replication, and DNS failover. |
| `recovery_plan` | Generates incident recovery plans (runbooks) with detection, impact assessment, recovery procedures, rollback steps, and post-incident review templates. |

---

## 10. 🌐 Network Engineer Prompts

**Category:** `NETWORK_ENGINEER_PROMPTS`  
**Purpose:** Generate network configurations and service mesh setups

| Prompt Name | Purpose |
|------------|---------|
| `generate_service_mesh` | Generates service mesh configurations (Istio/Linkerd) including virtual services, destination rules, gateways, mTLS, circuit breakers, and canary deployments. |
| `generate_network_policies` | Creates Kubernetes Network Policies for micro-segmentation with ingress/egress rules, namespace isolation, and default deny policies. |
| `generate_ingress` | Generates advanced Ingress configurations with host/path routing, TLS, rate limiting, authentication (OAuth, JWT), CORS, and sticky sessions. |

---

## 11. 🗄️ Database Operator Prompts

**Category:** `DATABASE_OPERATOR_PROMPTS`  
**Purpose:** Generate database deployment and management configurations

| Prompt Name | Purpose |
|------------|---------|
| `generate_statefulset` | Generates StatefulSet configurations for databases with stable network identities, PVCs, init containers, probes, backup CronJobs, and headless services. |
| `generate_operator` | Creates database operator configurations for automated backups, scaling, upgrades, monitoring, and disaster recovery (PostgreSQL, MySQL, MongoDB operators). |
| `migration_job` | Generates Kubernetes Jobs for database migrations including migration containers, ConfigMaps, secret management, pre-migration backups, and rollback jobs. |

---

## 12. 🛠️ Common Utility Prompts

**Category:** `COMMON_PROMPTS`  
**Purpose:** General-purpose utility prompts for various tasks

| Prompt Name | Purpose |
|------------|---------|
| `explain_configuration` | Explains configurations in simple terms covering what it does, key components, security considerations, resource requirements, and prerequisites. |
| `compare_options` | Compares deployment options based on performance, cost, maintainability, scalability, and security. Provides justified recommendations. |
| `generate_documentation` | Generates comprehensive documentation including overview, prerequisites, installation steps, configuration options, usage examples, troubleshooting, and FAQ. |

---

## 📖 Usage

### Basic Usage Example

```python
from prompt_templates import get_prompt

# Get a formatted prompt
prompt = get_prompt(
    "REQUIREMENTS_ANALYZER_PROMPTS",
    "analyze_deployment",
    user_input="Deploy a Node.js API with Redis cache"
)
```

### List All Available Prompts

```python
from prompt_templates import list_available_prompts

available = list_available_prompts()
for category, prompts in available.items():
    print(f"{category}: {prompts}")
```

### Create Custom Prompt

```python
from prompt_templates import create_custom_prompt

custom = create_custom_prompt(
    base_prompt="Generate Kubernetes config",
    additional_context="Must support multi-region deployment"
)
```

---

## 🎯 Use Cases by Role

### DevOps Engineer
- Requirements analysis and deployment specifications
- IaC generation (Kubernetes, Helm, Terraform)
- CI/CD pipeline setup
- Disaster recovery planning

### SRE (Site Reliability Engineer)
- Monitoring and alerting setup
- SLO/SLI definition
- Auto-remediation of common failures
- Incident recovery plans

### Security Engineer
- Vulnerability scanning
- RBAC configuration
- Security validation
- Secrets management

### Cloud Architect
- Cost optimization
- Multi-region failover
- Service mesh architecture
- Network policies

### Database Administrator
- StatefulSet configurations
- Database operators setup
- Migration jobs
- Backup strategies

---

## 🔄 Integration with Existing Agents

These prompts can be easily integrated with the existing agents in `agents.py`:

- **requirements_analyzer** → Use `REQUIREMENTS_ANALYZER_PROMPTS`
- **iac_generator** → Use `IAC_GENERATOR_PROMPTS`
- **validator** → Use `VALIDATOR_PROMPTS`
- **remediation_agent** → Use `REMEDIATION_PROMPTS`

### Example Integration

```python
from crewai import Task
from prompt_templates import get_prompt

# Create a task with a template prompt
analysis_task = Task(
    description=get_prompt(
        "REQUIREMENTS_ANALYZER_PROMPTS",
        "analyze_deployment",
        user_input=user_requirements
    ),
    agent=requirements_analyzer,
    expected_output="Structured JSON with deployment specifications"
)
```

---

## 📝 Key Features

✅ **40+ Pre-built Prompts** covering all major DevOps scenarios  
✅ **11 Specialized Categories** for different roles and tasks  
✅ **Template Variables** for dynamic prompt generation  
✅ **Best Practices Built-in** following industry standards  
✅ **Production-Ready** prompts tested for real-world scenarios  
✅ **Easy Integration** with CrewAI agents  
✅ **Extensible** - add custom prompts easily  

---

## 🚦 Quick Reference

| Need to... | Use Category | Top Prompt |
|------------|-------------|-----------|
| Deploy an application | IAC_GENERATOR_PROMPTS | generate_kubernetes_manifest |
| Fix CrashLoopBackOff | REMEDIATION_PROMPTS | diagnose_crashloop |
| Scan for vulnerabilities | SECURITY_SCANNER_PROMPTS | scan_vulnerabilities |
| Reduce cloud costs | COST_OPTIMIZER_PROMPTS | analyze_costs |
| Setup monitoring | MONITORING_SETUP_PROMPTS | generate_monitoring |
| Create CI/CD pipeline | CICD_GENERATOR_PROMPTS | generate_github_actions |
| Plan disaster recovery | DISASTER_RECOVERY_PROMPTS | generate_backup_strategy |
| Configure service mesh | NETWORK_ENGINEER_PROMPTS | generate_service_mesh |
| Deploy database | DATABASE_OPERATOR_PROMPTS | generate_statefulset |

---

## 📚 Additional Resources

- **File:** `prompt_templates.py`
- **Agents:** `agents.py`
- **Configuration:** `config.py`
- **Tasks:** `tasks.py`

---

## 🔮 Future Enhancements

Potential additions to the prompt library:
- Chaos engineering prompts
- Performance testing configurations
- Compliance audit prompts
- Multi-cloud migration prompts
- Edge computing deployment prompts
- Serverless/FaaS configurations

---

**Last Updated:** January 14, 2026  
**Version:** 1.0  
**Maintainer:** DevOps Automation Team
