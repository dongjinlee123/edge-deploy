"""Async gRPC server bootstrap.

TLS disabled (default / dev mode):
  • One insecure server on port 50051 — all services.

TLS enabled (CTRL_GRPC_TLS_ENABLED=true):
  • Port 50051 — mTLS, all services except EdgeRegistration.
  • Port 50052 — server-TLS only (no client cert), EdgeRegistration only.
    Agents call this port to bootstrap their first certificate.

Reflection is enabled so `grpcurl -plaintext localhost:50051 list` works in
dev mode.
"""
import logging
import sys
from pathlib import Path

import grpc
import grpc.aio
from grpc_reflection.v1alpha import reflection

# grpc_tools.protoc generates cross-imports like `from edgedeploy.v1 import ...`
# which resolve relative to the generated/ directory — add it to sys.path once.
_GENERATED_DIR = str(Path(__file__).parent / "generated")
if _GENERATED_DIR not in sys.path:
    sys.path.insert(0, _GENERATED_DIR)

logger = logging.getLogger(__name__)

GRPC_PORT = 50051
GRPC_REGISTRATION_PORT = 50052

# CA key/cert populated at startup when TLS is enabled; imported by the
# EdgeRegistrationServicer for CSR signing.
_CA_KEY = None
_CA_CERT = None


async def start_grpc_server() -> list[grpc.aio.Server]:
    """Create, start, and return all running gRPC servers."""
    from app.config import settings

    servers: list[grpc.aio.Server] = []

    if settings.grpc_tls_enabled:
        servers = await _start_tls_servers(settings)
    else:
        servers = [await _start_insecure_server()]

    return servers


async def stop_grpc_server(servers: list[grpc.aio.Server], grace: float = 5.0) -> None:
    for srv in servers:
        await srv.stop(grace)
    logger.info("gRPC server(s) stopped")


# ---------------------------------------------------------------------------
# Insecure (dev) mode
# ---------------------------------------------------------------------------

async def _start_insecure_server() -> grpc.aio.Server:
    server = grpc.aio.server()
    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    _attach_all_servicers(server)
    _enable_reflection(server)
    await server.start()
    logger.info("gRPC server (insecure) listening on port %d", GRPC_PORT)
    return server


# ---------------------------------------------------------------------------
# TLS mode
# ---------------------------------------------------------------------------

async def _start_tls_servers(settings) -> list[grpc.aio.Server]:
    global _CA_KEY, _CA_CERT

    from app.services.cert_manager import (
        load_or_create_ca,
        load_or_create_server_cert,
    )

    _CA_KEY, _CA_CERT = load_or_create_ca(settings.certs_dir)
    server_key_pem, server_cert_pem = load_or_create_server_cert(
        settings.certs_dir, _CA_KEY, _CA_CERT
    )
    from pathlib import Path
    ca_cert_pem = (Path(settings.certs_dir) / "ca.crt").read_bytes()

    # -- mTLS main server (port 50051) --
    mtls_creds = grpc.ssl_server_credentials(
        [(server_key_pem, server_cert_pem)],
        root_certificates=ca_cert_pem,
        require_client_auth=True,
    )
    main_server = grpc.aio.server()
    main_server.add_secure_port(f"[::]:{GRPC_PORT}", mtls_creds)
    _attach_main_servicers(main_server)
    _enable_reflection(main_server)
    await main_server.start()
    logger.info("gRPC server (mTLS) listening on port %d", GRPC_PORT)

    # -- Server-TLS registration server (port 50052) --
    tls_creds = grpc.ssl_server_credentials(
        [(server_key_pem, server_cert_pem)],
        root_certificates=None,
        require_client_auth=False,
    )
    reg_server = grpc.aio.server()
    reg_server.add_secure_port(f"[::]:{GRPC_REGISTRATION_PORT}", tls_creds)
    _attach_registration_servicer(reg_server)
    await reg_server.start()
    logger.info(
        "gRPC registration server (server-TLS) listening on port %d",
        GRPC_REGISTRATION_PORT,
    )

    return [main_server, reg_server]


# ---------------------------------------------------------------------------
# Servicer attachment helpers
# ---------------------------------------------------------------------------

def _attach_all_servicers(server: grpc.aio.Server) -> None:
    """Attach every servicer (used in insecure dev mode)."""
    from app.grpc_services import (
        app_servicer,
        deployment_servicer,
        device_servicer,
        edge_control_servicer,
        edge_registration_servicer,
    )
    for mod in (
        edge_registration_servicer,
        edge_control_servicer,
        device_servicer,
        app_servicer,
        deployment_servicer,
    ):
        try:
            mod.add_to_server(server)
        except Exception as exc:
            logger.warning("Could not register servicer %s: %s", mod.__name__, exc)


def _attach_main_servicers(server: grpc.aio.Server) -> None:
    """Attach all servicers except EdgeRegistration (mTLS server)."""
    from app.grpc_services import (
        app_servicer,
        deployment_servicer,
        device_servicer,
        edge_control_servicer,
    )
    for mod in (edge_control_servicer, device_servicer, app_servicer, deployment_servicer):
        try:
            mod.add_to_server(server)
        except Exception as exc:
            logger.warning("Could not register servicer %s: %s", mod.__name__, exc)


def _attach_registration_servicer(server: grpc.aio.Server) -> None:
    """Attach only EdgeRegistration (registration server)."""
    from app.grpc_services import edge_registration_servicer
    try:
        edge_registration_servicer.add_to_server(server)
    except Exception as exc:
        logger.warning("Could not register EdgeRegistration: %s", exc)


def _enable_reflection(server: grpc.aio.Server) -> None:
    service_names: list[str] = [reflection.SERVICE_NAME]
    try:
        from edgedeploy.v1 import (
            app_management_pb2,
            deployment_management_pb2,
            device_management_pb2,
            edge_control_pb2,
        )
        for pb2 in (
            edge_control_pb2,
            device_management_pb2,
            app_management_pb2,
            deployment_management_pb2,
        ):
            for svc in pb2.DESCRIPTOR.services_by_name.values():
                service_names.append(svc.full_name)
    except ImportError:
        logger.info("Generated proto stubs not found — run `make proto-python`")

    reflection.enable_server_reflection(service_names, server)
