"""
Advanced Self-Healing Engine for Kubernetes Deployments
Provides intelligent failure detection, diagnosis, and remediation with:
- Smart failure pattern recognition
- Root cause analysis
- Surgical manifest modifications
- Metrics-based remediation
- Full audit trail
"""
import re
import yaml
import json
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class FailureType(Enum):
    """Enumeration of Kubernetes failure types"""
    OOM_KILLED = "OOMKilled"
    CRASH_LOOP_BACKOFF = "CrashLoopBackOff"
    IMAGE_PULL_BACKOFF = "ImagePullBackOff"
    PENDING = "Pending"
    PROBE_FAILURE = "ProbeFailure"
    NODE_NOT_READY = "NodeNotReady"
    UNKNOWN = "UnknownFailure"


@dataclass
class FailurePattern:
    """Pattern for detecting specific failure types"""
    failure_type: FailureType
    signatures: List[str]  # Log patterns to match
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    healing_strategy: str  # Strategy to use for this failure


@dataclass
class DiagnosisResult:
    """Result of failure diagnosis"""
    failure_type: FailureType
    root_cause: str
    confidence: float  # 0-100
    evidence: List[str]  # Log snippets supporting diagnosis
    suggested_fixes: List[Dict]  # List of possible fixes
    severity: str


@dataclass
class RemediationAction:
    """Action taken to remediate failure"""
    timestamp: str
    failure_type: FailureType
    root_cause: str
    modifications: List[Dict]  # Fields changed in manifest
    healing_rationale: str
    risk_level: str  # LOW, MEDIUM, HIGH


class FailureDetector:
    """Detects and classifies Kubernetes failures"""
    
    # Failure patterns library
    FAILURE_PATTERNS = {
        FailureType.OOM_KILLED: FailurePattern(
            failure_type=FailureType.OOM_KILLED,
            signatures=[
                r"OOMKilled",
                r"OutOfMemory",
                r"Memory exhausted",
                r"Exit Code: 137",
                r"exit 137",
                r"Killed",
                r"exceeded memory limit"
            ],
            severity="CRITICAL",
            healing_strategy="increase_memory"
        ),
        
        FailureType.CRASH_LOOP_BACKOFF: FailurePattern(
            failure_type=FailureType.CRASH_LOOP_BACKOFF,
            signatures=[
                r"CrashLoopBackOff",
                r"Exit Code: [1-9]",
                r"exit [1-9]",
                r"exception",
                r"panic",
                r"fatal error",
                r"segmentation fault",
                r"core dumped",
                r"ERROR.*startup",
                r"application failed"
            ],
            severity="HIGH",
            healing_strategy="increase_startup_time"
        ),
        
        FailureType.IMAGE_PULL_BACKOFF: FailurePattern(
            failure_type=FailureType.IMAGE_PULL_BACKOFF,
            signatures=[
                r"ImagePullBackOff",
                r"image not found",
                r"no such image",
                r"unauthorized",
                r"pull access denied",
                r"image pull error",
                r"failed to pull image",
                r"not found: manifest"
            ],
            severity="CRITICAL",
            healing_strategy="fix_image_reference"
        ),
        
        FailureType.PENDING: FailurePattern(
            failure_type=FailureType.PENDING,
            signatures=[
                r"Pending",
                r"insufficient.*memory",
                r"insufficient.*cpu",
                r"no nodes available",
                r"node selector",
                r"taint.*toleration",
                r"PersistentVolumeClaim.*not bound"
            ],
            severity="HIGH",
            healing_strategy="reduce_requests"
        ),
        
        FailureType.PROBE_FAILURE: FailurePattern(
            failure_type=FailureType.PROBE_FAILURE,
            signatures=[
                r"readiness.*fail",
                r"liveness.*fail",
                r"health check.*fail",
                r"probe.*fail",
                r"connection refused",
                r"timeout waiting for probe",
                r"Unhealthy"
            ],
            severity="MEDIUM",
            healing_strategy="adjust_probes"
        )
    }
    
    @classmethod
    def detect(cls, error_logs: str, pod_status: str = None) -> List[FailureType]:
        """
        Detect failure types from logs
        
        Args:
            error_logs: Pod error logs
            pod_status: Pod status string (e.g., "OOMKilled")
        
        Returns:
            List of detected failure types (most likely first)
        """
        detected = []
        scores = {}
        
        logs_lower = error_logs.lower()
        
        # Score each pattern
        for failure_type, pattern in cls.FAILURE_PATTERNS.items():
            match_count = 0
            for signature in pattern.signatures:
                if re.search(signature, logs_lower, re.IGNORECASE):
                    match_count += 1
            
            if match_count > 0:
                # Confidence = percentage of signatures matched
                confidence = (match_count / len(pattern.signatures)) * 100
                scores[failure_type] = confidence
        
        # Also check pod status directly
        if pod_status:
            for failure_type, pattern in cls.FAILURE_PATTERNS.items():
                if failure_type.value in pod_status or failure_type.value.replace("_", "") in pod_status.replace(" ", ""):
                    if failure_type not in scores:
                        scores[failure_type] = 90
                    else:
                        scores[failure_type] = min(100, scores[failure_type] + 10)
        
        # Sort by confidence
        sorted_failures = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        detected = [ft for ft, _ in sorted_failures]
        
        if not detected:
            detected = [FailureType.UNKNOWN]
        
        return detected
    
    @classmethod
    def get_pattern(cls, failure_type: FailureType) -> Optional[FailurePattern]:
        """Get pattern for a failure type"""
        return cls.FAILURE_PATTERNS.get(failure_type)


