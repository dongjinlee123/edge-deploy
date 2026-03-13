# EdgeDeploy — Korail Edge Deployment System

A lightweight edge deployment platform for managing containerized applications across distributed K3s nodes.

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   Frontend   │──────▶│    Controller    │──────▶│   Edge Agent     │
│  (React/Vite)│  HTTP │  (FastAPI + DB)  │  HTTP │  (FastAPI + K8s) │
│   :80        │       │   :8000          │       │   :30080         │
└──────────────┘       └──────────────────┘       └──────────────────┘
                                                          │
                                                          ▼
                                                  ┌──────────────┐
                                                  │  K3s Cluster │
                                                  │  (kubectl)   │
                                                  └──────────────┘
```

The **Controller** is the central management server. It stores device/app/deployment records in SQLite and communicates with **Edge Agents** running on each K3s node. The **Frontend** is a React SPA that provides a dashboard for operators.

---

## Prerequisites

- Docker & Docker Compose
- K3s installed on each edge node (for edge-agent)
- `kubectl` configured (for edge-agent local development)
- Access to a container registry (e.g., Harbor at `192.168.11.136:30002`)

---

## Quick Start (Development)

```bash
docker-compose up --build
```

| Service    | URL                          |
|------------|------------------------------|
| Frontend   | http://localhost:80           |
| Controller | http://localhost:8000         |
| API Docs   | http://localhost:8000/docs    |

The controller automatically creates an SQLite database on first run at `/app/data/controller.db` inside the container (persisted via `controller_data` volume).

---

## Deploying Edge Agent to a K3s Node

### 1. Build and push the edge-agent image

```bash
cd edge-agent
docker build -t 192.168.11.136:30002/korail/edge-agent:latest .
docker push 192.168.11.136:30002/korail/edge-agent:latest
```

### 2. Copy deploy files to the edge device

```bash
scp -r deploy/agent-manifests/ <user>@<EDGE_NODE_IP>:~/agent-manifests/
```

Then SSH into the edge device for the remaining steps:

```bash
ssh <user>@<EDGE_NODE_IP>
cd ~/agent-manifests
```

### 3. Create registry credentials (if using a private registry)

```bash
kubectl create namespace edge-agent

kubectl create secret docker-registry harbor-creds \
  --namespace edge-agent \
  --docker-server=192.168.11.136:30002 \
  --docker-username=<user> \
  --docker-password=<password>
```

### 4. Apply the manifests in order

```bash
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-serviceaccount.yaml
kubectl apply -f 02-rbac.yaml
kubectl apply -f 03-deployment.yaml
kubectl apply -f 04-service.yaml
```

### 5. Verify

```bash
# Check the pod is running
kubectl -n edge-agent get pods

# Health check (replace NODE_IP with your node's IP)
curl http://<NODE_IP>:30080/api/v1/health
```

The agent is exposed as a `NodePort` service on port **30080**.

---

## Deploying Controller (Production)

Use the pre-built images with the production compose file:

```bash
cd deploy
docker-compose -f docker-compose.prod.yml up -d
```

This uses images from the registry (`192.168.11.136:30002/korail/controller:latest` and `192.168.11.136:30002/korail/frontend:latest`). The SQLite database is persisted via the `controller_data` Docker volume.

---

## Configuration Reference

### Controller

| Environment Variable       | Description                          | Default                                   |
|---------------------------|--------------------------------------|-------------------------------------------|
| `CTRL_DATABASE_URL`       | SQLAlchemy async database URL        | `sqlite+aiosqlite:///./data/controller.db`|
| `CTRL_LOG_LEVEL`          | Logging level                        | `info`                                    |
| `CTRL_HEALTH_POLL_INTERVAL`| Seconds between device health polls | `30`                                      |
| `CTRL_AGENT_TIMEOUT`      | Timeout (seconds) for agent HTTP calls | `30.0`                                  |
| `CTRL_BLOCKED_NAMESPACES` | JSON list of namespaces to block     | `["kube-system","kube-public","kube-node-lease","edge-agent"]` |

### Edge Agent

| Environment Variable    | Description                              | Default |
|------------------------|------------------------------------------|---------|
| `AGENT_PORT`           | Port the agent listens on                | `30080` |
| `AGENT_LOG_LEVEL`      | Logging level                            | `info`  |
| `AGENT_K8S_IN_CLUSTER` | Use in-cluster K8s config (`true`/`false`) | `true`  |

---

## Using the Frontend

### Dashboard
Real-time overview showing total/online/offline devices and total/running/failed deployments. Auto-refreshes every 15 seconds (pauses when the browser tab is not visible).

