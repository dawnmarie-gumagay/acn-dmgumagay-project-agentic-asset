"""
Main Execution Script with Self-Healing Capability
Orchestrates the DevOps automation workflow with failure detection and remediation
Uses advanced healing engine for intelligent failure diagnosis and remediation
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
from healing_engine import SelfHealingEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

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
        tuple: (success: bool, status_info: dict)
    """
    # Simulate deployment scenarios
    # In real implementation, this would use kubectl or Kubernetes API
    
    # For demo: First attempt fails with OOMKilled, retry succeeds
    if retry_count == 0:
        logger.info("Simulating initial deployment attempt...")
        time.sleep(1)
        
        status_info = {
            "success": False,
            "pod_status": "OOMKilled",
            "error_logs": """
                Pod java-spring-boot-78f5d4d7c-abc12 (OOMKilled, Exit Code: 137)
                
                Error logs from previous run:
                java.lang.OutOfMemoryError: Java heap space
                Exception in thread "http-listener-1" java.lang.OutOfMemoryError: GC overhead limit exceeded
                The container memory limit of 512Mi was exceeded
                Observed memory usage: approximately 580Mi
                Process was killed by Kubernetes due to exceeding memory limit
            """,
            "pod_name": "java-spring-boot-78f5d4d7c-abc12"
        }
        return False, status_info
    else:
        logger.info("Simulating deployment retry with corrected manifest...")
        time.sleep(1)
        
        status_info = {
            "success": True,
            "pod_status": "Running",
            "error_logs": "",
            "pod_summary": """
                Pod Status: Running (Ready 1/1)
                - java-spring-boot-78f5d4d7c-xyz12: Running (Ready 1/1)
                - java-spring-boot-78f5d4d7c-xyz34: Running (Ready 1/1)
                - java-spring-boot-78f5d4d7c-xyz56: Running (Ready 1/1)
                
                All replicas are healthy and ready to serve traffic.
                Memory usage: 580Mi (within 1Gi limit)
                CPU usage: 450m (within 1000m limit)
            """
        }
        return True, status_info


