"""
Project Templates for Different Architecture Patterns
Defines complete project structures for various deployment scenarios
"""
from typing import Dict, List, Any


class ProjectTemplate:
    """Base class for project templates"""
    
    def __init__(self, project_name: str, description: str):
        self.project_name = project_name
        self.description = description
        self.tech_stack = []
        self.structure = {}
    
    def get_structure(self) -> Dict[str, Any]:
        """Return the complete project structure"""
        return self.structure
    
    def get_tech_stack(self) -> List[str]:
        """Return the technology stack"""
        return self.tech_stack


class MicroservicesTemplate(ProjectTemplate):
    """Template for microservices architecture"""
    
    def __init__(self, project_name: str, services: List[str], use_service_mesh: bool = True):
        super().__init__(project_name, "Microservices architecture with Kubernetes")
        self.services = services
        self.use_service_mesh = use_service_mesh
        self.tech_stack = [
            "Kubernetes",
            "Docker",
            "Prometheus & Grafana",
            "GitHub Actions",
            "Terraform",
            "Istio" if use_service_mesh else "Nginx Ingress"
        ]
        self._build_structure()
    
    def _build_structure(self):
        """Build the microservices project structure"""
        self.structure = {
            'services': {
                service: {
                    'Dockerfile': self._get_service_dockerfile(service),
                    'k8s': {
                        'deployment.yaml': self._get_service_deployment(service),
                        'service.yaml': self._get_service_service(service),
                    },
                    'src': {},
                    'tests': {}
                } for service in self.services
            },
            'infrastructure': {
                'terraform': {
                    'main.tf': self._get_terraform_main(),
                    'variables.tf': self._get_terraform_variables(),
                    'outputs.tf': self._get_terraform_outputs(),
                    'kubernetes.tf': self._get_terraform_kubernetes(),
                },
                'k8s': {
                    'namespace.yaml': self._get_namespace(),
                    'network-policies.yaml': self._get_network_policies(),
                }
            },
            'monitoring': {
                'prometheus': {
                    'prometheus-config.yaml': self._get_prometheus_config(),
                    'alert-rules.yaml': self._get_alert_rules(),
                },
                'grafana': {
                    'dashboards': {
                        'overview.json': '{}  # Grafana dashboard JSON'
                    }
                }
            },
            '.github': {
                'workflows': {
                    'ci-cd.yaml': self._get_github_actions(),
                    'security-scan.yaml': self._get_security_scan_workflow(),
                }
            },
            'docs': {
                'architecture.md': self._get_architecture_doc(),
                'deployment.md': self._get_deployment_doc(),
                'runbook.md': self._get_runbook(),
            },
            'scripts': {
                'deploy.sh': self._get_deploy_script(),
                'rollback.sh': self._get_rollback_script(),
            },
            'README.md': self._get_readme(),
            '.gitignore': self._get_gitignore(),
            'docker-compose.yaml': self._get_docker_compose(),
        }
        
        if self.use_service_mesh:
            self.structure['infrastructure']['k8s']['istio'] = {
                'virtual-services.yaml': self._get_virtual_services(),
                'destination-rules.yaml': self._get_destination_rules(),
                'gateway.yaml': self._get_istio_gateway(),
            }
    
    def _get_service_dockerfile(self, service_name: str) -> str:
        return f"""FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app .

EXPOSE 8080

USER node

CMD ["node", "index.js"]

# Service: {service_name}
# Multi-stage build for smaller image size
"""
    
    def _get_service_deployment(self, service_name: str) -> str:
        return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  namespace: {self.project_name}
  labels:
    app: {service_name}
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
        version: v1
    spec:
      serviceAccountName: {service_name}
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: {service_name}
        image: {self.project_name}/{service_name}:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
          name: http
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
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
        env:
        - name: SERVICE_NAME
          value: {service_name}
        - name: ENVIRONMENT
          valueFrom:
            configMapKeyRef:
              name: {self.project_name}-config
              key: environment
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {service_name}
  namespace: {self.project_name}
"""
    
    def _get_service_service(self, service_name: str) -> str:
        return f"""apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  namespace: {self.project_name}
  labels:
    app: {service_name}
