# Kubernetes Mutating Admission Webhook

A production-ready Kubernetes Mutating Admission Webhook that automatically injects annotations into Kubernetes resources. Built with FastAPI and implementing Clean Architecture principles with comprehensive testing, dependency injection, and modern Python development practices.

## Overview

This webhook automatically adds the annotation `example.com/injected: "true"` to Kubernetes resources during admission. It can be configured to either add the annotation only when missing or overwrite existing values based on the `OVERWRITE` environment variable.

## Architecture Overview

This project follows **Clean Architecture** (also known as Hexagonal Architecture or Ports and Adapters) to ensure maintainability, testability, and separation of concerns.

### Design Patterns Implemented

#### 1. Clean Architecture Layers

```
┌─────────────────────────────────────────┐
│              API Layer                   │
│  (Webhook routes, schemas, server)      │
├─────────────────────────────────────────┤
│            Application Layer             │
│   (Mutation handlers, Use Cases, DI)   │
├─────────────────────────────────────────┤
│             Domain Layer                 │
│   (Admission models, Interfaces)        │
├─────────────────────────────────────────┤
│           Infrastructure Layer           │
│    (Kubernetes API integration)         │
└─────────────────────────────────────────┘
```

**Domain Layer** (`app/domain/`)

- Contains admission review models and business rules
- Independent of external frameworks
- Defines interfaces for mutation logic

**Application Layer** (`app/handlers/`)

- Contains mutation use cases and business logic orchestration
- Implements annotation injection rules
- Depends only on the domain layer

**Infrastructure Layer** (`app/infra/`)

- Implements domain interfaces
- Contains Kubernetes API integration logic
- Framework-specific implementations

**API Layer** (`app/api/`)

- Webhook HTTP request/response handling
- Admission review validation and serialization
- Route definitions for mutation endpoint

#### 2. Webhook Request Processing

The webhook processes Kubernetes admission review requests through a clean pipeline:

```python
# app/api/routes/webhook.py
@router.post("", response_model=AdmissionReviewResponse)
def create_item(body: AdmissionReviewRequest):
    target_key = "example.com/injected"
    target_value = "true"
    patch_ops = []
    
    # Extract admission review data
    annotations = body.annotations
    uid = body.uid
    
    # Apply mutation logic
    if annotations is None:
        patch_ops.append({
            "op": "add",
            "path": "/metadata/annotations",
            "value": {target_key: target_value}
        })
    
    # Return admission response with patches
    return AdmissionReviewResponse(...)
```

#### 3. Admission Review Models

Strict typing for Kubernetes admission review objects:

```python
# app/api/schemas.py
class AdmissionReviewRequest(BaseModel):
    uid: str = Field(min_length=1, max_length=100)
    obj: dict = Field(description="Kubernetes object")
    metadata: dict = Field(description="Object metadata")
    annotations: Optional[dict] = Field(description="Object annotations")

class AdmissionResponse(BaseModel):
    uid: str
    allowed: bool
    patch: Optional[str] = None
    patchType: Optional[str] = Field(default="JSONPatch")
```

## Project Structure

```
app/
├── api/                    # API Layer
│   ├── di.py              # Dependency Injection Container
│   ├── routes/            # HTTP Route Handlers
│   │   └── webhook.py     # Webhook mutation endpoint
│   ├── schemas.py         # Admission Review Models
│   └── server.py          # FastAPI Application Setup
├── domain/                # Domain Layer
│   └── (domain models)    # Admission review entities
├── handlers/              # Application Layer
│   └── (mutation logic)   # Mutation use case handlers
├── infra/                 # Infrastructure Layer
│   └── (k8s integration)  # Kubernetes API integration
└── tools/                 # Shared Utilities
    └── validator.py       # Validation Helpers

tests/
├── conftest.py            # Test Configuration
└── test_*.py              # Unit and Integration Tests

# Additional files
├── Dockerfile             # Container image definition
├── compose.yaml           # Docker Compose configuration
├── Makefile              # Development commands
└── pyproject.toml        # Python project configuration
```

## Webhook API

### Mutation Endpoint

The webhook exposes a single endpoint that receives Kubernetes admission review requests:

```bash
POST /mutate
Content-Type: application/json

{
  "uid": "12345678-1234-1234-1234-123456789012",
  "obj": {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
      "name": "example-pod",
      "namespace": "default"
    }
  },
  "metadata": {
    "name": "example-pod",
    "namespace": "default"
  },
  "annotations": null
}
```

### Response (Adding Annotation)

When the annotation is missing, the webhook responds with a patch to add it:

```json
{
  "apiVersion": "admission.k8s.io/v1",
  "kind": "AdmissionReview",
  "response": {
    "uid": "12345678-1234-1234-1234-123456789012",
    "allowed": true,
    "patch": "W3sib3AiOiJhZGQiLCJwYXRoIjoiL21ldGFkYXRhL2Fubm90YXRpb25zIiwidmFsdWUiOnsiZXhhbXBsZS5jb20vaW5qZWN0ZWQiOiJ0cnVlIn19XQ==",
    "patchType": "JSONPatch"
  }
}
```

### Response (No Changes Needed)

When the annotation already exists and `OVERWRITE=false`, no patch is applied:

```json
{
  "apiVersion": "admission.k8s.io/v1",
  "kind": "AdmissionReview",
  "response": {
    "uid": "12345678-1234-1234-1234-123456789012",
    "allowed": true
  }
}
```

### Environment Variables

- **`OVERWRITE`**: Set to `"true"`, `"1"`, or `"yes"` to overwrite existing annotations. Default: `"false"`

## Getting Started

### Prerequisites

- Python 3.12+
- uv (Python package manager)
- Docker (for containerized deployment)
- Kubernetes cluster (for webhook deployment)

### Local Development

1. Clone the repository:

```bash
git clone <repository-url>
cd webhookmuttating-example
```

2. Install dependencies:

```bash
make install
# or
uv sync
```

### Running the Application

#### Development Mode

```bash
make run
# or
ENVIRONMENT=local uv run python main.py
```

#### Production Mode

```bash
make run-prod
# or
uv run python main.py
```

The webhook will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

### Kubernetes Deployment

#### 1. Build and Push Container Image

```bash
# Build the image
docker build -t your-registry/webhookmuttating-example:latest .

# Push to your container registry
docker push your-registry/webhookmuttating-example:latest
```

#### 2. Create TLS Certificate

The webhook requires TLS. Create a certificate and key:

```bash
# Generate a private key
openssl genrsa -out webhook.key 2048

# Create a certificate signing request
openssl req -new -key webhook.key -out webhook.csr -subj "/CN=webhook-service.default.svc"

# Generate the certificate (self-signed for development)
openssl x509 -req -in webhook.csr -signkey webhook.key -out webhook.crt -days 365

# Create Kubernetes secret
kubectl create secret tls webhook-certs --cert=webhook.crt --key=webhook.key
```

#### 3. Deploy the Webhook