class RootCauseAnalyzer:
    """Analyzes root causes of failures"""
    
    # Root cause analysis rules
    ANALYSIS_RULES = {
        FailureType.OOM_KILLED: {
            "indicators": [
                ("memory_limit_low", r"memory: (\d+)Mi", "Check if limit is less than observed usage"),
                ("java_heap", r"java.*-Xmx", "Java heap size may be too small"),
                ("memory_leak", r"gradually.*memory", "Potential memory leak in application"),
                ("concurrent_load", r"concurrent|parallel", "High concurrency may increase memory usage")
            ],
            "typical_cause": "Container memory limit insufficient for application workload"
        },
        
        FailureType.CRASH_LOOP_BACKOFF: {
            "indicators": [
                ("missing_env", r"[^_]ENV|environment.*not set", "Missing environment variables"),
                ("missing_file", r"no such file|file not found", "Missing config files or dependencies"),
                ("connection_error", r"connection.*refused|connection.*error", "Cannot connect to dependencies"),
                ("config_error", r"invalid.*config|config.*error", "Configuration error in application"),
                ("startup_error", r"failed to start|startup.*error", "Application startup failure")
            ],
            "typical_cause": "Application crashes immediately on startup due to configuration, dependencies, or code issues"
        },
        
        FailureType.IMAGE_PULL_BACKOFF: {
            "indicators": [
                ("wrong_registry", r"registry|docker.io", "Check registry configuration"),
                ("wrong_tag", r":[a-z0-9\-\.]+", "Verify image tag exists"),
                ("private_registry", r"private|auth|credentials", "Private registry needs credentials"),
                ("typo", r"latest", "Consider using specific version instead of :latest")
            ],
            "typical_cause": "Container image unavailable or inaccessible from cluster"
        },
        
        FailureType.PENDING: {
            "indicators": [
                ("high_memory", r"memory.*[0-9]+Gi", "Memory request very high"),
                ("high_cpu", r"cpu.*[0-9]+", "CPU request very high"),
                ("node_selector", r"nodeSelector|affinity", "Node selection criteria too restrictive"),
                ("pvc", r"PersistentVolumeClaim|storage", "Storage not available")
            ],
            "typical_cause": "Insufficient cluster resources to schedule pod"
        },
        
        FailureType.PROBE_FAILURE: {
            "indicators": [
                ("app_not_ready", r"startup.*slow|initialization|loading", "Application needs more startup time"),
                ("endpoint_missing", r"404|not found", "Health check endpoint doesn't exist"),
                ("port_wrong", r"port|connection refused", "Wrong port number for health checks"),
                ("timeout", r"timeout", "Probe timeout too short for endpoint response")
            ],
            "typical_cause": "Health check probe failing to receive expected response"
        }
    }
    
    @classmethod
    def analyze(cls, failure_type: FailureType, error_logs: str, manifest_yaml: str = None) -> DiagnosisResult:
        """
        Analyze root cause of failure
        
        Args:
            failure_type: Type of failure
            error_logs: Pod error logs
            manifest_yaml: Current manifest (optional, for additional context)
        
        Returns:
            DiagnosisResult with root cause analysis
        """
        logs_lower = error_logs.lower()
        
        rules = cls.ANALYSIS_RULES.get(failure_type, {})
        evidence = []
        confidence = 50
        
        # Check indicators
        if "indicators" in rules:
            indicator_matches = 0
            for indicator_name, pattern, description in rules["indicators"]:
                if re.search(pattern, logs_lower, re.IGNORECASE):
                    evidence.append(f"{indicator_name}: {description}")
                    indicator_matches += 1
            
            # Boost confidence based on indicators found
            if indicator_matches > 0:
                confidence = min(95, 50 + (indicator_matches * 15))
        
        # Check manifest for additional context
        if manifest_yaml:
            manifest_dict = yaml.safe_load(manifest_yaml)
            resources = manifest_dict.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [{}])[0].get("resources", {})
            
            if failure_type == FailureType.OOM_KILLED:
                memory_limit = resources.get("limits", {}).get("memory", "unknown")
                evidence.append(f"Manifest shows memory limit: {memory_limit}")
            elif failure_type == FailureType.PENDING:
                memory_req = resources.get("requests", {}).get("memory", "unknown")
                cpu_req = resources.get("requests", {}).get("cpu", "unknown")
                evidence.append(f"Manifest shows requests: memory={memory_req}, cpu={cpu_req}")
        
        return DiagnosisResult(
            failure_type=failure_type,
            root_cause=rules.get("typical_cause", "Unknown cause"),
            confidence=confidence,
            evidence=evidence,
            suggested_fixes=cls._generate_fixes(failure_type),
            severity=FailureDetector.get_pattern(failure_type).severity if FailureDetector.get_pattern(failure_type) else "UNKNOWN"
        )
    
    @classmethod
    def _generate_fixes(cls, failure_type: FailureType) -> List[Dict]:
        """Generate suggested fixes for a failure type"""
        fixes = {
            FailureType.OOM_KILLED: [
                {"priority": "PRIMARY", "action": "increase_memory_limit", "description": "Increase memory limit by 50-100%"},
                {"priority": "SECONDARY", "action": "increase_memory_request", "description": "Increase memory request proportionally"},
                {"priority": "TERTIARY", "action": "enable_jvm_metrics", "description": "Monitor JVM heap usage (for Java apps)"}
            ],
            FailureType.CRASH_LOOP_BACKOFF: [
                {"priority": "PRIMARY", "action": "increase_startup_delay", "description": "Increase probe initialDelaySeconds"},
                {"priority": "SECONDARY", "action": "check_dependencies", "description": "Verify dependencies are available"},
                {"priority": "TERTIARY", "action": "add_startup_probe", "description": "Add startup probe for slow-starting apps"}
            ],
            FailureType.IMAGE_PULL_BACKOFF: [
                {"priority": "PRIMARY", "action": "verify_image_name", "description": "Verify image name and registry"},
                {"priority": "SECONDARY", "action": "add_pull_secret", "description": "Add imagePullSecrets for private registries"},
                {"priority": "TERTIARY", "action": "use_explicit_tag", "description": "Use explicit image tag instead of :latest"}
            ],
            FailureType.PENDING: [
                {"priority": "PRIMARY", "action": "reduce_memory_request", "description": "Reduce memory request"},
                {"priority": "SECONDARY", "action": "reduce_cpu_request", "description": "Reduce CPU request"},
                {"priority": "TERTIARY", "action": "check_node_selectors", "description": "Review node selectors and affinity rules"}
            ],
            FailureType.PROBE_FAILURE: [
                {"priority": "PRIMARY", "action": "increase_probe_delay", "description": "Increase probe initialDelaySeconds"},
                {"priority": "SECONDARY", "action": "increase_probe_timeout", "description": "Increase probe timeoutSeconds"},
                {"priority": "TERTIARY", "action": "verify_endpoint", "description": "Verify health check endpoint exists"}
            ]
        }
        
        return fixes.get(failure_type, [])