spec:
  selector:
    app: {service_name}
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
    name: http
  type: ClusterIP
"""
    
    def _get_terraform_main(self) -> str:
        return f"""terraform {{
  required_version = ">= 1.0"
  
  required_providers {{
    kubernetes = {{
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }}
    helm = {{
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }}
  }}
  
  backend "s3" {{
    bucket = "{self.project_name}-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-east-1"
  }}
}}

provider "kubernetes" {{
  config_path = var.kubeconfig_path
}}

provider "helm" {{
  kubernetes {{
    config_path = var.kubeconfig_path
  }}
}}

# Main infrastructure configuration
resource "kubernetes_namespace" "{self.project_name}" {{
  metadata {{
    name = "{self.project_name}"
    labels = {{
      project     = "{self.project_name}"
      environment = var.environment
    }}
  }}
}}
"""
    
    def _get_terraform_variables(self) -> str:
        return """variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "enable_monitoring" {
  description = "Enable Prometheus and Grafana"
  type        = bool
  default     = true
}

variable "enable_istio" {
  description = "Enable Istio service mesh"
  type        = bool
  default     = true
}
"""
    
    def _get_terraform_outputs(self) -> str:
        return f"""output "namespace" {{
  description = "Kubernetes namespace"
  value       = kubernetes_namespace.{self.project_name}.metadata[0].name
}}

output "services" {{
  description = "Deployed services"
  value       = [
{chr(10).join([f'    "{service}",' for service in self.services])}
  ]
}}
"""
    
    def _get_terraform_kubernetes(self) -> str:
        return """# Kubernetes resources managed by Terraform

resource "kubernetes_config_map" "app_config" {
  metadata {
    name      = "${var.project_name}-config"
    namespace = kubernetes_namespace.main.metadata[0].name
  }
  
  data = {
    environment = var.environment
    log_level   = var.environment == "prod" ? "info" : "debug"
  }
}

resource "kubernetes_secret" "app_secrets" {
  metadata {
    name      = "${var.project_name}-secrets"
    namespace = kubernetes_namespace.main.metadata[0].name
  }
  
  type = "Opaque"
  
  data = {
    # Add secrets here or use external secret management
  }
}
"""
    
    def _get_namespace(self) -> str:
        return f"""apiVersion: v1
kind: Namespace
metadata:
  name: {self.project_name}
  labels:
    name: {self.project_name}
    istio-injection: {'enabled' if self.use_service_mesh else 'disabled'}
"""
    
    def _get_network_policies(self) -> str:
        policies = [f"""apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {service}-policy
  namespace: {self.project_name}
