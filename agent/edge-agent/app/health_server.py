"""Minimal async HTTP health server.

Serves GET /api/v1/health → 200 OK on settings.agent_port (default 30080).
Uses only the stdlib so no extra dependencies are needed.
"""
import asyncio
import logging

from app.config import settings

logger = logging.getLogger(__name__)

_RESPONSE_200 = (
    b"HTTP/1.1 200 OK\r\n"
    b"Content-Type: application/json\r\n"
    b"Content-Length: 15\r\n"
    b"Connection: close\r\n"
    b"\r\n"
    b'{"status":"ok"}'
)
_RESPONSE_404 = (
    b"HTTP/1.1 404 Not Found\r\n"
    b"Content-Length: 0\r\n"
    b"Connection: close\r\n"
    b"\r\n"
)


async def _handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        # Read just the request line — we don't need headers.
        line = await asyncio.wait_for(reader.readline(), timeout=5.0)
        parts = line.split()
        path = parts[1].decode() if len(parts) >= 2 else ""
        writer.write(_RESPONSE_200 if path == "/api/v1/health" else _RESPONSE_404)
        await writer.drain()
    except Exception:
        pass
    finally:
        writer.close()


async def run_health_server() -> None:
    server = await asyncio.start_server(_handle, "0.0.0.0", settings.agent_port)
    logger.info("Health server listening on port %d", settings.agent_port)
    async with server:
        await server.serve_forever()
