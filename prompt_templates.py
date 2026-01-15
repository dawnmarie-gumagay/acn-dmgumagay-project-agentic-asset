"""
DevOps Agent Prompt Templates
Comprehensive prompt templates for various DevOps automation roles
"""

# ============================================================================
# CORE DEVOPS ROLES - Enhanced versions of existing agents
# ============================================================================

REQUIREMENTS_ANALYZER_PROMPTS = {
    "analyze_deployment": """
    Analyze the following user requirements and extract structured deployment specifications:
    
    User Requirements:
    {user_input}
    
    Extract and structure the following information:
    1. Application Details:
       - Application name
       - Application type (web app, API, database, etc.)
       - Runtime/technology stack
    
    2. Container Configuration:
       - Base container image
       - Required ports and protocols
       - Environment variables
       - Volume mounts (if any)
    
    3. Resource Requirements:
       - CPU requests and limits
       - Memory requests and limits
       - Storage requirements
    
    4. Scaling & Availability:
       - Number of replicas
       - High availability requirements
       - Auto-scaling parameters
    
    5. Networking:
       - Service type (ClusterIP, NodePort, LoadBalancer)
       - Ingress requirements
       - Internal/external access patterns
    
    6. Dependencies:
       - External services
       - ConfigMaps or Secrets needed
       - Init containers
    
    Provide a structured JSON output with all extracted specifications.
    """,
    
    "analyze_microservices": """
    Analyze the following microservices architecture requirements:
    
    Requirements:
    {user_input}
    
    For each microservice identified, extract:
    - Service name and purpose
    - Inter-service dependencies
    - Communication patterns (REST, gRPC, messaging)
    - Data storage needs
    - Service mesh requirements
    - API gateway needs
    
    Provide recommendations for service decomposition and deployment strategy.
    """,
    
    "analyze_migration": """
    Analyze the following legacy application migration requirements:
    
    Current State:
    {current_state}
    
    Target State:
    {target_state}
    
    Identify:
    1. Containerization strategy
    2. Stateful vs stateless components
    3. Data migration approach
    4. Rollback strategy
    5. Testing requirements
    6. Migration phases and milestones
    """
}

IAC_GENERATOR_PROMPTS = {
    "generate_kubernetes_manifest": """
    Generate a production-ready Kubernetes manifest based on these specifications:
    
    {specifications}
    
    Requirements:
    1. Include Deployment with proper labels and selectors
    2. Add Service definition for network access
    3. Configure resource requests and limits
    4. Add liveness and readiness probes
    5. Include proper annotations for monitoring
    6. Follow naming conventions: {namespace}-{app-name}
    7. Add pod disruption budget for HA deployments
    8. Include security context with non-root user
    
    Output valid YAML that can be applied directly with kubectl.
    """,
    
    "generate_helm_chart": """
    Generate a Helm chart structure for the following application:
    
    {specifications}
    
    Create:
    1. Chart.yaml with metadata
    2. values.yaml with configurable parameters
    3. Templates for Deployment, Service, Ingress
    4. ConfigMap and Secret templates
    5. NOTES.txt with post-installation instructions
    6. _helpers.tpl with template functions
    
    Follow Helm best practices for parameterization and reusability.
    """,
    
    "generate_terraform": """
    Generate Terraform configuration for Kubernetes resources:
    
    {specifications}
    
    Include:
    1. Provider configuration for Kubernetes
    2. Namespace resource
    3. Deployment resource
    4. Service resource
    5. Variables for customization
    6. Outputs for resource references
    
    Use proper Terraform syntax with resource dependencies.
    """,
    
    "generate_kustomize": """
    Generate Kustomize overlay structure for multi-environment deployment:
    
    Base Configuration:
    {base_config}
    
    Environments: {environments}
    
    Create:
    1. base/ directory with common resources
    2. overlays/ for each environment (dev, staging, prod)
    3. kustomization.yaml files with proper patches
    4. Environment-specific configurations
    """
}

