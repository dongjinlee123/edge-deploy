import uuid as _uuid

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    agent_port: int = 30080
    log_level: str = "info"
    # In-cluster by default; override for local dev
    k8s_in_cluster: bool = True

    # gRPC controller address (mTLS after Phase 3, insecure in dev).
    # Set to "" to disable gRPC client entirely (HTTP-only mode).
    controller_addr: str = ""

    # Stable device identifier — sent in every heartbeat.
    # After registration this is overridden by the UUID returned by the controller.
    device_uuid: str = str(_uuid.uuid4())

    # Phase 3 — TLS / registration
    # Enable TLS on all gRPC channels.
    tls_enabled: bool = False
    # Directory where device.key, device.crt, ca.crt, device_uuid are stored.
    cert_dir: str = "./certs"
    # One-time provisioning token obtained from the controller admin API.
    # Required for first-boot registration when TLS is enabled.
    provisioning_token: str = ""
    # Controller address used for initial registration (server-TLS, no client cert).
    # Defaults to the same host as controller_addr but on port 50052.
    registration_addr: str = ""

    # Phase 5 — config cache
    # Directory for the persistent desired-config cache (config_cache.json).
    data_dir: str = "/app/data"

    model_config = {"env_prefix": "AGENT_"}


settings = Settings()
