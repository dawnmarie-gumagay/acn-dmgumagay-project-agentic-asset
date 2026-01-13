#!/usr/bin/env python3
"""
Simplified Main with Healing - No LLM Required
Uses pre-generated manifest and focuses on demonstrating the healing engine
"""
import os
import sys
import json
import time
import logging
from datetime import datetime
from healing_engine import SelfHealingEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pre-generated manifest (what CrewAI would normally generate)
INITIAL_MANIFEST = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: java-spring-boot
  labels:
    app: java-spring-boot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: java-spring-boot
  template:
    metadata:
      labels:
        app: java-spring-boot
    spec:
      containers:
      - name: java-spring-boot
        image: openjdk:11-jre-slim
        ports:
        - containerPort: 8080
        env:
        - name: JAVA_OPTS
          value: "-Xmx512m -Xms256m"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
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
          initialDelaySeconds: 5
          periodSeconds: 5
"""

OUTPUT_DIR = "outputs"

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logger.info(f"Created output directory: {OUTPUT_DIR}")

def simulate_deployment(manifest, retry_count=0):
    """
    Simulate Kubernetes deployment
    
    First attempt: Pod crashes with OOMKilled
    Retry attempt: Pod runs successfully
    """
    if retry_count == 0:
        logger.info("[DEPLOY] Simulating initial deployment attempt...")
        time.sleep(1)
        
        status = {
            "success": False,
            "pod_status": "OOMKilled",
            "error_logs": """java.lang.OutOfMemoryError: Java heap space
Exception in thread "http-listener-1" java.lang.OutOfMemoryError: GC overhead limit exceeded
The container memory limit of 512Mi was exceeded
Observed memory usage: approximately 580Mi""",
            "pod_name": "java-spring-boot-78f5d4d7c-abc12"
        }
        logger.warning(f"[DEPLOY] Deployment failed: {status['pod_status']}")
        return False, status
    else:
        logger.info(f"[DEPLOY] Simulating retry #{retry_count} with healed manifest...")
        time.sleep(1)
        
        status = {
            "success": True,
            "pod_status": "Running",
            "error_logs": "",
            "pod_summary": """Pod Status: Running (Ready 3/3)
  - java-spring-boot-78f5d4d7c-xyz12: Running
  - java-spring-boot-78f5d4d7c-xyz34: Running
  - java-spring-boot-78f5d4d7c-xyz56: Running