VALIDATOR_PROMPTS = {
    "validate_kubernetes": """
    Validate the following Kubernetes manifest:
    
    {manifest}
    
    Check for:
    1. YAML syntax correctness
    2. Required fields presence (apiVersion, kind, metadata, spec)
    3. Resource limit configurations
    4. Label consistency and best practices
    5. Probe configurations (liveness, readiness, startup)
    6. Security contexts and policies
    7. Image pull policies
    8. Service selector matching
    9. Volume mount configurations
    10. Deprecated API versions
    
    Provide detailed feedback on issues found and validation status.
    """,
    
    "validate_security": """
    Perform security validation on the following manifest:
    
    {manifest}
    
    Security checklist:
    - Running as non-root user
    - Read-only root filesystem
    - Privilege escalation disabled
    - Capabilities dropped
    - Security context defined
    - No secrets in environment variables
    - Resource limits set (prevents DoS)
    - Network policies defined
    - Pod security standards compliance
    
    Report security risks with severity levels (Critical, High, Medium, Low).
    """,
    
    "validate_best_practices": """
    Validate against Kubernetes best practices:
    
    {manifest}
    
    Check:
    1. Health checks configured
    2. Resource requests match limits for guaranteed QoS
    3. Labels follow conventions (app, version, component, managed-by)
    4. Annotations for monitoring and documentation
    5. Rolling update strategy configured
    6. Pod disruption budget for HA
    7. Anti-affinity rules for pod distribution
    8. Appropriate restart policy
    9. Service account configuration
    10. Image tags are specific (not :latest)
    """
}

REMEDIATION_PROMPTS = {
    "diagnose_crashloop": """
    Diagnose and fix CrashLoopBackOff error:
    
    Pod Status:
    {pod_status}
    
    Recent Logs:
    {logs}
    
    Analyze:
    1. Application startup errors
    2. Missing dependencies or configurations
    3. Health check failures
    4. Resource constraints
    
    Provide:
    - Root cause analysis
    - Specific fix (configuration patch)
    - Prevention recommendations
    """,
    
    "diagnose_oom": """
    Diagnose OOMKilled (Out of Memory) error:
    
    Pod Details:
    {pod_details}
    
    Resource Usage:
    {resource_metrics}
    
    Determine:
    1. Memory usage patterns
    2. Memory leak indicators
    3. Appropriate memory limits
    
    Recommend:
    - Adjusted resource limits
    - Memory optimization strategies
    - Monitoring improvements
    """,
    
    "diagnose_image_pull": """
    Diagnose ImagePullBackOff error:
    
    Error Details:
    {error_details}
    
    Check:
    1. Image name and tag correctness
    2. Registry accessibility
    3. Authentication requirements
    4. Network connectivity
    
    Provide fix for image pull issues.
    """,
    
    "auto_remediate": """
    Automatically remediate the following deployment issue:
    
    Issue Type: {issue_type}
    Current State: {current_state}
    Error Details: {error_details}
    
    Analyze the failure pattern and generate:
    1. Detailed diagnosis
    2. Automated fix (kubectl patch or manifest update)
    3. Verification steps
    4. Monitoring recommendations to prevent recurrence
    
    Be specific with commands and configuration changes.
    """
}

# ============================================================================
# ADDITIONAL DEVOPS ROLES - New specialized agents
# ============================================================================

