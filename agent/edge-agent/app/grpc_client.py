"""Edge-agent gRPC client.

Boot sequence
─────────────
TLS disabled (dev):
  1. Connect insecure → controller_addr
  2. Open CommandStream, send heartbeats, handle commands.

TLS enabled (production):
  1. If device cert not present → call Register() on registration_addr
       (server-TLS only channel, no client cert needed).
     • Persist returned cert + CA cert + device_uuid to cert_dir.
  2. Re-open CommandStream on controller_addr with mTLS.

Reconnects automatically with exponential backoff (1 s → 60 s cap).
"""
import asyncio
import logging
import sys
from functools import partial
from pathlib import Path

import psutil

from app.config import settings
from app.services.reconnect import KEEPALIVE_OPTIONS, backoff_sleep

_GENERATED = str(Path(__file__).parent / "generated")
if _GENERATED not in sys.path:
    sys.path.insert(0, _GENERATED)

logger = logging.getLogger(__name__)

HEARTBEAT_INTERVAL = 15   # seconds
RECONCILE_INTERVAL = 60   # seconds

# ---------------------------------------------------------------------------
# Certificate paths
# ---------------------------------------------------------------------------

def _cert_path(name: str) -> Path:
    return Path(settings.cert_dir) / name


def _has_device_cert() -> bool:
    return _cert_path("device.crt").exists() and _cert_path("device.key").exists()


def _load_device_uuid() -> str:
    """Return persisted UUID (written after registration) or fall back to config."""
    p = _cert_path("device_uuid")
    if p.exists():
        return p.read_text().strip()
    return settings.device_uuid


def _save_registration(device_uuid: str, cert_pem: str, ca_cert_pem: str) -> None:
    """Persist cert material returned by Register()."""
    d = Path(settings.cert_dir)
    d.mkdir(parents=True, exist_ok=True)
    (d / "device.crt").write_text(cert_pem)
    (d / "ca.crt").write_text(ca_cert_pem)
    (d / "device_uuid").write_text(device_uuid)
    logger.info("Certificates saved to %s", d)


# ---------------------------------------------------------------------------
# Channel factories
# ---------------------------------------------------------------------------

def _insecure_channel(addr: str):
    import grpc.aio
    return grpc.aio.insecure_channel(addr, options=KEEPALIVE_OPTIONS)


def _mtls_channel(addr: str):
    import grpc
    import grpc.aio
    client_key = _cert_path("device.key").read_bytes()
    client_cert = _cert_path("device.crt").read_bytes()
    ca_cert = _cert_path("ca.crt").read_bytes()
    creds = grpc.ssl_channel_credentials(
        root_certificates=ca_cert,
        private_key=client_key,
        certificate_chain=client_cert,
    )
    return grpc.aio.secure_channel(addr, creds, options=KEEPALIVE_OPTIONS)


def _server_tls_channel(addr: str):
    """Server-TLS only (no client cert) — used for initial registration."""
    import grpc
    import grpc.aio
    ca_path = _cert_path("ca.crt")
    root_certs = ca_path.read_bytes() if ca_path.exists() else None
    creds = grpc.ssl_channel_credentials(root_certificates=root_certs)
    return grpc.aio.secure_channel(addr, creds, options=KEEPALIVE_OPTIONS)


def _registration_addr() -> str:
    if settings.registration_addr:
        return settings.registration_addr
    # Derive from controller_addr by replacing port with 50052.
    host = settings.controller_addr.split(":")[0]
    return f"{host}:50052"


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

async def _register() -> str:
    """Perform one-time device registration. Returns assigned device_uuid."""
    from edgedeploy.v1 import edge_control_pb2, edge_control_pb2_grpc
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.x509.oid import NameOID

    logger.info("Registering with controller at %s", _registration_addr())

    # Generate device key + CSR
    d = Path(settings.cert_dir)
    d.mkdir(parents=True, exist_ok=True)
    key_path = d / "device.key"

    if key_path.exists():
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        key = load_pem_private_key(key_path.read_bytes(), password=None)
    else:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        key_path.write_bytes(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
        )

    device_name = settings.device_uuid  # use as CN in CSR
    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, device_name)]))
        .sign(key, hashes.SHA256())
    )
    csr_pem = csr.public_bytes(serialization.Encoding.PEM).decode()

    if settings.tls_enabled:
        channel_ctx = _server_tls_channel(_registration_addr())
    else:
        channel_ctx = _insecure_channel(_registration_addr())

    async with channel_ctx as channel:
        stub = edge_control_pb2_grpc.EdgeRegistrationStub(channel)
        resp = await stub.Register(
            edge_control_pb2.RegisterRequest(
                provisioning_token=settings.provisioning_token,
                device_name=device_name,
                csr_pem=csr_pem,
            )
        )

    _save_registration(resp.device_uuid, resp.cert_pem, resp.ca_cert_pem)
    logger.info("Registration complete — device_uuid=%s", resp.device_uuid)
    return resp.device_uuid


# ---------------------------------------------------------------------------
# Main reconnect loop
# ---------------------------------------------------------------------------