Create a deployment manifest (`k8s-deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webhook-deployment
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webhook
  template:
    metadata:
      labels:
        app: webhook
    spec:
      containers:
      - name: webhook
        image: your-registry/webhookmuttating-example:latest
        ports:
        - containerPort: 8000
        env:
        - name: OVERWRITE
          value: "false"
        volumeMounts:
        - name: certs
          mountPath: /etc/certs
          readOnly: true
      volumes:
      - name: certs
        secret:
          secretName: webhook-certs
---
apiVersion: v1
kind: Service
metadata:
  name: webhook-service
  namespace: default
spec:
  selector:
    app: webhook
  ports:
  - port: 443
    targetPort: 8000
    protocol: TCP
---
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingAdmissionWebhook
metadata:
  name: annotation-injector
webhooks:
- name: inject-annotation.example.com
  clientConfig:
    service:
      name: webhook-service
      namespace: default
      path: /mutate
    caBundle: LS0tLS1CRUdJTi... # Base64 encoded CA certificate
  rules:
  - operations: ["CREATE", "UPDATE"]
    apiGroups: [""]
    apiVersions: ["v1"]
    resources: ["pods"]
  admissionReviewVersions: ["v1"]
  sideEffects: None
  failurePolicy: Fail
```

Apply the deployment:

```bash
kubectl apply -f k8s-deployment.yaml
```

#### 4. Test the Webhook

Create a test pod to verify the webhook is working:

```bash
kubectl run test-pod --image=nginx --dry-run=client -o yaml | kubectl apply -f -

# Check if the annotation was added
kubectl get pod test-pod -o jsonpath='{.metadata.annotations.example\.com/injected}'
# Should output: true
```

## Testing

### Run Tests

```bash
make test
# or
./run_tests.sh
```

### Coverage Reports

```bash
make coverage-report
# or
./coverage_report.sh
```

Current test coverage: **93.88%**

See [TESTING.md](TESTING.md) for detailed testing information.

## Development Commands

The project includes a Makefile with common development tasks:

```bash
make help           # Show available commands
make install        # Install dependencies
make test           # Run tests
make coverage       # Run tests with coverage
make coverage-html  # Generate HTML coverage report
make run            # Start development server
make run-prod       # Start production server
make clean          # Clean up generated files
```

## Benefits of This Architecture

### Testability

- Webhook mutation logic is isolated and easily testable
- Admission review processing can be unit tested
- Fast tests without requiring a Kubernetes cluster

### Maintainability

- Clear separation between webhook handling and mutation logic
- Changes to mutation rules don't affect HTTP handling
- Easy to understand and modify annotation injection logic

### Flexibility

- Easy to extend to support different annotations or resources
- Framework-agnostic mutation business logic
- Supports different Kubernetes deployment scenarios

### Reliability

- Structured error handling for admission failures
- Comprehensive logging for debugging webhook issues
- Graceful handling of malformed admission reviews

## Extending the Webhook

### 1. Adding New Annotations

To inject additional annotations, modify the mutation logic:

```python
# app/api/routes/webhook.py
def create_item(body: AdmissionReviewRequest):
    annotations_to_add = {
        "example.com/injected": "true",
        "example.com/processed-by": "webhook-v1.0",
        "example.com/timestamp": datetime.utcnow().isoformat()
    }
    
    for key, value in annotations_to_add.items():
        # Apply annotation logic
        pass
```

### 2. Supporting Different Resource Types

Extend the webhook to handle different Kubernetes resources:

```python
# Add to MutatingAdmissionWebhook configuration
rules:
- operations: ["CREATE", "UPDATE"]
  apiGroups: [""]
  apiVersions: ["v1"]
  resources: ["pods", "services", "configmaps"]
- operations: ["CREATE"]
  apiGroups: ["apps"]
  apiVersions: ["v1"]
  resources: ["deployments"]
```

### 3. Conditional Mutation Logic

Add conditions based on object properties:

```python
def should_mutate(obj: dict) -> bool:
    # Only mutate pods in specific namespaces
    namespace = obj.get("metadata", {}).get("namespace")
    return namespace in ["production", "staging"]
    
    # Or based on labels
    labels = obj.get("metadata", {}).get("labels", {})
    return labels.get("app") == "web-server"
```

### 4. Environment-Based Configuration

Make the webhook behavior configurable:

```python
# Environment variables
TARGET_ANNOTATION = os.getenv("TARGET_ANNOTATION", "example.com/injected")
TARGET_VALUE = os.getenv("TARGET_VALUE", "true")
TARGET_NAMESPACES = os.getenv("TARGET_NAMESPACES", "default").split(",")
```

## Configuration

### Environment Variables

- **`ENVIRONMENT`**: Set to "local" for development mode with hot reload
- **`OVERWRITE`**: Set to "true", "1", or "yes" to overwrite existing annotations (default: "false")
- **`TARGET_ANNOTATION`**: Custom annotation key to inject (default: "example.com/injected")
- **`TARGET_VALUE`**: Custom annotation value (default: "true")
- **`TARGET_NAMESPACES`**: Comma-separated list of namespaces to target (optional)

### TLS Configuration

For production deployment, the webhook requires TLS certificates:

```bash
# Mount certificates in the container
volumeMounts:
- name: certs
  mountPath: /etc/certs
  readOnly: true
```

### Webhook Configuration

The MutatingAdmissionWebhook resource controls which resources are intercepted:

```yaml
rules:
- operations: ["CREATE", "UPDATE"]
  apiGroups: [""]
  apiVersions: ["v1"]
  resources: ["pods"]
  namespaceSelector:
    matchLabels:
      webhook: "enabled"
```

## Contributing

1. Follow the established architecture patterns
2. Write tests for new features
3. Maintain test coverage above 90%
4. Update documentation for significant changes
5. Use type hints throughout the codebase

## License

This project is licensed under the MIT License.
