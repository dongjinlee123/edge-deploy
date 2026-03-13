import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.grpc_server import start_grpc_server, stop_grpc_server
from app.routers import provisioning
from app.services.health_monitor import run_health_monitor

logging.basicConfig(level=settings.log_level.upper())


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("data", exist_ok=True)
    await init_db()
    monitor_task = asyncio.create_task(run_health_monitor())
    grpc_servers = await start_grpc_server()
    yield
    monitor_task.cancel()
    await stop_grpc_server(grpc_servers)


# FastAPI is kept for admin-only REST endpoints (provisioning tokens).
# All device / app / deployment operations are served over gRPC (port 50051)
# and accessed by the frontend through the Envoy gRPC-Web proxy (port 8080).
app = FastAPI(title="Edge Deploy Controller", version="0.4.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"
app.include_router(provisioning.router, prefix=PREFIX)