def run_healing_workflow(user_prompt, max_retries=3):
    """
    Run the complete workflow with advanced self-healing capability
    
    Args:
        user_prompt (str): User's deployment request
        max_retries (int): Maximum number of healing attempts
        
    Returns:
        dict: Workflow execution results with full audit trail
    """
    logger.info("="*80)
    logger.info("DEVOPS AUTOMATION WITH ADVANCED SELF-HEALING ENGINE")
    logger.info("="*80)
    
    start_time = time.time()
    ensure_output_dir()
    
    # Initialize healing engine
    healing_engine = SelfHealingEngine(max_retries=max_retries)
    
    remediation_log = {
        "timestamp": datetime.now().isoformat(),
        "user_prompt": user_prompt,
        "max_retries": max_retries,
        "healing_engine_version": "v2.0",
        "attempts": [],
        "healing_audit_trail": []
    }
    
    # Phase 1: Generate initial manifest
    logger.info("\n[PHASE 1] GENERATING DEPLOYMENT MANIFEST")
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
    
    logger.info(f"\n[SUCCESS] Initial manifest generated successfully")
    
    # Phase 2: Deploy and monitor with intelligent self-healing loop
    for attempt in range(max_retries):
        attempt_num = attempt + 1
        logger.info(f"\n[DEPLOYMENT] ATTEMPT #{attempt_num}/{max_retries}")
        logger.info("-" * 80)
        
        attempt_log = {
            "attempt_number": attempt_num,
            "timestamp": datetime.now().isoformat(),
            "deployment_status": None,
            "diagnosis": None,
            "healing_applied": False,
            "remediation_details": None,
            "result": None
        }
        
        # Deploy manifest
        success, status_info = simulate_deployment(current_manifest, attempt)
        attempt_log["deployment_status"] = status_info.get("pod_status", "Unknown")
        
        if success:
            logger.info("\n✅ DEPLOYMENT SUCCESSFUL!")
            if "pod_summary" in status_info:
                logger.info(status_info["pod_summary"])
            attempt_log["result"] = "SUCCESS"
            remediation_log["attempts"].append(attempt_log)
            remediation_log["final_status"] = "SUCCESS"
            remediation_log["total_attempts"] = attempt_num
            break
        
        # Deployment failed - use intelligent healing engine
        logger.warning(f"\n❌ Deployment failed on attempt #{attempt_num}")
        logger.warning(f"Pod Status: {status_info.get('pod_status', 'Unknown')}")
        
        attempt_log["result"] = "FAILED"
        
        # Check if we should continue healing
        if attempt_num >= max_retries:
            logger.error(f"\n❌ Max retries ({max_retries}) reached. Giving up.")
            attempt_log["healing_applied"] = False
            remediation_log["attempts"].append(attempt_log)
            remediation_log["final_status"] = "FAILED - Max retries exceeded"
            remediation_log["total_attempts"] = attempt_num
            break
        
        # Phase 3: Intelligent Healing
        logger.info(f"\n🔧 PHASE 3: INTELLIGENT SELF-HEALING (Attempt #{attempt_num})")
        logger.info("-" * 80)
        
        error_logs = status_info.get("error_logs", "")
        pod_status = status_info.get("pod_status", "Unknown")
        
        try:
            # Use advanced healing engine
            healed_manifest, remediation_action = healing_engine.diagnose_and_heal(
                error_logs=error_logs,
                manifest_yaml=current_manifest,
                pod_status=pod_status
            )
            
            if healed_manifest:
                current_manifest = healed_manifest
                attempt_log["healing_applied"] = True
                attempt_log["remediation_details"] = {
                    "failure_type": remediation_action.failure_type.value,
                    "root_cause": remediation_action.root_cause,
                    "healing_rationale": remediation_action.healing_rationale,
                    "modifications": remediation_action.modifications,
                    "risk_level": remediation_action.risk_level
                }
                
                logger.info(f"\n✅ Remediation strategy applied successfully")
                logger.info(f"Failure type: {remediation_action.failure_type.value}")
                logger.info(f"Risk level: {remediation_action.risk_level}")
                logger.info(f"Modifications made: {len(remediation_action.modifications)}")
        
        except Exception as e:
            logger.error(f"Healing engine error: {e}")
            attempt_log["healing_applied"] = False
        
        # Calculate exponential backoff
        backoff_delay = min(2 ** attempt, 8)  # 2s, 4s, 8s max
        logger.info(f"\n⏳ Exponential backoff: waiting {backoff_delay}s before retry...")
        time.sleep(backoff_delay)
        
        remediation_log["attempts"].append(attempt_log)
    
    # Compile full audit trail
    remediation_log["healing_audit_trail"] = healing_engine.get_audit_trail()
    
    # Save results
    execution_time = time.time() - start_time
    remediation_log["execution_time_seconds"] = round(execution_time, 2)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save remediation log with full details
    log_file = os.path.join(Config.OUTPUT_DIR, f"remediation_log_{timestamp}.json")
    with open(log_file, 'w') as f:
        json.dump(remediation_log, f, indent=2)
    logger.info(f"\n📝 Saved remediation log to: {log_file}")
    
    # Save final manifest
    manifest_file = os.path.join(Config.OUTPUT_DIR, f"healed_deployment_{timestamp}.yaml")
    with open(manifest_file, 'w') as f:
        f.write(current_manifest)
    logger.info(f"📄 Saved final manifest to: {manifest_file}")
    
    # Print summary
    logger.info("\n" + "="*80)
    logger.info("EXECUTION SUMMARY")
    logger.info("="*80)
    logger.info(f"Final Status: {remediation_log['final_status']}")
    logger.info(f"Total Attempts: {remediation_log.get('total_attempts', 'Unknown')}")
    logger.info(f"Execution Time: {execution_time:.2f} seconds")
    
    if remediation_log["healing_audit_trail"]:
        logger.info(f"\nHealing Actions Taken: {len(remediation_log['healing_audit_trail'])}")
        for action in remediation_log["healing_audit_trail"]:
            logger.info(f"  - {action['failure_type']}: {action['root_cause']}")
    
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
    
    # Run workflow with advanced self-healing
    result = run_healing_workflow(user_prompt, max_retries=3)
    
    logger.info(f"\n✨ Workflow completed with status: {result['final_status']}")