spec:
  podSelector:
    matchLabels:
      app: {service}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: {self.project_name}
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: {self.project_name}
  - to:  # Allow DNS
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
---""" for service in self.services]
        
        return '\n'.join(policies)
    
    def _get_prometheus_config(self) -> str:
        return f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
          - {self.project_name}
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
"""
    
    def _get_alert_rules(self) -> str:
        return """apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-alert-rules
  namespace: monitoring
data:
  alerts.yml: |
    groups:
    - name: application_alerts
      interval: 30s
      rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} for {{ $labels.service }}"
      
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod is crash looping"
          description: "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is restarting"
"""
    
    def _get_github_actions(self) -> str:
        workflows = []
        for service in self.services:
            workflows.append(f"""
      - name: Build and Push {service}
        run: |
          docker build -t ${{{{ secrets.REGISTRY }}}}/{self.project_name}/{service}:${{{{ github.sha }}}} ./services/{service}
          docker push ${{{{ secrets.REGISTRY }}}}/{self.project_name}/{service}:${{{{ github.sha }}}}
      
      - name: Deploy {service}
        run: |
          kubectl set image deployment/{service} {service}=${{{{ secrets.REGISTRY }}}}/{self.project_name}/{service}:${{{{ github.sha }}}} -n {self.project_name}
""")
        
        return f"""name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Tests
        run: |
          # Add test commands here
          echo "Running tests..."
  
  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{{{ secrets.AWS_ACCESS_KEY_ID }}}}
          aws-secret-access-key: ${{{{ secrets.AWS_SECRET_ACCESS_KEY }}}}
          aws-region: us-east-1
      
      - name: Login to Container Registry
        run: |
          echo ${{{{ secrets.REGISTRY_PASSWORD }}}} | docker login ${{{{ secrets.REGISTRY }}}} -u ${{{{ secrets.REGISTRY_USERNAME }}}} --password-stdin
{''.join(workflows)}
      - name: Verify Deployment
        run: |
          kubectl rollout status deployment -n {self.project_name} --timeout=5m
"""
    
    def _get_security_scan_workflow(self) -> str:
        return """name: Security Scanning

on:
  push:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
"""
    
    def _get_virtual_services(self) -> str:
        services_yaml = []
        for service in self.services:
            services_yaml.append(f"""---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: {service}
  namespace: {self.project_name}
spec:
  hosts:
  - {service}.{self.project_name}.svc.cluster.local
  http:
  - route:
    - destination:
        host: {service}
        subset: v1
      weight: 100
    retries:
      attempts: 3
      perTryTimeout: 2s
    timeout: 10s
""")
        return '\n'.join(services_yaml)
    
    def _get_destination_rules(self) -> str:
        rules = []
        for service in self.services:
            rules.append(f"""---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: {service}
  namespace: {self.project_name}
spec:
  host: {service}
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
  subsets:
  - name: v1
    labels:
      version: v1
""")
        return '\n'.join(rules)
    
    def _get_istio_gateway(self) -> str:
        return f"""apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: {self.project_name}-gateway
  namespace: {self.project_name}
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: {self.project_name}-tls-cert
    hosts:
    - "*"
"""
    
    def _get_architecture_doc(self) -> str:
        return f"""# {self.project_name} - Architecture Documentation

## Overview

This project implements a microservices architecture with the following services:

{chr(10).join([f'- **{service}**: [Description]' for service in self.services])}

## Architecture Diagram

```
┌─────────────────┐
│   API Gateway   │
│   (Istio/Nginx) │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│Service│ │Service│
│   1   │ │   2   │
└───┬───┘ └──┬────┘
    │        │
    └────┬───┘
         │
    ┌────▼────┐
    │Database │
    └─────────┘
```

## Technology Stack

- **Container Runtime**: Docker
- **Orchestration**: Kubernetes
- **Service Mesh**: {'Istio' if self.use_service_mesh else 'Nginx Ingress'}
- **Monitoring**: Prometheus + Grafana
- **CI/CD**: GitHub Actions
- **IaC**: Terraform

## Design Decisions

### Microservices Pattern
- Each service is independently deployable
- Services communicate via REST APIs
- Service discovery via Kubernetes DNS

### Scalability
- Horizontal pod autoscaling based on CPU/memory
- Load balancing at service level
- Stateless service design

### Resilience
- Circuit breakers and retries
- Health checks (liveness/readiness probes)
- Pod disruption budgets

### Security
- RBAC for service accounts
- Network policies for service isolation
- mTLS for service-to-service communication
- Non-root containers

## Service Descriptions

{chr(10).join([f'''### {service}

**Purpose**: [Add description]

**Endpoints**:
- `GET /health` - Health check
- `GET /ready` - Readiness check
- [Add more endpoints]

**Dependencies**: [List dependencies]

**Scaling Strategy**: Horizontal based on CPU
''' for service in self.services])}

## Data Flow

1. Request enters through API Gateway
2. Gateway routes to appropriate service
3. Service processes request
4. Response returns through gateway

## Monitoring and Observability

- **Metrics**: Prometheus scrapes metrics from all services
- **Logs**: Centralized logging with ELK/Loki
- **Tracing**: Distributed tracing with Jaeger
- **Dashboards**: Grafana dashboards for visualization

## Deployment Strategy

- **Blue-Green**: For zero-downtime deployments
- **Canary**: For gradual rollout with monitoring
- **Rolling Update**: Default strategy for regular updates
"""
    
    def _get_deployment_doc(self) -> str:
        return f"""# Deployment Guide - {self.project_name}

## Prerequisites

1. Kubernetes cluster (1.24+)
2. kubectl CLI configured
3. Helm 3.x installed
4. Docker for building images
5. Terraform (for infrastructure)

## Environment Setup

### Local Development

```bash
# Start local Kubernetes cluster
minikube start --cpus=4 --memory=8192

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### Infrastructure Provisioning

```bash
# Initialize Terraform
cd infrastructure/terraform
terraform init

# Review plan
terraform plan -var="environment=dev"

# Apply infrastructure
terraform apply -var="environment=dev"
```

## Build and Deploy

### 1. Build Container Images

```bash
# Build all services
{chr(10).join([f'docker build -t {self.project_name}/{service}:latest ./services/{service}' for service in self.services])}
```

### 2. Push to Registry

```bash
# Tag and push
{chr(10).join([f'''docker tag {self.project_name}/{service}:latest your-registry/{self.project_name}/{service}:latest
docker push your-registry/{self.project_name}/{service}:latest''' for service in self.services])}
```

### 3. Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace {self.project_name}

# Apply configurations
kubectl apply -f infrastructure/k8s/namespace.yaml
kubectl apply -f infrastructure/k8s/network-policies.yaml

# Deploy services
{chr(10).join([f'kubectl apply -f services/{service}/k8s/' for service in self.services])}
```

### 4. Verify Deployment

```bash
# Check pod status
kubectl get pods -n {self.project_name}

# Check services
kubectl get svc -n {self.project_name}

# View logs
kubectl logs -f deployment/[service-name] -n {self.project_name}
```

## Configuration Management

### Environment Variables

Set via ConfigMaps:
```bash
kubectl create configmap {self.project_name}-config \\
  --from-literal=environment=production \\
  --from-literal=log_level=info \\
  -n {self.project_name}
```

### Secrets

```bash
kubectl create secret generic {self.project_name}-secrets \\
  --from-literal=db-password=your-password \\
  -n {self.project_name}
```

## Monitoring Setup

```bash
# Install Prometheus and Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# Access Grafana
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
```

## Rollback

```bash
# Rollback a deployment
kubectl rollout undo deployment/[service-name] -n {self.project_name}

# Rollback to specific revision
kubectl rollout undo deployment/[service-name] --to-revision=2 -n {self.project_name}
```

## Troubleshooting

### Pod Not Starting

```bash
# Describe pod for events
kubectl describe pod [pod-name] -n {self.project_name}

# Check logs
kubectl logs [pod-name] -n {self.project_name}
```

### Service Not Reachable

```bash
# Check service endpoints
kubectl get endpoints [service-name] -n {self.project_name}

# Test connectivity from another pod
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://[service-name]
```

## Production Checklist

- [ ] Resource limits configured
- [ ] Health checks enabled
- [ ] Monitoring and alerting set up
- [ ] Backup strategy in place
- [ ] Disaster recovery plan documented
- [ ] Security scanning completed
- [ ] Load testing performed
- [ ] Runbooks created
"""
    
    def _get_runbook(self) -> str:
        return f"""# Runbook - {self.project_name}

## Common Operations

### Check System Health

```bash
# Overall cluster health
kubectl get nodes
kubectl top nodes

# Application health
kubectl get pods -n {self.project_name}
kubectl top pods -n {self.project_name}
```

### Scale Services

```bash
# Manual scaling
kubectl scale deployment/[service-name] --replicas=5 -n {self.project_name}

# Enable autoscaling
kubectl autoscale deployment/[service-name] --cpu-percent=70 --min=3 --max=10 -n {self.project_name}
```

### View Logs

```bash
# Recent logs
kubectl logs -f deployment/[service-name] -n {self.project_name}

# Logs from specific time
kubectl logs --since=1h deployment/[service-name] -n {self.project_name}

# Logs from all replicas
kubectl logs -l app=[service-name] -n {self.project_name} --all-containers=true
```

## Incident Response

### High CPU Usage

1. Check which pods are consuming resources:
   ```bash
   kubectl top pods -n {self.project_name} --sort-by=cpu
   ```

2. Scale up if needed:
   ```bash
   kubectl scale deployment/[service-name] --replicas=10 -n {self.project_name}
   ```

3. Investigate root cause in logs

### Pod CrashLooping

1. Get pod status:
   ```bash
   kubectl describe pod [pod-name] -n {self.project_name}
   ```

2. Check recent logs:
   ```bash
   kubectl logs [pod-name] -n {self.project_name} --previous
   ```

3. Common fixes:
   - Increase memory limits
   - Fix configuration errors
   - Update liveness probe settings

### Service Unreachable

1. Check service endpoints:
   ```bash
   kubectl get endpoints [service-name] -n {self.project_name}
   ```

2. Verify network policies:
   ```bash
   kubectl get networkpolicies -n {self.project_name}
   ```

3. Test connectivity:
   ```bash
   kubectl run test --image=busybox -it --rm -- wget -O- http://[service-name]
   ```

### Database Connection Issues

1. Check database pod status
2. Verify connection string in secrets
3. Test database connectivity from application pod
4. Check network policies

## Alerts and Response

### Critical Alerts

| Alert | Severity | Response |
|-------|----------|----------|
| High Error Rate | Critical | Check logs, rollback if needed |
| Pod CrashLoop | High | Investigate logs, fix config |
| High Memory | Warning | Scale or optimize |
| Disk Full | Critical | Clean up logs, expand storage |

## Maintenance Windows

### Update Application

1. Build new version
2. Push to registry
3. Update deployment:
   ```bash
   kubectl set image deployment/[service-name] [container-name]=[new-image] -n {self.project_name}
   ```
4. Monitor rollout:
   ```bash
   kubectl rollout status deployment/[service-name] -n {self.project_name}
   ```

### Cluster Upgrades

1. Drain nodes one by one
2. Upgrade node
3. Uncordon node
4. Verify workload redistribution

## Backup and Recovery

### Backup

```bash
# Using Velero
velero backup create {self.project_name}-backup --include-namespaces {self.project_name}
```

### Restore

```bash
# Restore from backup
velero restore create --from-backup {self.project_name}-backup
```

## Contact Information

- On-call engineer: [pagerduty rotation]
- Team Slack: #team-{self.project_name}
- Incident channel: #incidents
"""
    
    def _get_deploy_script(self) -> str:
        return f"""#!/bin/bash
set -e

# Deploy script for {self.project_name}

NAMESPACE="{self.project_name}"
ENVIRONMENT="${{1:-dev}}"

echo "Deploying {self.project_name} to $ENVIRONMENT environment..."

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply infrastructure
echo "Applying infrastructure configurations..."
kubectl apply -f infrastructure/k8s/

# Deploy services
echo "Deploying services..."
{chr(10).join([f'kubectl apply -f services/{service}/k8s/' for service in self.services])}

# Wait for rollout
echo "Waiting for deployment to complete..."
{chr(10).join([f'kubectl rollout status deployment/{service} -n $NAMESPACE' for service in self.services])}

echo "✓ Deployment completed successfully!"
echo ""
echo "Service endpoints:"
kubectl get svc -n $NAMESPACE
"""
    
    def _get_rollback_script(self) -> str:
        return f"""#!/bin/bash
set -e

# Rollback script for {self.project_name}

NAMESPACE="{self.project_name}"
SERVICE="${{1}}"
REVISION="${{2:-0}}"

if [ -z "$SERVICE" ]; then
    echo "Usage: ./rollback.sh <service-name> [revision]"
    echo "Available services: {', '.join(self.services)}"
    exit 1
fi

echo "Rolling back $SERVICE to revision $REVISION..."

if [ "$REVISION" -eq 0 ]; then
    # Rollback to previous revision
    kubectl rollout undo deployment/$SERVICE -n $NAMESPACE
else
    # Rollback to specific revision
    kubectl rollout undo deployment/$SERVICE --to-revision=$REVISION -n $NAMESPACE
fi

# Wait for rollback to complete
kubectl rollout status deployment/$SERVICE -n $NAMESPACE

echo "✓ Rollback completed successfully!"
"""
    
    def _get_readme(self) -> str:
        return f"""# {self.project_name}

{self.description}

## Architecture

This project follows a microservices architecture pattern with the following services:

{chr(10).join([f'- **{service}**: [Add description]' for service in self.services])}

## Technology Stack

{chr(10).join([f'- {tech}' for tech in self.tech_stack])}

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl CLI tool
- Terraform for infrastructure provisioning

### Local Development

```bash
# Start all services locally
docker-compose up

# Access services
# [Add service URLs]
```

### Deploy to Kubernetes

```bash
# Deploy infrastructure
cd infrastructure/terraform
terraform init
terraform apply

# Deploy services
./scripts/deploy.sh dev
```

## Project Structure

```
.
├── services/                   # Microservices
{chr(10).join([f'│   ├── {service}/' for service in self.services])}
├── infrastructure/            # Infrastructure as Code
│   ├── terraform/            # Terraform configurations
│   └── k8s/                  # Kubernetes manifests
├── monitoring/               # Monitoring configurations
│   ├── prometheus/
│   └── grafana/
├── .github/workflows/        # CI/CD pipelines
├── docs/                     # Documentation
│   ├── architecture.md
│   ├── deployment.md
│   └── runbook.md
└── scripts/                  # Utility scripts
    ├── deploy.sh
    └── rollback.sh
```

## Documentation

- [Architecture Documentation](docs/architecture.md)
- [Deployment Guide](docs/deployment.md)
- [Runbook](docs/runbook.md)

## Monitoring

Access monitoring dashboards:
- **Grafana**: http://grafana.{self.project_name}.local
- **Prometheus**: http://prometheus.{self.project_name}.local

## CI/CD

This project uses GitHub Actions for automated CI/CD:
- Automated testing on PRs
- Security scanning with Trivy and Snyk
- Automated deployment to dev/staging/prod

## Security

- RBAC policies for service accounts
- Network policies for service isolation
- Pod security standards enforced
- Regular security scanning
- Secret management via Kubernetes Secrets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions:
- Create an issue in the repository
- Contact: [team-email]
- Slack: #team-{self.project_name}

## License

[Add license information]
"""
    
    def _get_gitignore(self) -> str:
        return """# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Terraform
*.tfstate
*.tfstate.backup
.terraform/
*.tfvars
!terraform.tfvars.example

# Kubernetes
*.kubeconfig

# Secrets
.env
*.pem
*.key
secrets.yaml

# Build outputs
dist/
build/
target/
node_modules/

# Logs
*.log
logs/

# Generated files
outputs/
"""
    
    def _get_docker_compose(self) -> str:
        services = {}
        for idx, service in enumerate(self.services, start=1):
            services[service] = f"""
  {service}:
    build: ./services/{service}
    ports:
      - "{8080 + idx}:8080"
    environment:
      - SERVICE_NAME={service}
      - ENVIRONMENT=local
"""
        
        return f"""version: '3.8'

services:
{''.join(services.values())}

networks:
  default:
    name: {self.project_name}-network
"""


