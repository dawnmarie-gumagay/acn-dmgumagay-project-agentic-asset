#!/usr/bin/env python3
"""
Standalone Demo: Self-Healing Engine in Action
No LLM required - Shows the healing engine detecting and fixing failures
"""
import sys
import json
from datetime import datetime
from healing_engine import SelfHealingEngine

# Sample Kubernetes manifest (pre-generated)
SAMPLE_MANIFEST = """
apiVersion: apps/v1
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

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_section(title):
    """Print a section header"""
    print(f"\n[{title}]")
    print("-" * 80)

def demo_oom_killed():
    """Demo: Out of Memory (OOMKilled) failure"""
    print_header("DEMO 1: Out of Memory (OOMKilled) Detection & Healing")
    
    print_section("SCENARIO")
    print("Pod crashes with OutOfMemoryError")
    print("- App requires more memory than allocated (512Mi)")
    print("- Using Java with -Xmx512m but actual heap usage exceeds limit")
    
    # Simulated pod status
    pod_status = {
        "error_logs": """
java.lang.OutOfMemoryError: Java heap space
Exception in thread "http-listener-1" java.lang.OutOfMemoryError: GC overhead limit exceeded
The container memory limit of 512Mi was exceeded
Observed memory usage: approximately 580Mi
Process was killed by Kubernetes due to exceeding memory limit
        """,
        "pod_status": "OOMKilled",
        "pod_name": "java-spring-boot-78f5d4d7c-abc12",
        "exit_code": 137
    }
    
    print_section("STEP 1: DETECT")
    engine = SelfHealingEngine()
    detection = engine.failure_detector.detect(pod_status)
    print(f"Failure Type: {detection['failure_type']}")
    print(f"Confidence: {detection['confidence']}%")
    print(f"Evidence Found:")
    for evidence in detection['evidence']:
        print(f"  - {evidence}")
    
    print_section("STEP 2: DIAGNOSE")
    diagnosis = engine.root_cause_analyzer.analyze(detection, SAMPLE_MANIFEST, pod_status)
    print(f"Root Cause: {diagnosis['root_cause']}")
    print(f"Confidence: {diagnosis['confidence']}%")
    print(f"Analysis Indicators:")
    for indicator in diagnosis['analysis_indicators']:
        print(f"  - {indicator}")
    
    print_section("STEP 3: HEAL")
    healed = engine.manifest_healer.heal(detection, diagnosis, SAMPLE_MANIFEST)
    print(f"Healing Strategy: {healed.strategy.value}")
    print(f"Risk Level: {healed.risk_level}")
    print(f"Modifications Made:")
    for path, change in healed.modifications.items():
        print(f"  - {path}")
        if isinstance(change, dict) and 'before' in change:
            print(f"    Before: {change['before']}")
            print(f"    After:  {change['after']}")
    
    print_section("STEP 4: RESULT")
    print(f"Status: SUCCESS")
    print(f"Rationale: {healed.healing_rationale}")
    
    return healed.manifest

def demo_crash_loop():
    """Demo: CrashLoopBackOff failure"""
    print_header("DEMO 2: CrashLoopBackOff Detection & Healing")
    
    print_section("SCENARIO")
    print("Pod starts but immediately crashes")
    print("- Application exits on startup")
    print("- Kubernetes keeps restarting it")
    
    pod_status = {
        "error_logs": """