class ManifestHealer:
    """Applies surgical fixes to Kubernetes manifests"""
    
    @staticmethod
    def parse_manifest(manifest_yaml: str) -> Dict:
        """Parse YAML manifest safely"""
        try:
            return yaml.safe_load(manifest_yaml)
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse manifest YAML: {e}")
            raise
    
    @staticmethod
    def to_yaml(manifest_dict: Dict) -> str:
        """Convert manifest dict to YAML"""
        return yaml.dump(manifest_dict, default_flow_style=False, sort_keys=False)
    
    @classmethod
    def heal_oom(cls, manifest_yaml: str, diagnosis: DiagnosisResult) -> Tuple[str, List[Dict]]:
        """Heal OOMKilled failure by increasing memory"""
        manifest_dict = cls.parse_manifest(manifest_yaml)
        modifications = []
        
        containers = manifest_dict["spec"]["template"]["spec"].get("containers", [])
        
        for container in containers:
            resources = container.get("resources", {})
            requests = resources.get("requests", {})
            
            if "memory" in requests:
                old_memory = requests["memory"]
                # Double the memory
                new_memory = cls._increase_memory(old_memory, factor=2)
                
                requests["memory"] = new_memory
                if "limits" not in resources:
                    resources["limits"] = {}
                resources["limits"]["memory"] = new_memory
                
                modifications.append({
                    "field": "spec.template.spec.containers[].resources.requests.memory",
                    "old_value": old_memory,
                    "new_value": new_memory,
                    "container": container.get("name")
                })
                
                logger.info(f"  ✓ Increased memory: {old_memory} → {new_memory}")
        
        return cls.to_yaml(manifest_dict), modifications
    
    @classmethod
    def heal_crash_loop(cls, manifest_yaml: str, diagnosis: DiagnosisResult) -> Tuple[str, List[Dict]]:
        """Heal CrashLoopBackOff by increasing startup delays"""
        manifest_dict = cls.parse_manifest(manifest_yaml)
        modifications = []
        
        containers = manifest_dict["spec"]["template"]["spec"].get("containers", [])
        
        for container in containers:
            # Increase liveness probe delay
            if "livenessProbe" in container:
                old_delay = container["livenessProbe"].get("initialDelaySeconds", 30)
                new_delay = min(old_delay + 30, 120)  # Cap at 120s
                container["livenessProbe"]["initialDelaySeconds"] = new_delay
                
                modifications.append({
                    "field": "livenessProbe.initialDelaySeconds",
                    "old_value": old_delay,
                    "new_value": new_delay,
                    "container": container.get("name")
                })
                logger.info(f"  ✓ Increased liveness delay: {old_delay}s → {new_delay}s")
            
            # Increase readiness probe delay
            if "readinessProbe" in container:
                old_delay = container["readinessProbe"].get("initialDelaySeconds", 10)
                new_delay = min(old_delay + 20, 60)
                container["readinessProbe"]["initialDelaySeconds"] = new_delay
                
                modifications.append({
                    "field": "readinessProbe.initialDelaySeconds",
                    "old_value": old_delay,
                    "new_value": new_delay,
                    "container": container.get("name")
                })
                logger.info(f"  ✓ Increased readiness delay: {old_delay}s → {new_delay}s")
            
            # Add startup probe if not present (for slow-starting apps)
            if "startupProbe" not in container:
                container["startupProbe"] = {
                    "httpGet": {
                        "path": "/health",
                        "port": container.get("ports", [{}])[0].get("containerPort", 8080)
                    },
                    "initialDelaySeconds": 0,
                    "periodSeconds": 10,
                    "timeoutSeconds": 3,
                    "failureThreshold": 30  # 5 minutes max startup time
                }
                modifications.append({
                    "field": "startupProbe",
                    "old_value": "none",
                    "new_value": "added",
                    "container": container.get("name")
                })
                logger.info(f"  ✓ Added startup probe")
        
        return cls.to_yaml(manifest_dict), modifications
    
    @classmethod
    def heal_image_pull(cls, manifest_yaml: str, diagnosis: DiagnosisResult, suggested_image: str = None) -> Tuple[str, List[Dict]]:
        """Heal ImagePullBackOff failure"""
        manifest_dict = cls.parse_manifest(manifest_yaml)
        modifications = []
        
        containers = manifest_dict["spec"]["template"]["spec"].get("containers", [])
        
        # If suggested image provided, use it
        if suggested_image:
            for container in containers:
                old_image = container.get("image", "unknown")
                container["image"] = suggested_image
                
                modifications.append({
                    "field": "image",
                    "old_value": old_image,
                    "new_value": suggested_image,
                    "container": container.get("name")
                })
                logger.info(f"  ✓ Updated image: {old_image} → {suggested_image}")
        else:
            # Try to fix image reference
            for container in containers:
                image = container.get("image", "")
                # If using :latest, suggest specific version
                if image.endswith(":latest"):
                    new_image = image.replace(":latest", ":stable")
                    container["image"] = new_image
                    
                    modifications.append({
                        "field": "image",
                        "old_value": image,
                        "new_value": new_image,
                        "container": container.get("name")
                    })
                    logger.info(f"  ✓ Changed to stable tag: {image} → {new_image}")
        
        return cls.to_yaml(manifest_dict), modifications
    
    @classmethod
    def heal_pending(cls, manifest_yaml: str, diagnosis: DiagnosisResult) -> Tuple[str, List[Dict]]:
        """Heal Pending failure by reducing resource requests"""
        manifest_dict = cls.parse_manifest(manifest_yaml)
        modifications = []
        
        containers = manifest_dict["spec"]["template"]["spec"].get("containers", [])
        
        for container in containers:
            resources = container.get("resources", {})
            requests = resources.get("requests", {})
            
            # Reduce memory
            if "memory" in requests:
                old_memory = requests["memory"]
                new_memory = cls._decrease_memory(old_memory, factor=0.5, minimum="256Mi")
                requests["memory"] = new_memory
                
                modifications.append({
                    "field": "memory request",
                    "old_value": old_memory,
                    "new_value": new_memory,
                    "container": container.get("name")
                })
                logger.info(f"  ✓ Reduced memory: {old_memory} → {new_memory}")
            
            # Reduce CPU
            if "cpu" in requests:
                old_cpu = requests["cpu"]
                new_cpu = cls._decrease_cpu(old_cpu, factor=0.5, minimum="100m")
                requests["cpu"] = new_cpu
                
                modifications.append({
                    "field": "cpu request",
                    "old_value": old_cpu,
                    "new_value": new_cpu,
                    "container": container.get("name")
                })
                logger.info(f"  ✓ Reduced CPU: {old_cpu} → {new_cpu}")
        
        return cls.to_yaml(manifest_dict), modifications
    
    @classmethod
    def heal_probe_failure(cls, manifest_yaml: str, diagnosis: DiagnosisResult) -> Tuple[str, List[Dict]]:
        """Heal probe failure by adjusting probe settings"""
        manifest_dict = cls.parse_manifest(manifest_yaml)
        modifications = []
        
        containers = manifest_dict["spec"]["template"]["spec"].get("containers", [])
        
        for container in containers:
            # Increase all probe delays and timeouts
            for probe_type in ["livenessProbe", "readinessProbe"]:
                if probe_type in container:
                    probe = container[probe_type]
                    
                    # Increase delay
                    old_delay = probe.get("initialDelaySeconds", 10)
                    new_delay = min(old_delay + 15, 60)
                    probe["initialDelaySeconds"] = new_delay
                    
                    # Increase timeout
                    old_timeout = probe.get("timeoutSeconds", 1)
                    new_timeout = min(old_timeout + 2, 10)
                    probe["timeoutSeconds"] = new_timeout
                    
                    # Increase period
                    old_period = probe.get("periodSeconds", 10)
                    new_period = min(old_period + 5, 30)
                    probe["periodSeconds"] = new_period
                    
                    modifications.append({
                        "field": f"{probe_type}",
                        "old_value": f"delay={old_delay}s, timeout={old_timeout}s",
                        "new_value": f"delay={new_delay}s, timeout={new_timeout}s",
                        "container": container.get("name")
                    })
                    logger.info(f"  ✓ Adjusted {probe_type}: delay {old_delay}→{new_delay}s")
        
        return cls.to_yaml(manifest_dict), modifications
    
    @staticmethod
    def _increase_memory(memory_str: str, factor: float = 2) -> str:
        """Increase memory value"""
        match = re.match(r"(\d+)(Mi|Gi|M|G)", memory_str)
        if match:
            value, unit = match.groups()
            new_value = int(int(value) * factor)
            return f"{new_value}{unit}"
        return memory_str
    
    @staticmethod
    def _decrease_memory(memory_str: str, factor: float = 0.5, minimum: str = "256Mi") -> str:
        """Decrease memory value"""
        match = re.match(r"(\d+)(Mi|Gi|M|G)", memory_str)
        if match:
            value, unit = match.groups()
            new_value = max(256, int(int(value) * factor))  # Never go below 256Mi
            return f"{new_value}{unit}"
        return memory_str
    
    @staticmethod
    def _decrease_cpu(cpu_str: str, factor: float = 0.5, minimum: str = "100m") -> str:
        """Decrease CPU value"""
        match = re.match(r"(\d+)(m|$)", cpu_str)
        if match:
            value = match.group(1)
            new_value = max(100, int(int(value) * factor))  # Never go below 100m
            return f"{new_value}m"
        return cpu_str


