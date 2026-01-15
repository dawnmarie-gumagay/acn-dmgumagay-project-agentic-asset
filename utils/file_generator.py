"""
File and Directory Generation Utilities
Handles creation of complete project structures with multiple files
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class ProjectGenerator:
    """Generates complete project directory structures with multiple files"""
    
    def __init__(self, base_path: str):
        """
        Initialize project generator
        
        Args:
            base_path: Base directory where project will be created
        """
        self.base_path = Path(base_path)
        self.created_files = []
        self.created_dirs = []
    
    def create_directory_structure(self, structure: Dict[str, Any]):
        """
        Create nested directory structure
        
        Args:
            structure: Dictionary representing directory structure
                      {'dir_name': {'subdir': {}, 'file.txt': 'content'}}
        """
        def _create_recursive(current_path: Path, struct: Dict):
            for name, content in struct.items():
                item_path = current_path / name
                
                if isinstance(content, dict):
                    # It's a directory
                    item_path.mkdir(parents=True, exist_ok=True)
                    self.created_dirs.append(str(item_path))
                    logger.info(f"Created directory: {item_path}")
                    _create_recursive(item_path, content)
                elif isinstance(content, str):
                    # It's a file with content
                    item_path.parent.mkdir(parents=True, exist_ok=True)
                    item_path.write_text(content)
                    self.created_files.append(str(item_path))
                    logger.info(f"Created file: {item_path}")
        
        self.base_path.mkdir(parents=True, exist_ok=True)
        _create_recursive(self.base_path, structure)
    
    def create_file(self, relative_path: str, content: str):
        """
        Create a single file at the specified path
        
        Args:
            relative_path: Path relative to base_path
            content: File content
        """
        file_path = self.base_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        self.created_files.append(str(file_path))
        logger.info(f"Created file: {file_path}")
    
    def create_files_from_dict(self, files: Dict[str, str]):
        """
        Create multiple files from a dictionary
        
        Args:
            files: Dictionary of {relative_path: content}
        """
        for path, content in files.items():
            self.create_file(path, content)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of created files and directories
        
        Returns:
            Dictionary with creation summary
        """
        return {
            'base_path': str(self.base_path),
            'total_files': len(self.created_files),
            'total_directories': len(self.created_dirs),
            'files': self.created_files,
            'directories': self.created_dirs
        }
    
    def save_summary(self, output_file: str = 'project_structure.json'):
        """
        Save project structure summary to JSON file
        
        Args:
            output_file: Output filename
        """
        summary = self.get_summary()
        output_path = self.base_path / output_file
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Saved project summary to: {output_path}")


def generate_readme(project_name: str, description: str, 
                   tech_stack: List[str], setup_steps: List[str]) -> str:
    """
    Generate README.md content
    
    Args:
        project_name: Name of the project
        description: Project description
        tech_stack: List of technologies used
        setup_steps: Setup instructions
    
    Returns:
        README content as string
    """
    tech_list = '\n'.join([f"- {tech}" for tech in tech_stack])
    steps_list = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(setup_steps)])
    
    return f"""# {project_name}

{description}

## Technology Stack

{tech_list}

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl CLI tool
- Helm 3+

## Quick Start

{steps_list}

## Project Structure

```
.
├── k8s/                    # Kubernetes manifests
├── terraform/              # Infrastructure as Code
├── .github/workflows/      # CI/CD pipelines
├── monitoring/             # Monitoring configurations
├── docs/                   # Documentation
└── README.md              # This file
```

## Deployment

### Local Development

```bash
# Build and run locally
docker-compose up

# Access the application
http://localhost:8080
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n {project_name.lower().replace(' ', '-')}
```

## Monitoring

Access monitoring dashboards:
- Grafana: http://grafana.example.com
- Prometheus: http://prometheus.example.com

## Security

This project implements:
- RBAC policies
- Network policies
- Pod security policies
- Secret management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For issues and questions, please open an issue in the repository.
"""


def generate_gitignore(project_type: str = 'general') -> str:
    """
    Generate .gitignore content based on project type
    
    Args:
        project_type: Type of project (general, python, node, java)
    
    Returns:
        .gitignore content
    """
    base_ignore = """# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Terraform
*.tfstate
*.tfstate.backup
.terraform/
*.tfvars

# Kubernetes
*.kubeconfig

# Secrets
.env
*.pem
*.key
secrets.yaml

# Outputs
outputs/
logs/
*.log
"""
    
    python_ignore = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
"""
    
    node_ignore = """
# Node
node_modules/
npm-debug.log
yarn-error.log
.npm
dist/
build/
"""
    
    java_ignore = """
# Java
target/
*.class
*.jar
*.war
.gradle/
build/
"""
    
    if project_type == 'python':
        return base_ignore + python_ignore
    elif project_type == 'node':
        return base_ignore + node_ignore
    elif project_type == 'java':
        return base_ignore + java_ignore
    else:
        return base_ignore


def generate_dockerfile(app_type: str, port: int = 8080) -> str:
    """
    Generate Dockerfile based on application type
    
    Args:
        app_type: Application type (node, python, java, go)
        port: Application port
    
    Returns:
        Dockerfile content
    """
    dockerfiles = {
        'node': f"""FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app .

EXPOSE {port}

USER node

CMD ["node", "index.js"]
""",
        'python': f"""FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app .

EXPOSE {port}

USER nobody

CMD ["python", "app.py"]
""",
        'java': f"""FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

COPY pom.xml .
RUN mvn dependency:go-offline

COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

COPY --from=builder /app/target/*.jar app.jar

EXPOSE {port}

USER nobody

ENTRYPOINT ["java", "-jar", "app.jar"]
""",
        'go': f"""FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/main .

EXPOSE {port}

USER nobody

CMD ["./main"]
"""
    }
    
    return dockerfiles.get(app_type, dockerfiles['node'])


if __name__ == "__main__":
    # Test project generation
    import tempfile
    import shutil
    
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        generator = ProjectGenerator(os.path.join(temp_dir, 'test-project'))
        
        # Create sample structure
        structure = {
            'k8s': {
                'deployment.yaml': 'apiVersion: apps/v1\nkind: Deployment',
                'service.yaml': 'apiVersion: v1\nkind: Service'
            },
            'terraform': {
                'main.tf': '# Terraform configuration',
                'variables.tf': '# Variables'
            },
            '.github': {
                'workflows': {
                    'ci.yaml': '# CI workflow'
                }
            },
            'README.md': generate_readme(
                'Test Project',
                'A test project',
                ['Kubernetes', 'Terraform'],
                ['Clone repository', 'Run setup']
            ),
            '.gitignore': generate_gitignore('python'),
            'Dockerfile': generate_dockerfile('node')
        }
        
        generator.create_directory_structure(structure)
        generator.save_summary()
        
        summary = generator.get_summary()
        print(f"✓ Created {summary['total_files']} files")
        print(f"✓ Created {summary['total_directories']} directories")
        print(f"✓ Base path: {summary['base_path']}")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print("✓ Test completed and cleaned up")