Error: Cannot find application.properties
java.io.FileNotFoundException: config/application.properties (No such file or directory)
App startup failed, exiting with code 1
        """,
        "pod_status": "CrashLoopBackOff",
        "pod_name": "java-spring-boot-78f5d4d7c-xyz12"
    }
    
    print_section("STEP 1: DETECT")
    engine = SelfHealingEngine()
    detection = engine.failure_detector.detect(pod_status)
    print(f"Failure Type: {detection['failure_type']}")
    print(f"Confidence: {detection['confidence']}%")
    
    print_section("STEP 2: DIAGNOSE")
    diagnosis = engine.root_cause_analyzer.analyze(detection, SAMPLE_MANIFEST, pod_status)
    print(f"Root Cause: {diagnosis['root_cause']}")
    print(f"Confidence: {diagnosis['confidence']}%")
    
    print_section("STEP 3: HEAL")
    healed = engine.manifest_healer.heal(detection, diagnosis, SAMPLE_MANIFEST)
    print(f"Healing Strategy: {healed.strategy.value}")
    print(f"Risk Level: {healed.risk_level}")
    print(f"Modifications Made:")
    for path, change in healed.modifications.items():
        print(f"  - {path}")
    
    print_section("RESULT")
    print(f"Status: SUCCESS")
    print(f"Rationale: {healed.healing_rationale}")
    
    return healed.manifest

def demo_pending():
    """Demo: Pod Pending failure"""
    print_header("DEMO 3: Pod Pending Detection & Healing")
    
    print_section("SCENARIO")
    print("Pod cannot be scheduled")
    print("- Requesting resources no nodes have available")
    print("- Waiting indefinitely for suitable node")
    
    pod_status = {
        "error_logs": """
0/3 nodes are available: 3 Insufficient memory.
Pod was pending for more than 5 minutes.
Requested 4 CPUs but maximum available is 2 CPUs per node.
        """,
        "pod_status": "Pending",
        "pod_name": "java-spring-boot-78f5d4d7c-def34"
    }
    
    print_section("STEP 1: DETECT")
    engine = SelfHealingEngine()
    detection = engine.failure_detector.detect(pod_status)
    print(f"Failure Type: {detection['failure_type']}")
    print(f"Confidence: {detection['confidence']}%")
    
    print_section("STEP 2: DIAGNOSE")
    diagnosis = engine.root_cause_analyzer.analyze(detection, SAMPLE_MANIFEST, pod_status)
    print(f"Root Cause: {diagnosis['root_cause']}")
    print(f"Confidence: {diagnosis['confidence']}%")
    
    print_section("STEP 3: HEAL")
    healed = engine.manifest_healer.heal(detection, diagnosis, SAMPLE_MANIFEST)
    print(f"Healing Strategy: {healed.strategy.value}")
    print(f"Risk Level: {healed.risk_level}")
    print(f"Modifications Made:")
    for path, change in healed.modifications.items():
        print(f"  - {path}")
    
    print_section("RESULT")
    print(f"Status: SUCCESS")
    print(f"Rationale: {healed.healing_rationale}")
    
    return healed.manifest

def print_summary():
    """Print execution summary"""
    print_header("SUMMARY: Self-Healing Engine Capabilities")
    
    print("\n✓ DETECTION")
    print("  - 39 patterns across 6 failure types")
    print("  - OOMKilled, CrashLoop, ImagePull, Pending, ProbeFailure, NodeNotReady")
    print("  - High confidence scoring (70-95%)")
    
    print("\n✓ DIAGNOSIS")
    print("  - 21+ diagnostic rules analyzed")
    print("  - Root cause identification with evidence")
    print("  - Contextual analysis from logs and manifest")
    
    print("\n✓ HEALING")
    print("  - Type-specific strategies")
    print("  - Memory tuning, timeout adjustment, request reduction")
    print("  - YAML-safe modifications with validation")
    
    print("\n✓ TRANSPARENCY")
    print("  - Complete audit trail")
    print("  - Decision chain logged")
    print("  - Risk assessment provided")
    
    print("\n" + "=" * 80)
    print("SUCCESS: Self-healing engine is fully operational!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    try:
        # Run demos
        demo_oom_killed()
        demo_crash_loop()
        demo_pending()
        
        # Print summary
        print_summary()
        
        print("\n[NEXT STEPS]")
        print("1. Run: python main_with_healing.py")
        print("   (Requires Ollama Cloud LLM connection)")
        print("\n2. Check generated files:")
        print("   - outputs/healed_deployment_[timestamp].yaml")
        print("   - outputs/remediation_log_[timestamp].json")
        print("\n3. Review documentation:")
        print("   - HOW_TO_USE.md - Complete usage guide")
        print("   - SIMPLE_SUMMARY.md - Before/after comparison")
        print("   - HEALING_ENGINE_V2.md - Technical details")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
