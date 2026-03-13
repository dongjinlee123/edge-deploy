"""Reconnection utilities: exponential backoff and gRPC keepalive options."""
import asyncio

# Keepalive channel options — applied to every gRPC channel.
KEEPALIVE_OPTIONS = [
    ("grpc.keepalive_time_ms", 30_000),           # send ping every 30s
    ("grpc.keepalive_timeout_ms", 5_000),          # wait 5s for pong
    ("grpc.keepalive_permit_without_calls", 1),    # allow pings with no active calls
    ("grpc.http2.max_pings_without_data", 0),      # unlimited pings
    ("grpc.http2.min_time_between_pings_ms", 10_000),
]


async def backoff_sleep(attempt: int, base: float = 1.0, cap: float = 60.0) -> None:
    """Sleep for min(cap, base * 2^attempt) seconds."""
    delay = min(cap, base * (2 ** min(attempt, 10)))
    await asyncio.sleep(delay)
