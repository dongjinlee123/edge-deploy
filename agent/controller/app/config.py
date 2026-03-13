from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./data/controller.db"
    log_level: str = "info"
    health_poll_interval: int = 30  # seconds
    agent_timeout: float = 30.0  # seconds
    blocked_namespaces: list[str] = [
        "kube-system",
        "kube-public",
        "kube-node-lease",
        "edge-agent",
    ]
    # Phase 3 — mTLS
    grpc_tls_enabled: bool = False
    certs_dir: str = "./certs"

    model_config = {"env_prefix": "CTRL_"}


settings = Settings()
