import asyncio
import logging

from app.config import settings
from app.services import k8s_manager

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


async def main():
    try:
        k8s_manager.load_k8s_config(in_cluster=settings.k8s_in_cluster)
    except Exception as exc:
        logger.error("Failed to load k8s config: %s", exc)

    from app.health_server import run_health_server
    health_task = asyncio.create_task(run_health_server())

    if not settings.controller_addr:
        logger.error("AGENT_CONTROLLER_ADDR not set — running health server only")
        await health_task
        return

    from app.grpc_client import run_grpc_client
    await asyncio.gather(health_task, run_grpc_client())


if __name__ == "__main__":
    asyncio.run(main())
