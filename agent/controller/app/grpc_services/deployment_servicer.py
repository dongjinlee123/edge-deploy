"""Real DeploymentManagement gRPC servicer.

Ports logic from:
  - controller/app/routers/deployments.py
  - controller/app/routers/bulk.py
  - controller/app/routers/overview.py
  - controller/app/services/deployment_service.py
"""
import json
import logging
import yaml as pyyaml
from datetime import datetime

import grpc

from app.config import settings
from app.database import async_session_factory
from app.models import App, Deployment, DeploymentLog, Device
from app.services import agent_client, deployment_service
from sqlmodel import func, select

try:
    from edgedeploy.v1 import deployment_management_pb2, deployment_management_pb2_grpc
    from google.protobuf.timestamp_pb2 import Timestamp
    _STUBS_AVAILABLE = True
except ImportError:
    deployment_management_pb2 = None  # type: ignore
    deployment_management_pb2_grpc = None  # type: ignore
    _STUBS_AVAILABLE = False

logger = logging.getLogger(__name__)


def _ts(dt: datetime | None) -> "Timestamp":
    ts = Timestamp()
    if dt:
        ts.FromDatetime(dt)
    return ts


def _depl_to_proto(d: Deployment) -> "deployment_management_pb2.DeploymentProto":
    return deployment_management_pb2.DeploymentProto(
        id=d.id,
        app_id=d.app_id or 0,
        device_id=d.device_id,
        namespace=d.namespace,
        manifests=d.manifests or "",
        status=d.status,
        status_message=d.status_message or "",
        created_at=_ts(d.created_at),
    )


def _log_to_proto(l: DeploymentLog) -> "deployment_management_pb2.DeploymentLogProto":
    return deployment_management_pb2.DeploymentLogProto(
        id=l.id,
        deployment_id=l.deployment_id,
        action=l.action,
        detail_json=json.dumps(l.detail) if l.detail else "{}",
        status=l.status,
        created_at=_ts(l.created_at),
    )


