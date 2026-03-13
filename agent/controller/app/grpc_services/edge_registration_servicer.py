"""Real implementation of EdgeRegistration.Register().

Flow:
  1. Validate provisioning token (not expired, not used).
  2. Sign the agent's CSR with the controller CA.
  3. Create / update the Device record with the assigned device_uuid.
  4. Mark the provisioning token as used.
  5. Return signed cert + CA cert to the agent.
"""
import logging
import uuid
from datetime import datetime

import grpc

from app.database import async_session_factory
from app.models import Device
from app.models.provisioning_token import ProvisioningToken
from app.config import settings
from sqlmodel import select

try:
    from edgedeploy.v1 import edge_control_pb2, edge_control_pb2_grpc
    _STUBS_AVAILABLE = True
except ImportError:
    edge_control_pb2 = None  # type: ignore
    edge_control_pb2_grpc = None  # type: ignore
    _STUBS_AVAILABLE = False

logger = logging.getLogger(__name__)


class EdgeRegistrationServicer:
    async def Register(self, request, context):
        token_str = request.provisioning_token
        device_name = request.device_name or "unnamed"
        csr_pem = request.csr_pem

        # -- Validate token --
        async with async_session_factory() as session:
            result = await session.execute(
                select(ProvisioningToken).where(ProvisioningToken.token == token_str)
            )
            token = result.scalars().first()

        if token is None or not token.is_valid:
            await context.abort(
                grpc.StatusCode.PERMISSION_DENIED,
                "Invalid or expired provisioning token",
            )
            return

        if not settings.grpc_tls_enabled:
            # TLS disabled (dev mode) — skip CSR signing, return dummy certs.
            assigned_uuid = str(uuid.uuid4())
            await _persist_device(device_name, assigned_uuid)
            await _mark_token_used(token.id)
            logger.info("Register (no-TLS): device_name=%s uuid=%s", device_name, assigned_uuid)
            return edge_control_pb2.RegisterResponse(
                device_uuid=assigned_uuid,
                cert_pem="",
                ca_cert_pem="",
            )

        # -- TLS enabled: sign CSR --
        from app.services.cert_manager import sign_csr, ca_cert_pem

        assigned_uuid = str(uuid.uuid4())
        try:
            from app.grpc_server import _CA_KEY, _CA_CERT
            signed_cert = sign_csr(csr_pem, _CA_KEY, _CA_CERT, assigned_uuid)
        except Exception as exc:
            logger.error("CSR signing failed: %s", exc)
            await context.abort(grpc.StatusCode.INTERNAL, f"CSR signing error: {exc}")
            return

        await _persist_device(device_name, assigned_uuid)
        await _mark_token_used(token.id)
        logger.info("Register (mTLS): device_name=%s uuid=%s", device_name, assigned_uuid)

        return edge_control_pb2.RegisterResponse(
            device_uuid=assigned_uuid,
            cert_pem=signed_cert,
            ca_cert_pem=ca_cert_pem(settings.certs_dir),
        )


async def _persist_device(device_name: str, device_uuid: str) -> None:
    """Create a Device record if one with this name doesn't exist yet."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Device).where(Device.device_uuid == device_uuid)
        )
        device = result.scalars().first()
        if not device:
            result = await session.execute(
                select(Device).where(Device.name == device_name)
            )
            device = result.scalars().first()

        if device:
            device.device_uuid = device_uuid
        else:
            device = Device(
                name=device_name,
                address="",        # agent will update on first heartbeat
                agent_port=0,
                device_uuid=device_uuid,
                status="unknown",
            )
        session.add(device)
        await session.commit()


async def _mark_token_used(token_id: int) -> None:
    async with async_session_factory() as session:
        token = await session.get(ProvisioningToken, token_id)
        if token:
            token.used_at = datetime.utcnow()
            session.add(token)
            await session.commit()


def add_to_server(server) -> None:
    if not _STUBS_AVAILABLE:
        logger.warning("EdgeRegistration stubs not found — run `make proto-python`")
        return
    edge_control_pb2_grpc.add_EdgeRegistrationServicer_to_server(
        EdgeRegistrationServicer(), server
    )
