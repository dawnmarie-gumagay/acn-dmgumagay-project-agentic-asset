"""
Task Definitions for DevOps Automation Workflow
Defines the sequential tasks for processing deployment requests
"""

from crewai import Task
from agents import (
    requirements_analyzer,
    iac_generator,
    validator,
    remediation_agent
)


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
        expected_output="A structured summary of deployment requirements including app name, image, ports, replicas, and resources",
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
        expected_output="A complete, valid Kubernetes Deployment YAML manifest",
    )


def create_app_generation_task():
    """
    Create task for generating a sample codebase and dockerfile which can be used to validate
    if infrastructure runs smoothly.

    Returns:
        Task: App Generation Instance
    """
    return Task(
        description="""Generate a simple application codebase along with a Dockerfile based on the following user requirements:
        1. Application type (e.g., web server, API service)
        2. Programming language (e.g., Python, Node.js, Java)
        3. Functionality (e.g., serves "Hello World" on a specified port)
        Ensure the code is well-structured and the Dockerfile correctly sets up the environment to run the application.
        Provide instructions on how to build and run the Docker container locally for testing purposes.""",
        agent=app_generator,
        expected_output="""A simple application codebase and a Dockerfile ready for containerization and deployment.""",
    )


def create_file_creation_task():
    """
    Create task for creating application code files and Dockerfile
    Returns:
        Task: File Creation task instance
    """
    return Task(
        description=f"""Create the necessary application code files and Dockerfile based on the provided context.
        Ensure that the files are well-structured and ready for deployment in a containerized environment.
        Output a confirmation message along with the file paths where the code and Dockerfile have been saved.""",
        agent=writer_agent,
        expected_output="Confirmation of file creation along with file paths",
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
        expected_output="Validation result with either the approved manifest or a list of issues to fix",
    )


def create_monitoring_task(deployment_status):
    """
    Create task for monitoring deployment health

    Args:
        deployment_status (str): Simulated deployment status information

    Returns:
        Task: Monitoring task instance
    """
    return Task(
        description=f"""Analyze the following deployment status and determine if there are any failures:
        
        Deployment Status:
        {deployment_status}
        
        Check for common failure patterns:
        - OOMKilled: Pods killed due to out of memory
        - CrashLoopBackOff: Pods repeatedly crashing
        - ImagePullBackOff: Unable to pull container image
        - Pending: Pods stuck in pending state (resource constraints)
        - Error: General deployment errors
        
        If failures detected, respond with "FAILURE DETECTED: [failure type]" and describe the issue.
        If deployment is healthy, respond with "DEPLOYMENT HEALTHY".""",
        agent=remediation_agent,
        expected_output="Health status indicating either deployment success or specific failure type detected",
    )


def create_diagnosis_task(failure_info):
    """
    Create task for diagnosing deployment failure

    Args:
        failure_info (str): Information about the detected failure

    Returns:
        Task: Diagnosis task instance
    """
    return Task(
        description=f"""Diagnose the following deployment failure and identify the root cause:
        
        Failure Information:
        {failure_info}
        
        Provide:
        1. Root cause analysis - Why did this failure occur?
        2. Impact assessment - What is affected?
        3. Recommended fix - What specific changes are needed?
        
        Be specific and actionable in your diagnosis.""",
        agent=remediation_agent,
        expected_output="Detailed diagnosis with root cause, impact, and specific remediation steps",
    )


def create_remediation_task(diagnosis_result, original_manifest):
    """
    Create task for applying remediation fixes

    Args:
        diagnosis_result (str): Diagnosis from previous task
        original_manifest (str): The original YAML manifest that failed

    Returns:
        Task: Remediation task instance
    """
    return Task(
        description=f"""Based on the diagnosis, generate a corrected Kubernetes manifest:
        
        Diagnosis:
        {diagnosis_result}
        
        Original Manifest:
        {original_manifest}
        
        Apply the recommended fixes to create a corrected manifest. Common fixes:
        - For OOMKilled: Increase memory limits (e.g., 512Mi → 1Gi)
        - For CrashLoopBackOff: Fix configuration or add init containers
        - For ImagePullBackOff: Correct image name or add imagePullSecrets
        - For Pending: Reduce resource requests or increase replicas
        
        Output the complete corrected YAML manifest with fixes applied.""",
        agent=remediation_agent,
        expected_output="A corrected Kubernetes manifest with remediation fixes applied",
    )