class DeploymentManagementServicer:

    async def ListDeployments(self, request, context):
        async with async_session_factory() as session:
            q = select(Deployment)
            if request.HasField("device_id"):
                q = q.where(Deployment.device_id == request.device_id.value)
            if request.HasField("app_id"):
                q = q.where(Deployment.app_id == request.app_id.value)
            if request.HasField("status"):
                q = q.where(Deployment.status == request.status.value)
            result = await session.execute(q.order_by(Deployment.created_at.desc()))
            deployments = result.scalars().all()
        return deployment_management_pb2.ListDeploymentsResponse(
            deployments=[_depl_to_proto(d) for d in deployments]
        )

    async def GetDeployment(self, request, context):
        async with async_session_factory() as session:
            d = await session.get(Deployment, request.id)
        if not d:
            await context.abort(grpc.StatusCode.NOT_FOUND, f"Deployment {request.id} not found")
            return
        return _depl_to_proto(d)

    async def CreateFormDeployment(self, request, context):
        try:
            async with async_session_factory() as session:
                d = await deployment_service.create_form_deployment(
                    session,
                    app_id=request.app_id,
                    device_id=request.device_id,
                    namespace=request.namespace or "default",
                    tag=request.tag or None,
                    replicas=request.replicas or None,
                    port=None,
                    env=None,
                )
            return _depl_to_proto(d)
        except ValueError as exc:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(exc))
        except Exception as exc:
            await context.abort(grpc.StatusCode.INTERNAL, str(exc))

    async def CreateYamlDeployment(self, request, context):
        try:
            async with async_session_factory() as session:
                d = await deployment_service.create_yaml_deployment(
                    session,
                    device_id=request.device_id,
                    namespace=request.namespace or "default",
                    manifests=request.manifests,
                    app_id=None,
                )
            return _depl_to_proto(d)
        except ValueError as exc:
            await context.abort(grpc.StatusCode.NOT_FOUND, str(exc))
        except Exception as exc:
            await context.abort(grpc.StatusCode.INTERNAL, str(exc))

    async def DeleteDeployment(self, request, context):
        async with async_session_factory() as session:
            try:
                await deployment_service.stop_deployment(session, request.id)
            except ValueError as exc:
                await context.abort(grpc.StatusCode.NOT_FOUND, str(exc))
                return
            except Exception as exc:
                logger.warning("Best-effort stop failed for deployment %d: %s", request.id, exc)

            logs = (await session.execute(
                select(DeploymentLog).where(DeploymentLog.deployment_id == request.id)
            )).scalars().all()
            for log in logs:
                await session.delete(log)

            d = await session.get(Deployment, request.id)
            if d:
                await session.delete(d)
            await session.commit()

        return deployment_management_pb2.DeleteDeploymentResponse(ok=True)

    async def RestartDeployment(self, request, context):
        async with async_session_factory() as session:
            d = await session.get(Deployment, request.id)
            if not d:
                await context.abort(grpc.StatusCode.NOT_FOUND, f"Deployment {request.id} not found")
                return
            device = await session.get(Device, d.device_id)
            if not device:
                await context.abort(grpc.StatusCode.NOT_FOUND, "Device not found")
                return

        errors = []
        for doc in pyyaml.safe_load_all(d.manifests):
            if doc and doc.get("kind", "").lower() == "deployment":
                name = doc.get("metadata", {}).get("name", "")
                try:
                    await agent_client.restart_deployment(device, d.namespace, name)
                except Exception as exc:
                    errors.append(str(exc))

        return deployment_management_pb2.RestartDeploymentResponse(ok=not errors)

    async def GetDeploymentLogs(self, request, context):
        async with async_session_factory() as session:
            result = await session.execute(
                select(DeploymentLog)
                .where(DeploymentLog.deployment_id == request.id)
                .order_by(DeploymentLog.created_at.desc())
            )
            logs = result.scalars().all()
        return deployment_management_pb2.GetDeploymentLogsResponse(
            logs=[_log_to_proto(l) for l in logs]
        )

    async def BulkDeploy(self, request, context):
        results = []
        async with async_session_factory() as session:
            for device_id in request.device_ids:
                try:
                    d = await deployment_service.create_form_deployment(
                        session,
                        app_id=request.app_id,
                        device_id=device_id,
                        namespace=request.namespace or "default",
                        tag=request.tag or None,
                        replicas=request.replicas or None,
                        port=None,
                        env=None,
                    )
                    results.append(_depl_to_proto(d))
                except Exception as exc:
                    logger.warning("BulkDeploy device %d failed: %s", device_id, exc)
        return deployment_management_pb2.BulkDeployResponse(deployments=results)

    async def GetOverview(self, request, context):
        async with async_session_factory() as session:
            total_devices = (await session.execute(select(func.count(Device.id)))).scalar_one()
            online_devices = (await session.execute(
                select(func.count(Device.id)).where(Device.status == "online")
            )).scalar_one()
            total_apps = (await session.execute(select(func.count(App.id)))).scalar_one()
            total_deployments = (await session.execute(select(func.count(Deployment.id)))).scalar_one()
            running_deployments = (await session.execute(
                select(func.count(Deployment.id)).where(Deployment.status == "running")
            )).scalar_one()
            failed_deployments = (await session.execute(
                select(func.count(Deployment.id)).where(Deployment.status == "failed")
            )).scalar_one()

        return deployment_management_pb2.OverviewProto(
            total_devices=total_devices,
            online_devices=online_devices,
            total_apps=total_apps,
            total_deployments=total_deployments,
            running_deployments=running_deployments,
            failed_deployments=failed_deployments,
        )


def add_to_server(server) -> None:
    if not _STUBS_AVAILABLE:
        logger.warning("DeploymentManagement stubs not found — run `make proto-python`")
        return
    deployment_management_pb2_grpc.add_DeploymentManagementServicer_to_server(
        DeploymentManagementServicer(), server
    )