class SelfHealingEngine:
    """Main orchestrator for self-healing"""
    
    def __init__(self, max_retries: int = 3, backoff_base: int = 2):
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.audit_trail = []
    
    def diagnose_and_heal(self, error_logs: str, manifest_yaml: str, pod_status: str = None) -> Tuple[Optional[str], RemediationAction]:
        """
        Main healing pipeline: detect → diagnose → heal
        
        Args:
            error_logs: Pod error logs
            manifest_yaml: Current manifest
            pod_status: Pod status string
        
        Returns:
            Tuple of (healed_manifest, remediation_action)
        """
        logger.info("\n🔍 INTELLIGENT FAILURE DIAGNOSIS")
        logger.info("=" * 80)
        
        # Step 1: Detect failure types
        detected_failures = FailureDetector.detect(error_logs, pod_status)
        primary_failure = detected_failures[0]
        logger.info(f"Detected failure type: {primary_failure.value}")
        
        # Step 2: Root cause analysis
        diagnosis = RootCauseAnalyzer.analyze(primary_failure, error_logs, manifest_yaml)
        logger.info(f"Root cause: {diagnosis.root_cause}")
        logger.info(f"Confidence: {diagnosis.confidence}%")
        logger.info(f"Severity: {diagnosis.severity}")
        
        if diagnosis.evidence:
            logger.info("Evidence:")
            for evidence in diagnosis.evidence:
                logger.info(f"  - {evidence}")
        
        # Step 3: Apply healing
        logger.info(f"\n🛠️  APPLYING REMEDIATION")
        logger.info("-" * 80)
        
        healed_manifest = None
        modifications = []
        
        try:
            if primary_failure == FailureType.OOM_KILLED:
                healed_manifest, modifications = ManifestHealer.heal_oom(manifest_yaml, diagnosis)
            elif primary_failure == FailureType.CRASH_LOOP_BACKOFF:
                healed_manifest, modifications = ManifestHealer.heal_crash_loop(manifest_yaml, diagnosis)
            elif primary_failure == FailureType.IMAGE_PULL_BACKOFF:
                healed_manifest, modifications = ManifestHealer.heal_image_pull(manifest_yaml, diagnosis)
            elif primary_failure == FailureType.PENDING:
                healed_manifest, modifications = ManifestHealer.heal_pending(manifest_yaml, diagnosis)
            elif primary_failure == FailureType.PROBE_FAILURE:
                healed_manifest, modifications = ManifestHealer.heal_probe_failure(manifest_yaml, diagnosis)
            else:
                logger.warning(f"No healing strategy for {primary_failure.value}")
                healed_manifest = manifest_yaml
        
        except Exception as e:
            logger.error(f"Healing failed: {e}")
            healed_manifest = manifest_yaml
        
        # Create remediation record
        action = RemediationAction(
            timestamp=datetime.now().isoformat(),
            failure_type=primary_failure,
            root_cause=diagnosis.root_cause,
            modifications=modifications,
            healing_rationale=f"Applied {primary_failure.value} remediation strategy with {diagnosis.confidence}% confidence",
            risk_level=diagnosis.severity
        )
        
        self.audit_trail.append(asdict(action))
        
        logger.info(f"\n✅ Remediation applied successfully")
        logger.info(f"Total modifications: {len(modifications)}")
        
        return healed_manifest, action
    
    def get_audit_trail(self) -> List[Dict]:
        """Get complete audit trail of all healing actions"""
        return self.audit_trail
