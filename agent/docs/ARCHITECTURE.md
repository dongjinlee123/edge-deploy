# Architecture Guide

Technical reference for the edge device management platform. Covers component topology, protocols, data flows, and key implementation files.

---

## 1. System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          SERVER SIDE                                │
│                                                                     │
│  ┌──────────┐  gRPC-Web   ┌─────────┐   gRPC/h2    ┌────────────┐   │
│  │ Browser  │────────────▶│  Envoy  │─────────────▶│ Controller │   │
│  │ (React)  │  HTTP/1.1   │  :8080  │              │   :50051   │   │
│  └──────────┘             └─────────┘              │   :8000    │   │
│                                                    │  (FastAPI) │   │
│                                                    └─────┬──────┘   │
└──────────────────────────────────────────────────────────┼──────────┘
                                                           │ gRPC bidi stream
                                                           │ (edge-initiated)
                         ┌─────────────────────────────────┼──────────────┐
                         │              EDGE NODE          │              │
                         │                                 ▼              │
                         │  ┌────────────────────────────────────────┐    │
                         │  │           Edge Agent :30080            │    │
                         │  │  grpc_client ◀──────────────────────── │    │
                         │  │      │  heartbeat / ack / status       │    │
                         │  │      ▼                                 │    │
                         │  │  k8s_manager ──▶ K8s API (in-cluster)  │    │
                         │  └────────────────────────────────────────┘   │
                         └────────────────────────────────────────────────┘
```

---

## 2. Protocol Reference

| Connection | Protocol | Port | Auth | Direction |
|-----------|----------|------|------|-----------|
| Browser → Envoy | gRPC-Web (HTTP/1.1) | 8080 | none | client-initiated |
| Envoy → Controller | gRPC (HTTP/2) | 50051 | none (dev) / TLS (prod) | proxied |
| Edge Agent → Controller | gRPC bidi stream (HTTP/2) | 50051 | none (dev) / mTLS (prod) | **edge-initiated** |
| Edge Agent → Controller (registration) | gRPC (HTTP/2) | 50052 | server-TLS only | edge-initiated |
| Frontend → Controller (admin) | HTTP/1.1 REST | 8000 | none | client-initiated |
| Edge Agent → K8s API | HTTPS | in-cluster | ServiceAccount token | client-initiated |

---

## 3. Data Flow: Deploying an App

```
User clicks Deploy
       │
       ▼ gRPC-Web (DeploymentManagement.CreateFormDeployment)
    Envoy :8080
       │
       ▼ gRPC
    Controller
       ├─ Validates app + device
       ├─ Builds Kubernetes YAML manifests
       ├─ Writes Deployment row (status=deploying)
       ├─ Sends ApplyManifestsCommand → StreamManager queue
       │        │
       │        ▼ gRPC bidi stream (EdgeCommand)
       │     Edge Agent
       │        ├─ command_handler receives ApplyManifestsCommand
       │        ├─ k8s_manager.apply_manifests() → kubectl apply
       │        └─ Returns CommandAck (success=true) → bidi stream
       │
       ├─ resolve_ack() resolves asyncio.Future
       ├─ Updates Deployment row (status=running)
       ├─ Bumps device.config_version
       └─ Returns Deployment proto to frontend
```

---

## 4. Data Flow: Edge Agent Reconnect + Config Sync

```
Edge Agent boots / reconnects
       │
       ├─ Reads config_cache.json → applies cached deployments to K8s (offline resilience)
       │
       ▼ gRPC bidi stream opens
    First Heartbeat (config_version=N)
       │
       ▼
    Controller _maybe_sync_config()
       ├─ config_version(agent) < config_version(controller)?
       │    YES → push ConfigSyncCommand (full desired state JSON)
       │    NO  → no-op
       │
       ▼ (if pushed)
    Edge Agent command_handler config_sync
       ├─ Saves new desired config to config_cache.json
       └─ Applies all deployments via k8s_manager
```

---

## 5. StreamManager: Command/Ack Correlation

Each outbound command is correlated with its acknowledgement using an `asyncio.Future` keyed by `command_id`.

```
Controller send_command(device_uuid, EdgeCommand)
       │
       ├─ Creates asyncio.Future → pending[command_id]
       ├─ Puts EdgeCommand on per-device queue
       │
       ▼ (writer task drains queue → bidi stream write)
    Edge Agent receives command → executes → sends CommandAck
       │
       ▼ (bidi stream read in controller)
    resolve_ack(command_id, success, message, result_json)
       └─ Sets Future result → caller's await unblocks
```

This means `send_command()` is effectively an async RPC over the long-lived bidi stream, with built-in timeout handling via `asyncio.wait_for`.

---

## 6. Certificate Bootstrap (mTLS, Production)

```
First boot (no device.crt):
  Edge Agent → Register() on :50052 (server-TLS only, no client cert)
             ← Controller signs CSR, returns device.crt + ca.crt
  Agent stores certs in AGENT_CERT_DIR

All subsequent connections:
  Edge Agent ──mTLS──▶ Controller :50051
  (client cert = device.crt signed by controller CA)
```

The registration port (`50052`) uses server-TLS only so that uncertified agents can bootstrap. After certificate issuance, all traffic moves to the mTLS port (`50051`).

---

## 7. Key Files Reference

| Component | File | Role |
|-----------|------|------|
| Controller gRPC bootstrap | `controller/app/grpc_server.py` | Start insecure/TLS gRPC servers on :50051/:50052 |
| Command stream servicer | `controller/app/grpc_services/edge_control_servicer.py` | Heartbeat handling, ack routing, config sync |
| Stream correlation | `controller/app/services/stream_manager.py` | Per-device queue + Future tracking |
| Config versioning | `controller/app/services/config_store.py` | bump/get `config_version` per device |
| Deployment orchestration | `controller/app/services/deployment_service.py` | Manifest generation + command dispatch |
| Edge gRPC client | `edge-agent/app/grpc_client.py` | Connect to controller, heartbeat loop, reconciliation |
| Command dispatch | `edge-agent/app/services/command_handler.py` | Route incoming commands to `k8s_manager` |
| Config cache | `edge-agent/app/services/config_cache.py` | Persist desired state for offline resilience |
| Envoy config | `envoy/envoy.yaml` | gRPC-Web → gRPC translation on :8080 → :50051 |