SECURITY_SCANNER_PROMPTS = {
    "scan_vulnerabilities": """
    Perform security vulnerability scan on deployment configuration:
    
    Configuration:
    {configuration}
    
    Scan for:
    1. Container image vulnerabilities
    2. Exposed secrets or credentials
    3. Insecure network configurations
    4. Missing RBAC policies
    5. Compliance violations (PCI-DSS, HIPAA, SOC2)
    6. Container runtime security issues
    
    Provide:
    - Vulnerability report with CVE details
    - Remediation steps for each finding
    - Compliance assessment
    """,
    
    "generate_rbac": """
    Generate RBAC (Role-Based Access Control) configuration:
    
    Requirements:
    {requirements}
    
    Create:
    1. ServiceAccount definitions
    2. Role/ClusterRole with minimal permissions
    3. RoleBinding/ClusterRoleBinding
    4. Pod security policies
    
    Follow principle of least privilege.
    """,
    
    "scan_secrets": """
    Scan configuration for hardcoded secrets or sensitive data:
    
    Files to scan:
    {files}
    
    Detect:
    - API keys, tokens, passwords
    - Database connection strings
    - Private keys or certificates
    - AWS/GCP credentials
    
    Recommend using Kubernetes Secrets or external secret management tools.
    """
}

COST_OPTIMIZER_PROMPTS = {
    "analyze_costs": """
    Analyze resource costs and optimization opportunities:
    
    Current Configuration:
    {configuration}
    
    Cluster Metrics:
    {metrics}
    
    Analyze:
    1. Over-provisioned resources
    2. Under-utilized deployments
    3. Idle resources
    4. Spot instance opportunities
    5. Storage optimization
    
    Provide:
    - Cost breakdown
    - Optimization recommendations
    - Estimated savings
    """,
    
    "optimize_resources": """
    Optimize resource allocation for cost efficiency:
    
    Current Resources:
    {current_resources}
    
    Usage Patterns:
    {usage_patterns}
    
    Recommend:
    1. Right-sized resource requests/limits
    2. Horizontal Pod Autoscaler configuration
    3. Vertical Pod Autoscaler recommendations
    4. Cluster autoscaler settings
    5. Spot/preemptible instance usage
    """,
    
    "storage_optimization": """
    Optimize storage costs and performance:
    
    Current Storage:
    {storage_config}
    
    Analyze:
    - Storage class selection
    - Volume reclaim policies
    - Snapshot strategies
    - Unused persistent volumes
    
    Recommend cost-effective storage solutions.
    """
}

MONITORING_SETUP_PROMPTS = {
    "generate_monitoring": """
    Generate comprehensive monitoring configuration:
    
    Application:
    {application_details}
    
    Generate:
    1. Prometheus ServiceMonitor definitions
    2. Grafana dashboard JSON
    3. Alert rules for critical metrics
    4. Log aggregation configuration
    5. Tracing setup (Jaeger/Zipkin)
    
    Include key metrics:
    - Request rate, error rate, duration (RED)
    - CPU, memory, disk, network (USE)
    - Custom application metrics
    """,
    
    "generate_alerts": """
    Generate alerting rules for production readiness:
    
    Service:
    {service_details}
    
    Create alerts for:
    1. High error rates (>1%)
    2. Slow response times (p99 > threshold)
    3. Pod restart loops
    4. Resource saturation (>80%)
    5. Deployment failures
    6. Certificate expiration
    7. Security incidents
    
    Configure alert severity and escalation policies.
    """,
    
    "slo_configuration": """
    Define Service Level Objectives (SLOs) and monitoring:
    
    Service Requirements:
    {requirements}
    
    Define:
    1. SLO targets (availability, latency, throughput)
    2. SLI (Service Level Indicators) to measure
    3. Error budget calculations
    4. Alerting on SLO violations
    5. Monitoring dashboards for SLOs
    
    Follow SRE best practices for SLO definition.
    """
}

