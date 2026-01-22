"""
Main Execution Script with Self-Healing Capability
Orchestrates the DevOps automation workflow with failure detection and remediation
"""
import os
import sys
import json
import time
import logging
from datetime import datetime
from crewai import Crew, Process
from config import Config
from agents import requirements_analyzer, iac_generator, validator, remediation_agent
from tasks import (
    create_analysis_task, 
    create_generation_task, 
    create_validation_task,
    create_monitoring_task,
    create_diagnosis_task,
    create_remediation_task
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
# Set console to UTF-8 mode for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)
        logger.info(f"Created output directory: {Config.OUTPUT_DIR}")


def simulate_deployment(manifest, retry_count=0):
    """
    Simulate deployment to Kubernetes cluster
    
    Args:
        manifest (str): YAML manifest to deploy
        retry_count (int): Current retry attempt number
        
    Returns:
        tuple: (success: bool, status: str)
    """
    # Simulate deployment scenarios
    # In real implementation, this would use kubectl or Kubernetes API
    
    # For demo: First attempt fails with OOMKilled, retry succeeds
    if retry_count == 0:
        logger.info("Simulating deployment attempt...")
        time.sleep(2)  # Simulate deployment time
        return False, """
        Deployment Status: FAILED
        Pod Status:
        - java-spring-boot-78f5d4d7c-abc12: OOMKilled (Exit Code: 137)
        - java-spring-boot-78f5d4d7c-def34: OOMKilled (Exit Code: 137)
        - java-spring-boot-78f5d4d7c-ghi56: OOMKilled (Exit Code: 137)
        
        Error: Pods are being killed due to out of memory (OOMKilled).
        Current memory limit: 512Mi
        Observed memory usage: 580Mi (exceeds limit)
        """
    else:
        logger.info("Simulating deployment retry with corrected manifest...")
        time.sleep(2)
        return True, """
        Deployment Status: SUCCESS
        Pod Status:
        - java-spring-boot-78f5d4d7c-xyz12: Running (Ready 1/1)
        - java-spring-boot-78f5d4d7c-xyz34: Running (Ready 1/1)
        - java-spring-boot-78f5d4d7c-xyz56: Running (Ready 1/1)
        
        All replicas are healthy and ready to serve traffic.
        """


def run_healing_workflow(user_prompt, max_retries=3):
    """
    Run the complete workflow with self-healing capability
    
    Args:
        user_prompt (str): User's deployment request
        max_retries (int): Maximum number of healing attempts
        
    Returns:
        dict: Workflow execution results
    """
    logger.info("="*80)
    logger.info("Starting DevOps Automation with Self-Healing")
    logger.info("="*80)
    
    start_time = time.time()
    ensure_output_dir()
    
    remediation_log = {
        "timestamp": datetime.now().isoformat(),
        "user_prompt": user_prompt,
        "max_retries": max_retries,
        "attempts": []
    }
    
    # Phase 1: Generate initial manifest
    logger.info("\n📋 PHASE 1: Generating Deployment Manifest")
    logger.info("-" * 80)
    
    analysis_task = create_analysis_task(user_prompt)
    generation_task = create_generation_task()
    validation_task = create_validation_task()
    
    # Set task dependencies
    generation_task.context = [analysis_task]
    validation_task.context = [generation_task]
    
    # Create and run initial crew
    initial_crew = Crew(
        agents=[requirements_analyzer, iac_generator, validator],
        tasks=[analysis_task, generation_task, validation_task],
        process=Process.sequential,
        verbose=True
    )
    
    initial_result = initial_crew.kickoff()
    current_manifest = str(initial_result)
    
    logger.info(f"\n✅ Initial manifest generated")
    
    # Phase 2: Deploy and monitor with self-healing loop
    for attempt in range(max_retries):
        attempt_num = attempt + 1
        logger.info(f"\n🚀 PHASE 2: Deployment Attempt #{attempt_num}")
        logger.info("-" * 80)
        
        attempt_log = {
            "attempt_number": attempt_num,
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate deployment
        success, deployment_status = simulate_deployment(current_manifest, attempt)
        attempt_log["deployment_status"] = deployment_status
        
        if success:
            logger.info("\n✅ Deployment successful!")
            attempt_log["result"] = "SUCCESS"
            remediation_log["attempts"].append(attempt_log)
            remediation_log["final_status"] = "SUCCESS"
            remediation_log["total_attempts"] = attempt_num
            break
        
        logger.warning(f"\n⚠️  Deployment failed on attempt #{attempt_num}")
        attempt_log["result"] = "FAILED"
        
        # If this was the last attempt, don't try to heal
        if attempt_num >= max_retries:
            logger.error(f"\n❌ Max retries ({max_retries}) reached. Self-healing failed.")
            attempt_log["healing_attempted"] = False
            remediation_log["attempts"].append(attempt_log)
            remediation_log["final_status"] = "FAILED - Max retries exceeded"
            remediation_log["total_attempts"] = attempt_num
            break
        
        # Phase 3: Self-Healing
        logger.info(f"\n🔧 PHASE 3: Self-Healing (Attempt #{attempt_num})")
        logger.info("-" * 80)
        
        attempt_log["healing_attempted"] = True
        
        # Step 1: Monitor and detect failure
        logger.info("Step 1: Monitoring deployment health...")
        monitoring_task = create_monitoring_task(deployment_status)
        
        # Step 2: Diagnose the failure
        logger.info("Step 2: Diagnosing failure...")
        diagnosis_task = create_diagnosis_task(deployment_status)
        diagnosis_task.context = [monitoring_task]
        
        # Step 3: Apply remediation
        logger.info("Step 3: Applying remediation...")
        remediation_task = create_remediation_task(
            f"Monitoring Result: {deployment_status}", 
            current_manifest
        )
        remediation_task.context = [diagnosis_task]
        
        # Create healing crew
        healing_crew = Crew(
            agents=[remediation_agent],
            tasks=[monitoring_task, diagnosis_task, remediation_task],
            process=Process.sequential,
            verbose=True
        )
        
        healing_result = healing_crew.kickoff()
        current_manifest = str(healing_result)
        
        attempt_log["diagnosis"] = "OOMKilled - Memory limit too low"
        attempt_log["remediation"] = "Increased memory limit from 512Mi to 1Gi"
        
        logger.info(f"\n✅ Remediation applied. Preparing retry #{attempt_num + 1}...")
        
        # Calculate backoff delay
        backoff_delay = min(2 ** attempt, 8)  # 1s, 2s, 4s, 8s max
        logger.info(f"⏳ Waiting {backoff_delay}s before retry (exponential backoff)...")
        time.sleep(backoff_delay)
        
        remediation_log["attempts"].append(attempt_log)
    
    # Save results
    execution_time = time.time() - start_time
    remediation_log["execution_time_seconds"] = round(execution_time, 2)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save remediation log
    log_file = os.path.join(Config.OUTPUT_DIR, f"remediation_log_{timestamp}.json")
    with open(log_file, 'w') as f:
        json.dump(remediation_log, f, indent=2)
    logger.info(f"\n📝 Saved remediation log to: {log_file}")
    
    # Save final manifest
    manifest_file = os.path.join(Config.OUTPUT_DIR, f"healed_deployment_{timestamp}.yaml")
    with open(manifest_file, 'w') as f:
        f.write(current_manifest)
    logger.info(f"📄 Saved final manifest to: {manifest_file}")
    
    logger.info("\n" + "="*80)
    logger.info(f"Execution Time: {execution_time:.2f} seconds")
    logger.info("="*80)
    
    return remediation_log


if __name__ == "__main__":
    # Validate configuration
    Config.validate()
    
    # Default deployment request
    default_prompt = "Deploy a Java Spring Boot application with 3 replicas, needs 512Mi memory and 500m CPU"
    
    # Get user prompt from command line or use default
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        user_prompt = default_prompt
        logger.info(f"Using default prompt: {user_prompt}")
    
    logger.info(f"\nUser Request: {user_prompt}\n")
    
    # Run workflow with self-healing
    result = run_healing_workflow(user_prompt, max_retries=3)
    
    logger.info(f"\n✨ Workflow completed with status: {result['final_status']}")
