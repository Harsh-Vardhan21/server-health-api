# Server Health Check API

A production-grade REST API microservice that exposes real-time server health metrics — CPU, memory, and disk usage — deployed on AWS EKS using Terraform and a fully automated Jenkins CI/CD pipeline.

---

## The Problem It Solves

In production environments, checking server health requires SSH-ing into machines and running commands manually. This API exposes those metrics programmatically over HTTP — any system, dashboard, or monitoring tool can query server health instantly without manual intervention.

---

## Live API
GET /health   → http://a09cebedfe40a48318443717ac949373-1191760405.ap-south-1.elb.amazonaws.com/health
GET /metrics  → http://a09cebedfe40a48318443717ac949373-1191760405.ap-south-1.elb.amazonaws.com/metrics
GET /docs     → http://a09cebedfe40a48318443717ac949373-1191760405.ap-south-1.elb.amazonaws.com/docs

---

## Architecture
Developer pushes code
│
▼ GitHub webhook
Jenkins CI/CD (EC2)
│
├── Run unit tests
├── Build Docker image
├── Push to Docker Hub
└── kubectl apply → AWS EKS
│
▼
Server Health Check API
(2 pods, LoadBalancer service)
│
▼
CloudWatch Alarms
→ SNS → Email alerts

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python + FastAPI | REST API framework |
| psutil | Read real system metrics |
| Docker | Containerize the application |
| Jenkins | CI/CD pipeline automation |
| Terraform | Provision AWS infrastructure as code |
| AWS EKS | Managed Kubernetes cluster |
| AWS VPC | Isolated network with public/private subnets |
| AWS IAM | Permissions for EKS cluster and nodes |
| AWS S3 | Remote Terraform state storage |
| AWS CloudWatch | Monitor EKS cluster metrics |
| AWS SNS | Email notifications for alarms |
| Kubernetes | Container orchestration |
| Docker Hub | Container image registry |
| GitHub Webhooks | Auto-trigger Jenkins on push |

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Service status and timestamp |
| `/metrics` | GET | All metrics — CPU, memory, disk |
| `/metrics/cpu` | GET | CPU usage, core count, frequency |
| `/metrics/memory` | GET | Total, used, available RAM |
| `/metrics/disk` | GET | Total, used, free disk space |
| `/docs` | GET | Interactive Swagger UI |

---

## Project Structure
server-health-api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   └── routes/
│       ├── health.py        # Health check endpoint
│       └── metrics.py       # System metrics endpoints
├── tests/
│   └── test_main.py         # Unit tests
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   └── service.yaml         # LoadBalancer service
├── terraform/
│   ├── main.tf              # Provider and backend config
│   ├── variables.tf         # Configurable values
│   ├── vpc.tf               # VPC, subnets, gateways
│   ├── eks.tf               # EKS cluster and node group
│   ├── iam.tf               # IAM roles for EKS
│   └── outputs.tf           # Output values after apply
├── Dockerfile               # Container definition
├── Jenkinsfile              # CI/CD pipeline definition
└── requirements.txt         # Python dependencies
---

## How to Run Locally

```bash
# Clone repo
git clone https://github.com/Harsh-Vardhan21/server-health-api.git
cd server-health-api

# Install dependencies
pip3 install -r requirements.txt

# Run API
python3 -m uvicorn app.main:app --reload

# Test at http://localhost:8000/docs
```

---

## How to Deploy

### Prerequisites
- AWS CLI configured
- Terraform installed
- kubectl installed
- Docker installed
- Jenkins running on EC2

### 1. Provision AWS infrastructure
```bash
cd terraform
terraform init
terraform apply
```

### 2. Connect kubectl to EKS
```bash
aws eks update-kubeconfig --region ap-south-1 --name server-health-cluster
```

### 3. Deploy to EKS
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 4. Get Load Balancer URL
```bash
kubectl get services
```

---

## How to Destroy (Stop All AWS Charges)

```bash
# Delete Kubernetes service first (removes Load Balancer)
kubectl delete service server-health-api-service

# Destroy all Terraform infrastructure
cd terraform
terraform destroy
```

---

## CI/CD Pipeline

Every `git push` to main branch automatically:
1. Runs 5 unit tests — pipeline stops if any fail
2. Builds Docker image
3. Pushes to Docker Hub
4. Connects to EKS via AWS credentials
5. Applies Kubernetes manifests
6. Verifies rollout is successful

---

## CloudWatch Monitoring

Three alarms configured on the EKS cluster:
- **EKS-High-CPU** — triggers when CPU exceeds 80%
- **EKS-High-Memory** — triggers when memory exceeds 80%
- **EKS-Pod-Restarts** — triggers when pods fail

All alarms notify via SNS email alerts.

---

## Author

**Harsh Vardhan**
- GitHub: [Harsh-Vardhan21](https://github.com/Harsh-Vardhan21)
- LinkedIn: linkedin.com/in/harsh-vardhan-71957a217