### Devices
- **Register** a device by providing its name, IP address, and agent port
- **Ping** a device to check its connectivity status
- **Search** devices by name or filter by status (online/offline)
- View device details including labels and associated deployments

### Apps
- **Define** an app with an image, default tag, replicas, and port
- Apps serve as templates for deployments — customize per-deployment at deploy time
- **Search** apps by name

### Deployments
- **Form mode**: Select an app and device, override defaults as needed
- **YAML mode**: Paste raw Kubernetes manifests directly
- Filter deployments by status
- View manifests and audit logs for each deployment
- **Restart** triggers a rolling restart of Deployment resources
- **Stop & Delete** removes K8s resources and the deployment record

---

## API Reference

All endpoints are prefixed with `/api/v1`.

| Method   | Path                                          | Description                      |
|----------|-----------------------------------------------|----------------------------------|
| `GET`    | `/overview`                                   | Dashboard statistics             |
| `GET`    | `/devices`                                    | List all devices                 |
| `POST`   | `/devices`                                    | Register a new device            |
| `GET`    | `/devices/{id}`                               | Get device details               |
| `PUT`    | `/devices/{id}`                               | Update device                    |
| `DELETE` | `/devices/{id}`                               | Remove device                    |
| `POST`   | `/devices/{id}/ping`                          | Ping device agent                |
| `GET`    | `/apps`                                       | List all apps                    |
| `POST`   | `/apps`                                       | Create app definition            |
| `GET`    | `/apps/{id}`                                  | Get app details                  |
| `PUT`    | `/apps/{id}`                                  | Update app                       |
| `DELETE` | `/apps/{id}`                                  | Delete app                       |
| `GET`    | `/deployments`                                | List deployments (filterable)    |
| `POST`   | `/deployments/form`                           | Create deployment (form mode)    |
| `POST`   | `/deployments/yaml`                           | Create deployment (YAML mode)    |
| `GET`    | `/deployments/{id}`                           | Get deployment details           |
| `PUT`    | `/deployments/{id}`                           | Update deployment status         |
| `DELETE` | `/deployments/{id}`                           | Stop & delete deployment         |
| `POST`   | `/deployments/{id}/restart`                   | Rolling restart                  |
| `GET`    | `/deployments/{id}/logs`                      | Deployment audit logs            |
| `POST`   | `/bulk/deploy`                                | Deploy app to multiple devices   |

Interactive API documentation is available at `/docs` (Swagger UI).

---

## Project Structure

```
agent/
├── docker-compose.yml              # Development compose
├── deploy/
│   ├── docker-compose.prod.yml     # Production compose (pre-built images)
│   └── agent-manifests/            # K8s manifests for edge-agent
│       ├── 00-namespace.yaml
│       ├── 01-serviceaccount.yaml
│       ├── 02-rbac.yaml
│       ├── 03-deployment.yaml
│       └── 04-service.yaml
├── controller/
│   ├── Dockerfile
│   ├── alembic/                    # Database migrations
│   └── app/
│       ├── main.py                 # FastAPI entrypoint
│       ├── config.py               # Settings (env vars)
│       ├── database.py             # Async SQLite session
│       ├── models/                 # SQLModel ORM models
│       ├── schemas/                # Pydantic request/response schemas
│       ├── routers/                # API route handlers
│       │   ├── overview.py
│       │   ├── devices.py
│       │   ├── apps.py
│       │   ├── deployments.py
│       │   └── bulk.py
│       └── services/
│           ├── agent_client.py     # HTTP client for edge agents
│           ├── deployment_service.py
│           ├── manifest_builder.py # YAML generation
│           └── health_monitor.py   # Background health polling
├── edge-agent/
│   ├── Dockerfile
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── schemas.py
│       ├── routers/
│       │   ├── apply.py            # kubectl apply endpoint
│       │   ├── health.py
│       │   └── resources.py        # CRUD on K8s resources
│       └── services/
│           └── k8s_manager.py      # Kubernetes API wrapper
└── frontend/
    ├── Dockerfile
    ├── vite.config.ts
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── router/index.tsx
        ├── api/                    # HTTP client modules
        ├── components/             # Shared UI components
        ├── pages/                  # Route pages
        │   ├── Dashboard.tsx
        │   ├── DeviceList.tsx
        │   ├── DeviceDetail.tsx
        │   ├── AppList.tsx
        │   ├── AppDetail.tsx
        │   ├── DeploymentList.tsx
        │   ├── DeploymentCreate.tsx
        │   └── DeploymentDetail.tsx
        └── types/index.ts
```