class MonolithTemplate(ProjectTemplate):
    """Template for monolithic application"""
    
    def __init__(self, project_name: str, app_type: str = 'node'):
        super().__init__(project_name, "Monolithic application with Kubernetes deployment")
        self.app_type = app_type
        self.tech_stack = ["Kubernetes", "Docker", "GitHub Actions", "Terraform"]
        self._build_structure()
    
    def _build_structure(self):
        self.structure = {
            'src': {},
            'tests': {},
            'k8s': {
                'deployment.yaml': '# Kubernetes deployment',
                'service.yaml': '# Kubernetes service',
                'ingress.yaml': '# Ingress configuration',
            },
            'terraform': {
                'main.tf': '# Terraform main configuration',
            },
            '.github': {
                'workflows': {
                    'ci-cd.yaml': '# CI/CD pipeline'
                }
            },
            'Dockerfile': '# Multi-stage Dockerfile',
            'README.md': f'# {self.project_name}\n\nMonolithic application',
            '.gitignore': '# Git ignore patterns',
        }


# Factory function
def get_template(template_type: str, project_name: str, **kwargs) -> ProjectTemplate:
    """
    Factory function to get the appropriate template
    
    Args:
        template_type: Type of template ('microservices', 'monolith', 'serverless')
        project_name: Name of the project
        **kwargs: Additional parameters for specific templates
    
    Returns:
        ProjectTemplate instance
    """
    templates = {
        'microservices': MicroservicesTemplate,
        'monolith': MonolithTemplate,
    }
    
    template_class = templates.get(template_type.lower())
    if not template_class:
        raise ValueError(f"Unknown template type: {template_type}")
    
    return template_class(project_name, **kwargs)
