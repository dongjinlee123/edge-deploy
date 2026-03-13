"""CA and certificate management using the `cryptography` library.

On first start (when CTRL_GRPC_TLS_ENABLED=true) this module:
  1. Generates a self-signed CA key/cert if they don't already exist.
  2. Generates a server key/cert signed by that CA.

Callers use `sign_csr()` to issue device certificates during registration.
"""
import datetime
import ipaddress
import logging
import os
import uuid
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _generate_rsa_key(key_size: int = 2048):
    return rsa.generate_private_key(public_exponent=65537, key_size=key_size)


def _pem_key(key) -> bytes:
    return key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    )


def _pem_cert(cert) -> bytes:
    return cert.public_bytes(serialization.Encoding.PEM)


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    logger.info("Written %s", path)


def _read(path: Path) -> bytes:
    return path.read_bytes()


def _load_key(path: Path):
    return serialization.load_pem_private_key(_read(path), password=None)


def _load_cert(path: Path):
    return x509.load_pem_x509_certificate(_read(path))


# ---------------------------------------------------------------------------
# CA bootstrap
# ---------------------------------------------------------------------------

def load_or_create_ca(certs_dir: str) -> tuple:
    """Return (ca_key, ca_cert).  Create and persist if they don't exist."""
    d = Path(certs_dir)
    key_path = d / "ca.key"
    crt_path = d / "ca.crt"

    if key_path.exists() and crt_path.exists():
        logger.info("Loading existing CA from %s", d)
        return _load_key(key_path), _load_cert(crt_path)

    logger.info("Generating new CA in %s", d)
    key = _generate_rsa_key(4096)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "Edge Deploy CA"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Edge Deploy"),
    ])
    now = datetime.datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False
        )
        .sign(key, hashes.SHA256())
    )
    _write(key_path, _pem_key(key))
    _write(crt_path, _pem_cert(cert))
    return key, cert


# ---------------------------------------------------------------------------
# Server cert
# ---------------------------------------------------------------------------

def load_or_create_server_cert(certs_dir: str, ca_key, ca_cert, hostnames: list[str] | None = None) -> tuple[bytes, bytes]:
    """Return (server_key_pem, server_cert_pem).  Create and persist if missing."""
    d = Path(certs_dir)
    key_path = d / "server.key"
    crt_path = d / "server.crt"

    if key_path.exists() and crt_path.exists():
        return _read(key_path), _read(crt_path)

    logger.info("Generating server cert in %s", d)
    key = _generate_rsa_key(2048)
    if not hostnames:
        hostnames = ["controller", "localhost"]

    san_dns = [x509.DNSName(h) for h in hostnames]
    san_ip = [x509.IPAddress(ipaddress.IPv4Address("127.0.0.1"))]

    now = datetime.datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "controller")]))
        .issuer_name(ca_cert.subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName(san_dns + san_ip), critical=False
        )
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]), critical=False
        )
        .sign(ca_key, hashes.SHA256())
    )
    _write(key_path, _pem_key(key))
    _write(crt_path, _pem_cert(cert))
    return _read(key_path), _read(crt_path)


# ---------------------------------------------------------------------------
# CSR signing  (called during device registration)
# ---------------------------------------------------------------------------

def sign_csr(csr_pem: str, ca_key, ca_cert, device_uuid: str) -> str:
    """Sign a device CSR and return PEM-encoded certificate."""
    csr = x509.load_pem_x509_csr(csr_pem.encode())
    if not csr.is_signature_valid:
        raise ValueError("CSR signature is invalid")

    now = datetime.datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, device_uuid)]))
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CLIENT_AUTH]), critical=False
        )
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(device_uuid)]), critical=False
        )
        .sign(ca_key, hashes.SHA256())
    )
    return _pem_cert(cert).decode()


# ---------------------------------------------------------------------------
# CA cert PEM helper (used when returning CA to agent)
# ---------------------------------------------------------------------------

def ca_cert_pem(certs_dir: str) -> str:
    return _read(Path(certs_dir) / "ca.crt").decode()
