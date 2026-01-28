"""
Task Definitions for DevOps Automation Workflow
Defines the sequential tasks for processing deployment requests
"""

from crewai import Task
from agents import requirements_analyzer, iac_generator, validator, remediation_agent, creator_agent, developer_agent

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


def create_project_task():
    """
    Create a composite task for end-to-end project execution

    Returns:
        Task: Composite project task instance
    """
    return Task(
        description="""
        Generate a simple project based on the given programming language.
        The project should be:
        - A simple "Hello, World!" application
        - Include a README.md with instructions to run the application
        - Structured with appropriate folders (e.g., src/, tests/)
        - Use best practices for the chosen language
        - A Dockerfile to containerize the application

        Output should be a list of the files and their contents.
        It should look like: 
        [Item#1]
        [start]
        Path: <file_path>
        Content: <content here>
        [end]

        The base path should be '/workspaces/acn-dmgumagay-project-agentic-asset/outputs/<project_name>/' where <project_name> is derived from the programming language.
        
        """,
        agent=developer_agent,  # Composite task does not have a single agent
        expected_output="List of project files with paths and contents",
    )

# def create_file_task():
#     """
#     Create task for file and directory operations

#     Returns:
#         Task: File operation task instance
#     """
#     return Task(
#         description=
#         """
#         Create the files and directories as per the previous task's output.
#         Extract the path and content for each file from the previous task output and format it to use the tool properly.
#         For each item in the previous task output:
#         1. Extract the path from "Path:" (excluding the file name at the end of the path ex: outputs/project/) then MUST call the "create_directory_tool" with this value.
#         2. Extract the file name from the "Path:" and content from "Content:" then MUST call the "write_file_tool" with these values.
#         Before giving final answer, MAKE sure that [write_file_tool] and [create_directory_tool] are called for each file and directory respectively.
#         """,
#         agent=creator_agent,
#         expected_output="Return ONLY the raw results from the tool responses",
#     )