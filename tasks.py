"""
Task Definitions for DevOps Automation Workflow
Defines the sequential tasks for processing deployment requests
"""
from crewai import Task
from agents import requirements_analyzer, iac_generator, validator

def create_analysis_task(user_prompt):
    """
    Create task for analyzing user requirements
    
    Args:
        user_prompt (str): User's deployment request
        
    Returns:
        Task: Analysis task instance
    """
    return Task(
        description=f"""Analyze the following deployment request and extract key information:
        
        User Request: {user_prompt}
        
        Extract and structure the following details:
        1. Application name and type (Java, Node.js, Python, etc.)
        2. Container image (if specified, otherwise suggest a standard one)
        3. Port numbers for the application
        4. Required replicas
        5. Resource requirements (CPU, memory)
        6. Environment variables (if any)
        7. Any special configurations
        
        Provide a clear, structured summary of the deployment requirements.""",
        agent=requirements_analyzer,
        expected_output='A structured summary of deployment requirements including app name, image, ports, replicas, and resources'
    )


def create_generation_task():
    """
    Create task for generating Kubernetes manifest
    
    Returns:
        Task: Generation task instance
    """
    return Task(
        description="""Based on the analyzed requirements, generate a complete Kubernetes Deployment YAML manifest.
        
        The manifest should include:
        1. apiVersion and kind (Deployment)
        2. metadata with name and labels
        3. spec with:
           - replicas
           - selector with matchLabels
           - template with:
             - metadata with labels
             - spec with containers including:
               - name, image, ports
               - resources (requests and limits)
               - livenessProbe and readinessProbe
        
        Follow Kubernetes best practices and ensure the YAML is valid and production-ready.
        Output ONLY the YAML manifest without additional commentary.""",
        agent=iac_generator,
        expected_output='A complete, valid Kubernetes Deployment YAML manifest'
    )


def create_validation_task():
    """
    Create task for validating the generated manifest
    
    Returns:
        Task: Validation task instance
    """
    return Task(
        description="""Review the generated Kubernetes Deployment manifest and validate:
        
        1. YAML syntax is correct
        2. All required Kubernetes fields are present
        3. Resource limits are reasonable
        4. Labels and selectors match correctly
        5. Health checks are properly configured
        6. Best practices are followed
        
        If valid, respond with "VALIDATION PASSED" followed by the complete manifest.
        If issues found, list them clearly.""",
        agent=validator,
        expected_output='Validation result with either the approved manifest or a list of issues to fix'
    )
