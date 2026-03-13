# Deployment Guide

This guide covers deploying the full platform: controller server, frontend, Envoy proxy, and edge agents.

---

## 1. Prerequisites

| Requirement | Notes |
|-------------|-------|
| Docker + Docker Compose v2 | All server-side services run in containers |
| `protoc` + `protoc-gen-grpc-web` binary | Required for TypeScript proto compilation (local dev) |
| Python 3.11+ with `grpcio-tools` | Required for Python proto compilation |
| Kubernetes cluster on each edge node | K3s recommended for resource-constrained nodes |
| Harbor registry (private images) | `192.168.11.136:30002` — production only |

---

## 2. Repository Layout

| Directory | Contents |
|-----------|----------|
| `controller/` | FastAPI + gRPC server (Python) |
| `edge-agent/` | Edge agent service (Python) |
| `envoy/` | Envoy proxy config for gRPC-Web translation |
| `frontend/` | React SPA |
| `proto/` | Protobuf definitions + Makefile |
| `deploy/` | K8s manifests and production compose files |

---

## 3. Proto Compilation

**Must be done before building any images.**

```bash
cd proto

# Python — outputs to controller/app/generated/ and edge-agent/app/generated/
pip install grpcio-tools           # if not already installed
make proto-python                  # → controller/app/generated/
make proto-edge                    # → edge-agent/app/generated/

# TypeScript — requires protoc + protoc-gen-grpc-web binary in PATH
make proto-ts                      # → frontend/src/generated/
```

---

## 4. Controller + Frontend + Envoy (Server Side)

### Dev Mode (single machine)

```bash
docker-compose up --build
```

Ports exposed:

| Port | Service | Purpose |
|------|---------|---------|
| 80 | frontend | React SPA |
| 8000 | controller | Admin REST (provisioning tokens only) |
| 8080 | envoy | gRPC-Web (browser → controller) |
| 50051 | controller | gRPC (edge agents) |
| 9901 | envoy | Envoy admin dashboard |

### Production Mode

```bash
docker-compose -f deploy/docker-compose.prod.yml up -d
```

- Images are pulled from the Harbor registry at `192.168.11.136:30002`
- Set `CTRL_GRPC_TLS_ENABLED=true` to enable mTLS for edge agent connections

### Key Environment Variables (Controller)

| Variable | Default | Description |
|----------|---------|-------------|
| `CTRL_LOG_LEVEL` | `info` | Logging level |
| `CTRL_GRPC_TLS_ENABLED` | `false` | Enable mTLS for gRPC connections |
| `CTRL_CERTS_DIR` | `./certs` | CA and server certificate directory |
| `CTRL_DATABASE_URL` | `sqlite+aiosqlite:///./data/controller.db` | Database path |
| `CTRL_HEALTH_POLL_INTERVAL` | `30` | Seconds between HTTP health checks for non-gRPC devices |
| `CTRL_AGENT_TIMEOUT` | `30.0` | Seconds before an unresponsive agent is marked offline |

---

## 5. Edge Agent Deployment

### Step 1 — Generate a provisioning token (server side)

```bash
curl -X POST http://<controller>:8000/api/v1/provisioning-tokens \
  -H "Content-Type: application/json" \
  -d '{"device_name": "edge-node-01", "expires_in_hours": 24}'
# Returns: {"token": "abc123...", ...}
```

### Step 2 — Apply base K8s manifests on the edge node

```bash
kubectl apply -f deploy/agent-manifests/00-namespace.yaml
kubectl apply -f deploy/agent-manifests/01-serviceaccount.yaml
kubectl apply -f deploy/agent-manifests/02-rbac.yaml
```

### Step 3 — Configure the deployment

Edit the `env` section of `deploy/agent-manifests/03-deployment.yaml`:

| Variable | Example Value | Description |
|----------|---------------|-------------|
| `AGENT_CONTROLLER_ADDR` | `<controller-ip>:50051` | Controller gRPC endpoint |
| `AGENT_TLS_ENABLED` | `false` / `true` | Enable mTLS |
| `AGENT_PROVISIONING_TOKEN` | `abc123...` | Token from Step 1 |
| `AGENT_CERT_DIR` | `/app/certs` | Certificate storage path |
| `AGENT_DATA_DIR` | `/app/data` | Config cache directory |
| `AGENT_K8S_IN_CLUSTER` | `true` | Use in-cluster K8s service account |
| `AGENT_LOG_LEVEL` | `info` | Logging level |

```bash
kubectl apply -f deploy/agent-manifests/03-deployment.yaml
kubectl apply -f deploy/agent-manifests/04-service.yaml
```

### Step 4 — Verify the connection

```bash
kubectl logs -n edge-agent -l app=edge-agent -f
# Look for: "CommandStream open → <controller>:50051"
```

---

## 6. mTLS Setup (Production)

1. Start the controller with `CTRL_GRPC_TLS_ENABLED=true`. A CA and server certificate are auto-generated in `./certs/`.
2. Set `AGENT_TLS_ENABLED=true` and `AGENT_PROVISIONING_TOKEN=<token>` on the edge agent.
3. On first boot, the edge agent calls `Register()` on port `50052` (server-TLS only, no client cert required).
4. The controller signs the agent's CSR and returns `device.crt` + `ca.crt`.
5. The agent stores the certificates in `AGENT_CERT_DIR` and reconnects with full mTLS on port `50051`.

---

## 7. Building and Pushing Images

```bash
# Build
docker build -t 192.168.11.136:30002/korail/controller:latest ./controller
docker build -t 192.168.11.136:30002/korail/edge-agent:latest ./edge-agent
docker build -t 192.168.11.136:30002/korail/frontend:latest ./frontend

# Push
docker push 192.168.11.136:30002/korail/controller:latest
docker push 192.168.11.136:30002/korail/edge-agent:latest
docker push 192.168.11.136:30002/korail/frontend:latest
```

---

## 8. Offline Resilience Behavior

- On startup, the edge agent reads `/app/data/config_cache.json` and re-applies all previously running deployments to Kubernetes before the controller connection is established.
- A reconciliation loop runs every 60 seconds to re-apply desired state and correct any configuration drift.
- Each heartbeat includes `config_version`. If the agent's version is behind the controller's, the controller pushes a `ConfigSyncCommand` with the full desired state.