Memory usage: 620Mi (within limit)
CPU usage: 450m"""
        }
        logger.info("[DEPLOY] Deployment successful!")
        return True, status

def main():
    """Run the workflow with intelligent self-healing"""
    
    logger.info("=" * 80)
    logger.info("DEVOPS AUTOMATION WITH SELF-HEALING ENGINE")
    logger.info("=" * 80)
    
    start_time = time.time()
    ensure_output_dir()
    
    # Initialize healing engine
    healing_engine = SelfHealingEngine()
    
    remediation_log = {
        "timestamp": datetime.now().isoformat(),
        "workflow": "Simplified Demo",
        "healing_engine_version": "v2.0",
        "attempts": [],
        "final_status": None
    }
    
    # Phase 1: Start with pre-generated manifest
    logger.info("\n[PHASE 1] Using Pre-Generated Manifest")
    logger.info("-" * 80)
    current_manifest = INITIAL_MANIFEST
    logger.info("Manifest loaded (3 replicas, 512Mi memory, 500m CPU)")
    
    # Phase 2: Deployment with healing loop
    max_retries = 3
    for attempt in range(max_retries):
        attempt_num = attempt + 1
        logger.info(f"\n[PHASE 2] DEPLOYMENT ATTEMPT #{attempt_num}/{max_retries}")
        logger.info("-" * 80)
        
        attempt_log = {
            "attempt": attempt_num,
            "timestamp": datetime.now().isoformat(),
            "deployment_status": None,
            "healing_applied": False
        }
        
        # Deploy
        success, pod_status = simulate_deployment(current_manifest, attempt)
        attempt_log["deployment_status"] = pod_status["pod_status"]
        
        if success:
            logger.info("\n[SUCCESS] Deployment Successful!")
            if "pod_summary" in pod_status:
                logger.info(pod_status["pod_summary"])
            attempt_log["result"] = "SUCCESS"
            remediation_log["attempts"].append(attempt_log)
            remediation_log["final_status"] = "SUCCESS"
            remediation_log["total_attempts"] = attempt_num
            break
        
        # Deployment failed - use healing engine
        logger.warning(f"\n[FAILED] Deployment failed on attempt #{attempt_num}")
        logger.warning(f"Pod Status: {pod_status['pod_status']}")
        attempt_log["result"] = "FAILED"
        
        # Check if we should continue
        if attempt_num >= max_retries:
            logger.error(f"\n[ABORT] Max retries ({max_retries}) reached.")
            attempt_log["healing_applied"] = False
            remediation_log["attempts"].append(attempt_log)
            remediation_log["final_status"] = "FAILED - Max retries exceeded"
            remediation_log["total_attempts"] = attempt_num
            break
        
        # Phase 3: Intelligent Healing
        logger.info(f"\n[PHASE 3] INTELLIGENT HEALING (Attempt #{attempt_num})")
        logger.info("-" * 80)
        
        try:
            error_logs = pod_status.get("error_logs", "")
            pod_status_str = pod_status.get("pod_status", "Unknown")
            
            # Use healing engine
            healed_manifest, remediation = healing_engine.diagnose_and_heal(
                error_logs=error_logs,
                manifest_yaml=current_manifest,
                pod_status=pod_status_str
            )
            
            if healed_manifest and healed_manifest != current_manifest:
                current_manifest = healed_manifest
                attempt_log["healing_applied"] = True
                attempt_log["healing_details"] = {
                    "failure_type": remediation.failure_type.value,
                    "root_cause": remediation.root_cause,
                    "modifications": len(remediation.modifications),
                    "risk_level": remediation.risk_level
                }
                
                logger.info(f"[HEAL] Failure Type: {remediation.failure_type.value}")
                logger.info(f"[HEAL] Root Cause: {remediation.root_cause}")
                logger.info(f"[HEAL] Risk Level: {remediation.risk_level}")
                logger.info(f"[HEAL] Modifications: {len(remediation.modifications)}")
        
        except Exception as e:
            logger.error(f"[ERROR] Healing failed: {e}")
            import traceback
            traceback.print_exc()
            attempt_log["healing_applied"] = False
        
        # Exponential backoff
        backoff = min(2 ** attempt, 8)
        logger.info(f"\n[BACKOFF] Waiting {backoff}s before retry...")
        time.sleep(backoff)
        
        remediation_log["attempts"].append(attempt_log)
    
    # Phase 4: Save results
    execution_time = time.time() - start_time
    remediation_log["execution_time_seconds"] = round(execution_time, 2)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save log
    log_file = os.path.join(OUTPUT_DIR, f"remediation_log_{timestamp}.json")
    with open(log_file, 'w') as f:
        json.dump(remediation_log, f, indent=2)
    logger.info(f"\n[SAVE] Remediation log: {log_file}")
    
    # Save manifest
    manifest_file = os.path.join(OUTPUT_DIR, f"healed_deployment_{timestamp}.yaml")
    with open(manifest_file, 'w') as f:
        f.write(current_manifest)
    logger.info(f"[SAVE] Healed manifest: {manifest_file}")
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("EXECUTION SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Final Status: {remediation_log['final_status']}")
    logger.info(f"Total Attempts: {remediation_log.get('total_attempts', 'Unknown')}")
    logger.info(f"Execution Time: {execution_time:.2f} seconds")
    logger.info("=" * 80 + "\n")
    
    return remediation_log

if __name__ == "__main__":
    try:
        result = main()
        logger.info("Workflow completed successfully!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