CICD_GENERATOR_PROMPTS = {
    "generate_github_actions": """
    Generate GitHub Actions workflow for CI/CD:
    
    Application:
    {application_details}
    
    Create workflow with:
    1. Build and test jobs
    2. Container image build and push
    3. Security scanning (Trivy, Snyk)
    4. Kubernetes deployment
    5. Integration tests
    6. Rollback procedures
    
    Include environment promotion strategy (dev -> staging -> prod).
    """,
    
    "generate_gitlab_ci": """
    Generate GitLab CI/CD pipeline:
    
    Requirements:
    {requirements}
    
    Pipeline stages:
    1. Build and unit tests
    2. Static code analysis
    3. Container build
    4. Security scanning
    5. Deploy to environments
    6. Smoke tests
    7. Performance tests
    
    Use GitLab CI best practices with caching and artifacts.
    """,
    
    "generate_argocd": """
    Generate ArgoCD application configuration for GitOps:
    
    Application:
    {application_details}
    
    Create:
    1. Application CRD definition
    2. Sync policy configuration
    3. Multi-environment strategy
    4. Automated sync vs manual approval
    5. Health checks and sync waves
    6. Notification configuration
    
    Follow GitOps best practices.
    """,
    
    "generate_tekton": """
    Generate Tekton Pipelines for Kubernetes-native CI/CD:
    
    Requirements:
    {requirements}
    
    Create:
    1. Task definitions for build, test, deploy
    2. Pipeline definition with task ordering
    3. PipelineRun triggers
    4. Workspace and volume configurations
    5. Secret handling for registry access
    """
}

DISASTER_RECOVERY_PROMPTS = {
    "generate_backup_strategy": """
    Generate disaster recovery and backup strategy:
    
    Application:
    {application_details}
    
    Create:
    1. Velero backup schedules
    2. Persistent volume backup policies
    3. Database backup procedures
    4. Disaster recovery runbook
    5. RTO/RPO definitions
    6. Recovery testing procedures
    
    Ensure compliance with business continuity requirements.
    """,
    
    "generate_failover": """
    Generate multi-region failover configuration:
    
    Requirements:
    {requirements}
    
    Design:
    1. Multi-cluster deployment strategy
    2. Traffic management (Global LB)
    3. Data replication approach
    4. Failover triggers and automation
    5. Health checks across regions
    6. DNS failover configuration
    """,
    
    "recovery_plan": """
    Generate incident recovery plan:
    
    Scenario:
    {scenario}
    
    Create detailed runbook including:
    1. Detection and alerting
    2. Impact assessment
    3. Step-by-step recovery procedures
    4. Rollback procedures
    5. Communication plan
    6. Post-incident review template
    """
}

NETWORK_ENGINEER_PROMPTS = {
    "generate_service_mesh": """
    Generate service mesh configuration (Istio/Linkerd):
    
    Application Architecture:
    {architecture}
    
    Configure:
    1. Virtual services for traffic routing
    2. Destination rules for load balancing
    3. Gateway for ingress traffic
    4. mTLS for service-to-service encryption
    5. Circuit breakers and retries
    6. Traffic mirroring for testing
    7. Canary deployments
    """,
    
    "generate_network_policies": """
    Generate Kubernetes Network Policies for micro-segmentation:
    
    Services:
    {services}
    
    Create policies for:
    1. Ingress rules (allowed sources)
    2. Egress rules (allowed destinations)
    3. Namespace isolation
    4. Default deny policies
    5. Database access restrictions
    6. External service access control
    """,
    
    "generate_ingress": """
    Generate Ingress configuration with advanced routing:
    
    Requirements:
    {requirements}
    
    Configure:
    1. Host-based routing
    2. Path-based routing
    3. TLS/SSL certificates
    4. Rate limiting
    5. Authentication (OAuth, JWT)
    6. CORS policies
    7. Sticky sessions
    8. Request/response transformations
    """
}

DATABASE_OPERATOR_PROMPTS = {
    "generate_statefulset": """
    Generate StatefulSet for database deployment:
    
    Database:
    {database_type}
    
    Requirements:
    {requirements}
    
    Configure:
    1. StatefulSet with stable network identities
    2. Persistent volume claims
    3. Init containers for setup
    4. Readiness and liveness probes
    5. Backup CronJob
    6. Headless service
    7. Pod anti-affinity for HA
    """,
    
    "generate_operator": """
    Generate database operator configuration (if applicable):
    
    Database: {database}
    
    Configure operator for:
    1. Automated backups
    2. Scaling operations
    3. Upgrade procedures
    4. Monitoring integration
    5. Disaster recovery
    
    Use operators like: PostgreSQL Operator, MySQL Operator, MongoDB Operator.
    """,
    
    "migration_job": """
    Generate Kubernetes Job for database migration:
    
    Migration Details:
    {migration_details}
    
    Create:
    1. Job definition with migration container
    2. ConfigMap with migration scripts
    3. Secret management for DB credentials
    4. Pre-migration backup job
    5. Rollback job (if needed)
    6. Success/failure notifications
    """
}

