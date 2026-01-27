"""
Simplified Self-Healing Demo
Demonstrates the healing workflow concept without long LLM calls
"""

import os
import json
import time
from datetime import datetime
from config import Config


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(Config.OUTPUT_DIR):
        os.makedirs(Config.OUTPUT_DIR)


def demo_healing_workflow():
    """
    Demonstrate self-healing workflow with simulated rapid responses
    """
    print("=" * 80)
    print("SELF-HEALING DEMO - Simplified Version")
    print("=" * 80)
    print("\nUser Prompt: Deploy a Java Spring Boot application with 3 replicas,")
    print("             needs 512Mi memory and 500m CPU\n")

    start_time = time.time()
    ensure_output_dir()

    # Initial Manifest (from Phase 1 - we already know this works)
    initial_manifest = """apiVersion: apps/v1
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
      - name: spring-boot
        image: spring-boot:latest
        ports:
          - containerPort: 8080
        resources:
          requests:
            memory: 512Mi
            cpu: 500m
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          periodSeconds: 5"""

    remediation_log = {
        "timestamp": datetime.now().isoformat(),
        "user_prompt": "Deploy a Java Spring Boot application with 3 replicas, needs 512Mi memory and 500m CPU",
        "max_retries": 3,
        "attempts": [],
    }

    current_manifest = initial_manifest

    # Attempt 1: Initial deployment fails
    print("\n" + "=" * 80)
    print("ATTEMPT #1: Initial Deployment")
    print("=" * 80)
    print("\n🚀 Deploying manifest...")
    time.sleep(1)

    print("\n❌ DEPLOYMENT FAILED!")
    print("\nPod Status:")
    print("  - java-spring-boot-78f5d4d7c-abc12: OOMKilled (Exit Code: 137)")
    print("  - java-spring-boot-78f5d4d7c-def34: OOMKilled (Exit Code: 137)")
    print("  - java-spring-boot-78f5d4d7c-ghi56: OOMKilled (Exit Code: 137)")
    print("\nError: Pods killed due to out of memory")
    print("  Current memory limit: 512Mi")
    print("  Observed memory usage: 580Mi (exceeds limit)")

    remediation_log["attempts"].append(
        {
            "attempt_number": 1,
            "timestamp": datetime.now().isoformat(),
            "deployment_status": "FAILED - OOMKilled",
            "result": "FAILED",
        }
    )

    # Self-Healing Phase
    print("\n" + "=" * 80)
    print("🔧 SELF-HEALING ACTIVATED")
    print("=" * 80)

    print("\n📊 Step 1: Monitoring - Detecting failure type...")
    time.sleep(0.5)
    print("   ✓ Failure detected: OOMKilled")

    print("\n🔍 Step 2: Diagnosing root cause...")
    time.sleep(0.5)
    print("   ✓ Root Cause: Memory limit (512Mi) insufficient")
    print("   ✓ Observed: Application needs ~580Mi")
    print("   ✓ Recommendation: Increase memory limit to 1Gi")

    print("\n🛠️  Step 3: Applying remediation...")
    time.sleep(0.5)
    print("   ✓ Modifying manifest: memory 512Mi → 1Gi")

    # Apply fix to manifest
    healed_manifest = current_manifest.replace("memory: 512Mi", "memory: 1Gi")
    healed_manifest = healed_manifest.replace(
        "requests:\n            memory: 1Gi",
        "requests:\n            memory: 1Gi\n          limits:\n            memory: 1Gi",
    )

    remediation_log["attempts"][-1]["healing_attempted"] = True
    remediation_log["attempts"][-1][
        "diagnosis"
    ] = "OOMKilled - Memory limit too low (512Mi insufficient for 580Mi usage)"
    remediation_log["attempts"][-1][
        "remediation"
    ] = "Increased memory limit from 512Mi to 1Gi"

    print("\n⏳ Exponential backoff: Waiting 1 second before retry...")
    time.sleep(1)

    # Attempt 2: Retry with fixed manifest
    print("\n" + "=" * 80)
    print("ATTEMPT #2: Deployment Retry with Corrected Manifest")
    print("=" * 80)
    print("\n🚀 Deploying updated manifest...")
    time.sleep(1)

    print("\n✅ DEPLOYMENT SUCCESSFUL!")
    print("\nPod Status:")
    print("  - java-spring-boot-9b8c7f5e2-xyz12: Running (Ready 1/1)")
    print("  - java-spring-boot-9b8c7f5e2-xyz34: Running (Ready 1/1)")
    print("  - java-spring-boot-9b8c7f5e2-xyz56: Running (Ready 1/1)")
    print("\n✓ All replicas healthy and ready to serve traffic")
    print("✓ Memory usage: 580Mi (within 1Gi limit)")

    remediation_log["attempts"].append(
        {
            "attempt_number": 2,
            "timestamp": datetime.now().isoformat(),
            "deployment_status": "SUCCESS",
            "result": "SUCCESS",
        }
    )

    remediation_log["final_status"] = "SUCCESS"
    remediation_log["total_attempts"] = 2

    execution_time = time.time() - start_time
    remediation_log["execution_time_seconds"] = round(execution_time, 2)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file = os.path.join(Config.OUTPUT_DIR, f"remediation_log_{timestamp}.json")
    with open(log_file, "w") as f:
        json.dump(remediation_log, f, indent=2)

    manifest_file = os.path.join(
        Config.OUTPUT_DIR, f"healed_deployment_{timestamp}.yaml"
    )
    with open(manifest_file, "w") as f:
        f.write(healed_manifest)

    print("\n" + "=" * 80)
    print("📝 RESULTS")
    print("=" * 80)
    print(f"\n✓ Remediation log saved: {log_file}")
    print(f"✓ Healed manifest saved: {manifest_file}")
    print(f"\n✓ Total execution time: {execution_time:.2f} seconds")
    print(f"✓ Final status: {remediation_log['final_status']}")
    print(f"✓ Total attempts: {remediation_log['total_attempts']}")

    print("\n" + "=" * 80)
    print("🎉 SELF-HEALING DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nKey Achievements:")
    print("  ✓ Detected OOMKilled failure automatically")
    print("  ✓ Diagnosed memory insufficiency (512Mi → 580Mi needed)")
    print("  ✓ Applied fix (increased to 1Gi)")
    print("  ✓ Retry succeeded on second attempt")
    print("  ✓ Full audit trail logged")

    return remediation_log


if __name__ == "__main__":
    Config.validate()
    result = demo_healing_workflow()