async def run_grpc_client() -> None:
    logger.info(
        "gRPC client starting: controller=%s tls=%s device_uuid=%s",
        settings.controller_addr,
        settings.tls_enabled,
        settings.device_uuid,
    )
    device_uuid = _load_device_uuid()

    # Phase 5: apply cached config immediately so offline state is restored.
    await _apply_cached_config()

    attempt = 0

    while True:
        try:
            # Registration (first boot, TLS mode only — but also support insecure
            # registration for dev when provisioning_token is set and no cert exists).
            needs_registration = (
                settings.provisioning_token
                and not _has_device_cert()
            )
            if needs_registration:
                device_uuid = await _register()

            await _connect_and_stream(device_uuid)
            attempt = 0  # reset on clean disconnect

        except asyncio.CancelledError:
            logger.info("gRPC client cancelled")
            return
        except Exception as exc:
            logger.error("gRPC error (attempt %d): %s — reconnecting", attempt, exc)
            await backoff_sleep(attempt)
            attempt += 1


# ---------------------------------------------------------------------------
# Offline resilience helpers
# ---------------------------------------------------------------------------

async def _apply_cached_config() -> None:
    """Apply desired state from local cache (called at startup)."""
    from app.services import config_cache, k8s_manager

    config = config_cache.load()
    if not config:
        logger.debug("No config cache found — skipping startup apply")
        return

    deployments = config.get("deployments", [])
    logger.info(
        "Applying %d deployment(s) from cache (v=%s)",
        len(deployments),
        config.get("config_version"),
    )
    loop = asyncio.get_running_loop()
    for dep in deployments:
        try:
            await loop.run_in_executor(
                None,
                partial(k8s_manager.apply_manifests, dep["manifests"], dep["namespace"]),
            )
            logger.debug("Cache-apply OK: namespace=%s", dep["namespace"])
        except Exception as exc:
            logger.warning("Cache-apply failed for namespace=%s: %s", dep["namespace"], exc)


async def _reconcile_loop() -> None:
    """Every RECONCILE_INTERVAL seconds, re-apply cached desired state vs actual K8s state."""
    from app.services import config_cache, k8s_manager

    while True:
        await asyncio.sleep(RECONCILE_INTERVAL)
        config = config_cache.load()
        if not config:
            continue
        deployments = config.get("deployments", [])
        loop = asyncio.get_running_loop()
        for dep in deployments:
            try:
                # get_resources returns current K8s state; apply_manifests is idempotent.
                await loop.run_in_executor(
                    None,
                    partial(k8s_manager.apply_manifests, dep["manifests"], dep["namespace"]),
                )
            except Exception as exc:
                logger.warning(
                    "Reconcile failed for namespace=%s: %s", dep["namespace"], exc
                )


# ---------------------------------------------------------------------------
# Bidi stream session
# ---------------------------------------------------------------------------

async def _connect_and_stream(device_uuid: str) -> None:
    from edgedeploy.v1 import edge_control_pb2, edge_control_pb2_grpc
    from app.services import command_handler

    if settings.tls_enabled and _has_device_cert():
        channel_ctx = _mtls_channel(settings.controller_addr)
    else:
        channel_ctx = _insecure_channel(settings.controller_addr)

    async with channel_ctx as channel:
        stub = edge_control_pb2_grpc.EdgeControlStub(channel)
        report_queue: asyncio.Queue = asyncio.Queue()

        async def report_generator():
            while True:
                report = await report_queue.get()
                yield report

        call = stub.CommandStream(report_generator())
        await report_queue.put(_heartbeat(device_uuid))
        logger.info("CommandStream open → %s (uuid=%s)", settings.controller_addr, device_uuid)

        async def heartbeat_loop():
            while True:
                await asyncio.sleep(HEARTBEAT_INTERVAL)
                await report_queue.put(_heartbeat(device_uuid))

        hb_task = asyncio.create_task(heartbeat_loop())
        reconcile_task = asyncio.create_task(_reconcile_loop())
        try:
            async for command in call:
                result = await command_handler.handle(command)
                if result is not None:
                    await report_queue.put(result)
        finally:
            hb_task.cancel()
            reconcile_task.cancel()
            for t in (hb_task, reconcile_task):
                try:
                    await t
                except asyncio.CancelledError:
                    pass


# ---------------------------------------------------------------------------
# Heartbeat factory
# ---------------------------------------------------------------------------

def _heartbeat(device_uuid: str):
    from edgedeploy.v1 import edge_control_pb2
    from google.protobuf.timestamp_pb2 import Timestamp
    from app.services import config_cache

    ts = Timestamp()
    ts.GetCurrentTime()
    return edge_control_pb2.EdgeReport(
        device_uuid=device_uuid,
        heartbeat=edge_control_pb2.Heartbeat(
            ts=ts,
            agent_version="0.3.0",
            config_version=config_cache.get_config_version(),
            cpu_usage_percent=float(psutil.cpu_percent(interval=None)),
            memory_usage_percent=float(psutil.virtual_memory().percent),
        ),
    )
