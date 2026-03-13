"""Real AppManagement gRPC servicer — ports controller/app/routers/apps.py."""
import json
import logging
from datetime import datetime

import grpc

from app.database import async_session_factory
from app.models import App
from sqlmodel import select

try:
    from edgedeploy.v1 import app_management_pb2, app_management_pb2_grpc
    from google.protobuf.timestamp_pb2 import Timestamp
    _STUBS_AVAILABLE = True
except ImportError:
    app_management_pb2 = None  # type: ignore
    app_management_pb2_grpc = None  # type: ignore
    _STUBS_AVAILABLE = False

logger = logging.getLogger(__name__)


def _ts(dt: datetime | None) -> "Timestamp":
    ts = Timestamp()
    if dt:
        ts.FromDatetime(dt)
    return ts


def _to_proto(a: App) -> "app_management_pb2.AppProto":
    return app_management_pb2.AppProto(
        id=a.id,
        name=a.name,
        image=a.image,
        default_tag=a.default_tag,
        default_replicas=a.default_replicas,
        default_port=a.default_port or 0,
        default_env_json=json.dumps(a.default_env) if a.default_env else "{}",
        yaml_template=a.yaml_template or "",
        created_at=_ts(a.created_at),
    )


class AppManagementServicer:
    async def ListApps(self, request, context):
        async with async_session_factory() as session:
            result = await session.execute(select(App))
            apps = result.scalars().all()
        return app_management_pb2.ListAppsResponse(apps=[_to_proto(a) for a in apps])

    async def GetApp(self, request, context):
        async with async_session_factory() as session:
            app = await session.get(App, request.id)
        if not app:
            await context.abort(grpc.StatusCode.NOT_FOUND, f"App {request.id} not found")
            return
        return _to_proto(app)

    async def CreateApp(self, request, context):
        async with async_session_factory() as session:
            app = App(
                name=request.name,
                image=request.image,
                default_tag=request.default_tag or "latest",
                default_replicas=request.default_replicas or 1,
                default_port=request.default_port or None,
                default_env=json.loads(request.default_env_json) if request.default_env_json else None,
                yaml_template=request.yaml_template or None,
            )
            session.add(app)
            await session.commit()
            await session.refresh(app)
        return _to_proto(app)

    async def UpdateApp(self, request, context):
        async with async_session_factory() as session:
            app = await session.get(App, request.id)
            if not app:
                await context.abort(grpc.StatusCode.NOT_FOUND, f"App {request.id} not found")
                return
            if request.name:
                app.name = request.name
            if request.image:
                app.image = request.image
            if request.default_tag:
                app.default_tag = request.default_tag
            if request.default_replicas:
                app.default_replicas = request.default_replicas
            if request.default_port:
                app.default_port = request.default_port
            if request.default_env_json:
                app.default_env = json.loads(request.default_env_json)
            if request.yaml_template:
                app.yaml_template = request.yaml_template
            session.add(app)
            await session.commit()
            await session.refresh(app)
        return _to_proto(app)

    async def DeleteApp(self, request, context):
        async with async_session_factory() as session:
            app = await session.get(App, request.id)
            if not app:
                await context.abort(grpc.StatusCode.NOT_FOUND, f"App {request.id} not found")
                return
            await session.delete(app)
            await session.commit()
        return app_management_pb2.DeleteAppResponse(ok=True)


def add_to_server(server) -> None:
    if not _STUBS_AVAILABLE:
        logger.warning("AppManagement stubs not found — run `make proto-python`")
        return
    app_management_pb2_grpc.add_AppManagementServicer_to_server(
        AppManagementServicer(), server
    )