# ============================================================================
# UTILITY TEMPLATES
# ============================================================================

COMMON_PROMPTS = {
    "explain_configuration": """
    Explain the following configuration in simple terms:
    
    {configuration}
    
    Provide:
    1. What this configuration does
    2. Key components and their purposes
    3. Security considerations
    4. Resource requirements
    5. Prerequisites for deployment
    """,
    
    "compare_options": """
    Compare the following deployment options:
    
    Option A:
    {option_a}
    
    Option B:
    {option_b}
    
    Compare based on:
    1. Performance
    2. Cost
    3. Maintainability
    4. Scalability
    5. Security
    
    Recommend the best option with justification.
    """,
    
    "generate_documentation": """
    Generate comprehensive documentation for:
    
    {subject}
    
    Include:
    1. Overview and architecture
    2. Prerequisites
    3. Installation steps
    4. Configuration options
    5. Usage examples
    6. Troubleshooting guide
    7. FAQ
    8. References
    """
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_prompt(category: str, prompt_name: str, **kwargs) -> str:
    """
    Retrieve and format a prompt template
    
    Args:
        category: Prompt category (e.g., 'REQUIREMENTS_ANALYZER_PROMPTS')
        prompt_name: Specific prompt name within the category
        **kwargs: Variables to substitute in the template
    
    Returns:
        Formatted prompt string
    """
    prompt_dict = globals().get(category, {})
    template = prompt_dict.get(prompt_name, "")
    
    if not template:
        raise ValueError(f"Prompt '{prompt_name}' not found in category '{category}'")
    
    return template.format(**kwargs)


def list_available_prompts() -> dict:
    """
    List all available prompt categories and their prompts
    
    Returns:
        Dictionary of categories and their available prompts
    """
    result = {}
    for name, value in globals().items():
        if name.endswith('_PROMPTS') and isinstance(value, dict):
            result[name] = list(value.keys())
    return result


def create_custom_prompt(base_prompt: str, additional_context: str = "") -> str:
    """
    Create a custom prompt by extending a base prompt
    
    Args:
        base_prompt: The base prompt template
        additional_context: Additional context or requirements to append
    
    Returns:
        Extended prompt
    """
    if additional_context:
        return f"{base_prompt}\n\nAdditional Context:\n{additional_context}"
    return base_prompt


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Example 1: Get a formatted prompt
    print("=" * 80)
    print("Example 1: Requirements Analysis Prompt")
    print("=" * 80)
    prompt = get_prompt(
        "REQUIREMENTS_ANALYZER_PROMPTS",
        "analyze_deployment",
        user_input="Deploy a Node.js API with Redis cache, needs 3 replicas"
    )
    print(prompt)
    
    # Example 2: List all available prompts
    print("\n" + "=" * 80)
    print("Example 2: Available Prompts")
    print("=" * 80)
    available = list_available_prompts()
    for category, prompts in available.items():
        print(f"\n{category}:")
        for prompt in prompts:
            print(f"  - {prompt}")
    
    # Example 3: Security scanning prompt
    print("\n" + "=" * 80)
    print("Example 3: Security Scan Prompt")
    print("=" * 80)
    security_prompt = get_prompt(
        "SECURITY_SCANNER_PROMPTS",
        "scan_vulnerabilities",
        configuration="apiVersion: apps/v1\nkind: Deployment..."
    )
    print(security_prompt[:500] + "...")
