"""
Sample Kubernetes manifests for testing
Reusable test fixtures for YAML validation and parsing
"""

SIMPLE_DEPLOYMENT = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
"""

DEPLOYMENT_WITH_RESOURCES = """
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
      - name: spring-boot
        image: spring-boot:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
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
          initialDelaySeconds: 10
          periodSeconds: 5
"""

DEPLOYMENT_WITH_SECURITY_CONTEXT = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  labels:
    app: secure-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: app
        image: secure-app:v1
        ports:
        - containerPort: 8080
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
"""

DEPLOYMENT_WITH_CONFIGMAP = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-config
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        envFrom:
        - configMapRef:
            name: app-config
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
      volumes:
      - name: config-volume
        configMap:
          name: app-config
"""

INVALID_YAML = """
apiVersion: apps/v1
kind: Deployment
metadata
  name: broken-deployment
spec:
  replicas: 3
"""

INCOMPLETE_DEPLOYMENT = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: incomplete
spec:
  replicas: 2
"""

# Failure scenarios for testing self-healing
OOMKILLED_STATUS = """
Deployment Status: FAILED
Pod Status:
- app-78f5d4d7c-abc12: OOMKilled (Exit Code: 137)
- app-78f5d4d7c-def34: OOMKilled (Exit Code: 137)
- app-78f5d4d7c-ghi56: OOMKilled (Exit Code: 137)

Error: Pods are being killed due to out of memory (OOMKilled).
Current memory limit: 512Mi
Observed memory usage: 650Mi (exceeds limit)
"""

CRASHLOOP_STATUS = """
Deployment Status: FAILED
Pod Status:
- app-pod-1: CrashLoopBackOff (Restart count: 5)
- app-pod-2: CrashLoopBackOff (Restart count: 5)

Error: Application crashes on startup.
Last log: "Error: Cannot find configuration file /config/app.yaml"
"""

IMAGE_PULL_STATUS = """
Deployment Status: FAILED
Pod Status:
- app-pod-1: ImagePullBackOff
- app-pod-2: ImagePullBackOff

Error: Failed to pull image "myregistry.io/app:v1.0.0"
Reason: Image not found or unauthorized
"""

INSUFFICIENT_RESOURCES_STATUS = """
Deployment Status: FAILED
Pod Status:
- app-pod-1: Pending
- app-pod-2: Pending
- app-pod-3: Pending

Error: 0/3 nodes are available: 3 Insufficient cpu.
Requested: 2000m CPU
Available: 1500m CPU per node
"""

SUCCESS_STATUS = """
Deployment Status: SUCCESS
Pod Status:
- app-78f5d4d7c-xyz12: Running (Ready 1/1)
- app-78f5d4d7c-xyz34: Running (Ready 1/1)
- app-78f5d4d7c-xyz56: Running (Ready 1/1)

All replicas are healthy and ready to serve traffic.
"""
