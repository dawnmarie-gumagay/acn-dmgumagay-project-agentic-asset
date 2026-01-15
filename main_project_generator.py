"""
Complete DevOps Project Generator - Like Claude Code
Generates full-stack DevOps projects beyond just Kubernetes YAML files
"""
import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from crewai import Crew, Process, Task
from config import Config
from agents import (
    requirements_analyzer, architecture_agent, infrastructure_agent,
    cicd_agent, monitoring_agent, security_agent, documentation_agent,
    iac_generator, validator
)
from project_templates import get_template, MicroservicesTemplate
from utils.file_generator import ProjectGenerator, generate_readme, generate_gitignore
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('project_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def create_comprehensive_project_tasks(user_requirements: str):
    """
    Create comprehensive tasks for full project generation
    
    Args:
        user_requirements: User's project requirements
    
    Returns:
        List of Task objects
    """
    
    # Task 1: Analyze Requirements and Design Architecture
    architecture_task = Task(
        description=f"""Analyze the following project requirements and design a comprehensive architecture:
        
        Requirements: {user_requirements}
        
        Provide:
        1. Recommended architecture pattern (microservices, monolith, serverless)
        2. List of services/components needed
        3. Technology stack recommendations
        4. Database and storage requirements
        5. Communication patterns between components
        6. Scalability and resilience strategies
        
        Output a structured JSON with your recommendations.""",
        agent=architecture_agent,
        expected_output='JSON with architecture design including pattern, services, tech stack, and strategies'
    )
    
    # Task 2: Generate Infrastructure Code
    infrastructure_task = Task(
        description="""Based on the architecture design, generate Terraform infrastructure code:
        
        Generate:
        1. Terraform main.tf with provider configuration
        2. Variables.tf with customizable parameters
        3. Kubernetes cluster configuration (if needed)
        4. Networking setup (VPC, subnets, security groups)
        5. Storage resources (if needed)
        
        Provide complete, production-ready Terraform code.""",
        agent=infrastructure_agent,
        expected_output='Complete Terraform code for infrastructure provisioning',
        context=[architecture_task]
    )
    
    # Task 3: Generate Kubernetes Manifests
    k8s_task = Task(
        description="""Generate comprehensive Kubernetes manifests for all services:
        
        For each service, create:
        1. Deployment with proper resource limits and health checks
        2. Service for network access
        3. ConfigMap for configuration
        4. ServiceAccount and RBAC policies
        5. NetworkPolicy for isolation
        
        Follow Kubernetes best practices.""",
        agent=iac_generator,
        expected_output='Complete set of Kubernetes YAML manifests for all services',
        context=[architecture_task]
    )
    
    # Task 4: Generate CI/CD Pipeline
    cicd_task = Task(
        description="""Create comprehensive CI/CD pipeline configuration:
        
        Generate GitHub Actions workflows for:
        1. Build and test on PRs
        2. Security scanning (Trivy, Snyk)
        3. Container image build and push
        4. Deployment to environments (dev, staging, prod)
        5. Rollback procedures
        6. Integration and smoke tests
        
        Include environment promotion strategy.""",
        agent=cicd_agent,
        expected_output='Complete GitHub Actions workflow files for CI/CD',
        context=[architecture_task]
    )
    
    # Task 5: Generate Monitoring Configuration
    monitoring_task = Task(
        description="""Create comprehensive monitoring and observability setup:
        
        Generate:
        1. Prometheus configuration and ServiceMonitors
        2. Grafana dashboard JSON
        3. Alert rules for critical metrics
        4. SLO/SLI definitions
        5. Log aggregation configuration
        
        Include dashboards for RED and USE metrics.""",
        agent=monitoring_agent,
        expected_output='Complete monitoring stack configuration with Prometheus, Grafana, and alert rules',
        context=[architecture_task]
    )
    
    # Task 6: Generate Security Configurations
    security_task = Task(
        description="""Generate security and compliance configurations:
        
        Create:
        1. RBAC roles and bindings for services
        2. Network policies for service isolation
        3. Pod security policies/standards
        4. Secret management setup
        5. Security scanning configurations
        
        Follow zero-trust security principles.""",
        agent=security_agent,
        expected_output='Complete security configurations including RBAC, network policies, and pod security',
        context=[architecture_task, k8s_task]
    )
    
    # Task 7: Generate Documentation
    documentation_task = Task(
        description="""Create comprehensive technical documentation:
        
        Generate:
        1. README.md with overview and quick start
        2. Architecture documentation with diagrams
        3. Deployment guide with step-by-step instructions
        4. Runbook for operations and troubleshooting
        5. API documentation (if applicable)
        
        Make documentation clear, complete, and maintainable.""",
        agent=documentation_agent,
        expected_output='Complete documentation set including README, architecture docs, deployment guide, and runbook',
        context=[architecture_task, k8s_task, cicd_task, monitoring_task]
    )
    
    # Task 8: Validate Everything
    validation_task = Task(
        description="""Validate all generated configurations:
        
        Check:
        1. YAML syntax correctness
        2. Terraform syntax validation
        3. Security best practices compliance
        4. Resource configurations
        5. Complete coverage of requirements
        
        Provide validation report.""",
        agent=validator,
        expected_output='Validation report confirming correctness of all generated artifacts',
        context=[infrastructure_task, k8s_task, cicd_task, monitoring_task, security_task]
    )
    
    return [
        architecture_task,
        infrastructure_task,
        k8s_task,
        cicd_task,
        monitoring_task,
        security_task,
        documentation_task,
        validation_task
    ]


def generate_project(user_requirements: str, output_dir: str, template_type: str = 'microservices'):
    """
    Generate complete DevOps project
    
    Args:
        user_requirements: User's project requirements
        output_dir: Directory where project will be generated
        template_type: Type of project template to use
    
    Returns:
        dict: Generation summary
    """
    logger.info("="*80)
    logger.info("Starting Complete DevOps Project Generation")
    logger.info("="*80)
    logger.info(f"User Requirements: {user_requirements}")
    logger.info(f"Output Directory: {output_dir}")
    logger.info(f"Template Type: {template_type}")
    
    start_time = datetime.now()
    
    # Validate configuration
    Config.validate()
    
    # Phase 1: Run AI agents to generate configurations
    logger.info("\n📋 Phase 1: AI-Powered Configuration Generation")
    logger.info("-"*80)
    
    tasks = create_comprehensive_project_tasks(user_requirements)
    
    crew = Crew(
        agents=[
            architecture_agent,
            infrastructure_agent,
            iac_generator,
            cicd_agent,
            monitoring_agent,
            security_agent,
            documentation_agent,
            validator
        ],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # Execute crew
    logger.info("Executing AI agent workflow...")
    crew_result = crew.kickoff()
    
    logger.info("\n✅ AI generation completed")
    
    # Phase 2: Parse AI output and extract components
    logger.info("\n🔧 Phase 2: Extracting and Organizing Generated Content")
    logger.info("-"*80)
    
    # Parse the crew result to extract different components
    result_str = str(crew_result)
    
    # Extract services from requirements (simplified - in production, parse from AI output)
    # For demo, we'll use a template approach
    services = extract_services_from_requirements(user_requirements)
    project_name = extract_project_name(user_requirements)
    
    logger.info(f"Project Name: {project_name}")
    logger.info(f"Services Identified: {', '.join(services)}")
    
    # Phase 3: Generate project structure using template
    logger.info("\n🏗️ Phase 3: Building Project Structure")
    logger.info("-"*80)
    
    # Get the appropriate template
    template = get_template(
        template_type,
        project_name,
        services=services,
        use_service_mesh=True
    )
    
    # Create project generator
    project_gen = ProjectGenerator(output_dir)
    
    # Generate complete project structure
    structure = template.get_structure()
    project_gen.create_directory_structure(structure)
    
    # Save project metadata
    metadata = {
        'project_name': project_name,
        'template_type': template_type,
        'services': services,
        'tech_stack': template.get_tech_stack(),
        'generated_at': datetime.now().isoformat(),
        'user_requirements': user_requirements,
        'ai_model': Config.DEFAULT_MODEL
    }
    
    project_gen.create_file('project-metadata.json', json.dumps(metadata, indent=2))
    
    # Phase 4: Save AI-generated content
    logger.info("\n💾 Phase 4: Saving AI-Generated Configurations")
    logger.info("-"*80)
    
    # Save the full AI output for reference
    project_gen.create_file(
        'ai-generated/full-output.txt',
        result_str
    )
    
    # Save summary
    project_gen.save_summary()
    summary = project_gen.get_summary()
    
    execution_time = (datetime.now() - start_time).total_seconds()
    
    logger.info("\n"+"="*80)
    logger.info("✅ PROJECT GENERATION COMPLETED")
    logger.info("="*80)
    logger.info(f"Project: {project_name}")
    logger.info(f"Location: {output_dir}")
    logger.info(f"Files Created: {summary['total_files']}")
    logger.info(f"Directories Created: {summary['total_directories']}")
    logger.info(f"Execution Time: {execution_time:.2f} seconds")
    logger.info("="*80)
    
    return {
        'project_name': project_name,
        'output_dir': output_dir,
        'summary': summary,
        'metadata': metadata,
        'execution_time': execution_time,
        'status': 'success'
    }


def extract_services_from_requirements(requirements: str) -> list:
    """
    Extract service names from requirements
    Simple implementation - in production, this would use NLP
    
    Args:
        requirements: User requirements string
    
    Returns:
        List of service names
    """
    # Simple keyword extraction
    services = []
    keywords = {
        'api': 'api-service',
        'frontend': 'frontend-service',
        'backend': 'backend-service',
        'auth': 'auth-service',
        'user': 'user-service',
        'payment': 'payment-service',
        'notification': 'notification-service',
        'database': 'database-service',
        'cache': 'cache-service',
        'gateway': 'gateway-service'
    }
    
    req_lower = requirements.lower()
    for keyword, service in keywords.items():
        if keyword in req_lower:
            services.append(service)
    
    # Default services if none found
    if not services:
        services = ['api-service', 'web-service']
    
    return services


def extract_project_name(requirements: str) -> str:
    """
    Extract or generate project name from requirements
    
    Args:
        requirements: User requirements string
    
    Returns:
        Project name
    """
    # Simple implementation - look for project name patterns
    words = requirements.split()
    
    # Look for "project", "app", "platform", etc.
    for i, word in enumerate(words):
        if word.lower() in ['project', 'app', 'platform', 'system', 'service']:
            if i + 1 < len(words):
                return words[i + 1].lower().replace(' ', '-')
    
    # Default name
    return 'my-devops-project'


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Complete DevOps Project Generator - Like Claude Code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Create a microservices e-commerce platform with user, product, and payment services"
  %(prog)s "Build a Node.js API with authentication, database, and caching" --output ./my-project
  %(prog)s "Deploy a Python web app with monitoring and CI/CD" --template monolith
        """
    )
    
    parser.add_argument(
        'requirements',
        nargs='*',
        help='Project requirements as natural language description'
    )
    
    parser.add_argument(
        '--requirements', '-r',
        dest='requirements_flag',
        help='Alternative way to specify requirements'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='./generated-projects/project-' + datetime.now().strftime('%Y%m%d-%H%M%S'),
        help='Output directory for generated project'
    )
    
    parser.add_argument(
        '--template', '-t',
        choices=['microservices', 'monolith'],
        default='microservices',
        help='Project template type'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without creating files'
    )
    
    args = parser.parse_args()
    
    # Determine requirements
    if args.requirements_flag:
        user_requirements = args.requirements_flag
    elif args.requirements:
        user_requirements = ' '.join(args.requirements)
    else:
        user_requirements = "Create a microservices application with API gateway, user service, and product service. Include monitoring, CI/CD, and security configurations."
        logger.info("No requirements provided, using default example")
    
    print("\n" + "="*80)
    print("🚀 Complete DevOps Project Generator (Like Claude Code)")
    print("="*80)
    print(f"\n📝 Requirements: {user_requirements}")
    print(f"📁 Output Directory: {args.output}")
    print(f"📋 Template: {args.template}")
    print()
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be created")
        print("\nWould generate:")
        print("  - Complete project structure")
        print("  - Kubernetes manifests")
        print("  - Terraform infrastructure code")
        print("  - CI/CD pipelines")
        print("  - Monitoring configurations")
        print("  - Security policies")
        print("  - Documentation")
        return
    
    try:
        result = generate_project(
            user_requirements=user_requirements,
            output_dir=args.output,
            template_type=args.template
        )
        
        print("\n" + "="*80)
        print("✅ PROJECT GENERATED SUCCESSFULLY")
        print("="*80)
        print(f"\n📦 Project: {result['project_name']}")
        print(f"📁 Location: {result['output_dir']}")
        print(f"📄 Files: {result['summary']['total_files']}")
        print(f"📂 Directories: {result['summary']['total_directories']}")
        print(f"⏱️  Time: {result['execution_time']:.2f} seconds")
        
        print("\n📚 What was generated:")
        print("  ✓ Kubernetes manifests for all services")
        print("  ✓ Terraform infrastructure code")
        print("  ✓ CI/CD pipelines (GitHub Actions)")
        print("  ✓ Monitoring stack (Prometheus + Grafana)")
        print("  ✓ Security configurations (RBAC, Network Policies)")
        print("  ✓ Complete documentation (README, guides, runbooks)")
        print("  ✓ Deployment and rollback scripts")
        
        print("\n🚀 Next Steps:")
        print(f"  1. cd {result['output_dir']}")
        print("  2. Review the generated files")
        print("  3. Customize for your specific needs")
        print("  4. Follow docs/deployment.md to deploy")
        
        print("\n" + "="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        print(f"\n✗ Error: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
