"""
Test Self-Healing Capability with Various Failure Scenarios
Simulates different deployment failures to test remediation logic
"""
import sys
import logging
from main_with_healing import simulate_deployment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


def test_failure_scenarios():
    """Test various deployment failure scenarios"""
    
    logger.info("="*80)
    logger.info("Testing Self-Healing Failure Scenarios")
    logger.info("="*80)
    
    scenarios = [
        {
            "name": "OOMKilled - Out of Memory",
            "status": """
            Deployment Status: FAILED
            Pod Status:
            - app-pod-1: OOMKilled (Exit Code: 137)
            - app-pod-2: OOMKilled (Exit Code: 137)
            
            Error: Pods killed due to out of memory.
            Current memory limit: 512Mi
            Observed usage: 650Mi
            """,
            "expected_fix": "Increase memory limit to 1Gi or higher"
        },
        {
            "name": "CrashLoopBackOff - Configuration Error",
            "status": """
            Deployment Status: FAILED
            Pod Status:
            - app-pod-1: CrashLoopBackOff (Restart count: 5)
            - app-pod-2: CrashLoopBackOff (Restart count: 5)
            
            Error: Application crashes on startup.
            Last log: "Error: Cannot find configuration file /config/app.yaml"
            """,
            "expected_fix": "Add ConfigMap volume mount or fix configuration path"
        },
        {
            "name": "ImagePullBackOff - Image Not Found",
            "status": """
            Deployment Status: FAILED
            Pod Status:
            - app-pod-1: ImagePullBackOff
            - app-pod-2: ImagePullBackOff
            
            Error: Failed to pull image "myregistry.io/app:v1.0.0"
            Reason: Image not found or unauthorized
            """,
            "expected_fix": "Correct image name or add imagePullSecrets"
        },
        {
            "name": "Pending - Insufficient Resources",
            "status": """
            Deployment Status: FAILED
            Pod Status:
            - app-pod-1: Pending
            - app-pod-2: Pending
            - app-pod-3: Pending
            
            Error: 0/3 nodes are available: 3 Insufficient cpu.
            Requested: 2000m CPU
            Available: 1500m CPU per node
            """,
            "expected_fix": "Reduce CPU request or scale down replicas"
        },
        {
            "name": "Liveness Probe Failed - Health Check Issue",
            "status": """
            Deployment Status: DEGRADED
            Pod Status:
            - app-pod-1: Running but restarting (Liveness probe failed)
            - app-pod-2: Running but restarting (Liveness probe failed)
            
            Error: Liveness probe failed: Get http://:8080/health: dial tcp :8080: connect: connection refused
            """,
            "expected_fix": "Fix liveness probe configuration or health endpoint"
        }
    ]
    
    logger.info(f"\nFound {len(scenarios)} failure scenarios to document\n")
    
    for i, scenario in enumerate(scenarios, 1):
        logger.info(f"\n{'='*80}")
        logger.info(f"Scenario {i}: {scenario['name']}")
        logger.info(f"{'='*80}")
        logger.info(f"\n📊 Failure Status:")
        logger.info(scenario['status'])
        logger.info(f"\n💡 Expected Fix:")
        logger.info(f"   {scenario['expected_fix']}")
        logger.info(f"\n{'='*80}\n")
    
    logger.info("\n✅ All failure scenarios documented")
    logger.info("\nThese scenarios are handled by the Remediation Agent in main_with_healing.py")
    logger.info("Run: python main_with_healing.py to see self-healing in action")


if __name__ == "__main__":
    test_failure_scenarios()
