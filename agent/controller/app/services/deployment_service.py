"""Orchestrate deployment: validate → generate YAML → push to agent → log."""
import logging
from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import settings
from app.models import App, Deployment, DeploymentLog, Device
from app.services import agent_client, manifest_builder
from app.services import config_store

logger = logging.getLogger(__name__)


async def create_form_deployment(
    session: AsyncSession,
    app_id: int,
    device_id: int,
    namespace: str,
    tag: str | None,
    replicas: int | None,
    port: int | None,
    env: dict | None,
) -> Deployment:
    if namespace in settings.blocked_namespaces:
        raise ValueError(f"Namespace '{namespace}' is blocked for deployments")

    app = await session.get(App, app_id)
    if not app:
        raise ValueError(f"App {app_id} not found")

    device = await session.get(Device, device_id)
    if not device:
        raise ValueError(f"Device {device_id} not found")

    # Use app defaults for anything not overridden
    resolved_tag = tag or app.default_tag
    resolved_replicas = replicas if replicas is not None else app.default_replicas
    resolved_port = port or app.default_port
    resolved_env = env or app.default_env or {}

    # Use custom template if defined, else generate from standard templates
    if app.yaml_template:
        from jinja2 import Template
        manifests = Template(app.yaml_template).render(
            name=app.name.lower().replace(" ", "-"),
            image=app.image,
            tag=resolved_tag,
            replicas=resolved_replicas,
            namespace=namespace,
            port=resolved_port,
            env=resolved_env,
        )
    else:
        manifests = manifest_builder.build_manifests(
            name=app.name.lower().replace(" ", "-"),
            image=app.image,
            tag=resolved_tag,
            replicas=resolved_replicas,
            namespace=namespace,
            port=resolved_port,
            env=resolved_env,
        )

    return await _push_deployment(
        session=session,
        device=device,
        app_id=app_id,
        namespace=namespace,
        manifests=manifests,
    )


async def create_yaml_deployment(
    session: AsyncSession,
    device_id: int,
    namespace: str,
    manifests: str,
    app_id: int | None,
) -> Deployment:
    if namespace in settings.blocked_namespaces:
        raise ValueError(f"Namespace '{namespace}' is blocked for deployments")

    device = await session.get(Device, device_id)
    if not device:
        raise ValueError(f"Device {device_id} not found")

    return await _push_deployment(
        session=session,
        device=device,
        app_id=app_id,
        namespace=namespace,
        manifests=manifests,
    )


async def _push_deployment(
    session: AsyncSession,
    device: Device,
    app_id: int | None,
    namespace: str,
    manifests: str,
) -> Deployment:
    deployment = Deployment(
        app_id=app_id,
        device_id=device.id,
        namespace=namespace,
        manifests=manifests,
        status="deploying",
    )
    session.add(deployment)
    await session.commit()
    await session.refresh(deployment)

    try:
        result = await agent_client.apply_manifests(device, manifests, namespace)
        deployment.status = "running"
        deployment.status_message = f"Applied {len(result.get('applied', []))} resource(s)"
        log_status = "success"
        log_detail = result
    except Exception as exc:
        deployment.status = "failed"
        deployment.status_message = str(exc)
        log_status = "failure"
        log_detail = {"error": str(exc)}
        logger.error("Deployment %d failed: %s", deployment.id, exc)

    session.add(deployment)

    log_entry = DeploymentLog(
        deployment_id=deployment.id,
        action="deploy",
        detail=log_detail,
        status=log_status,
    )
    session.add(log_entry)
    await session.commit()
    await session.refresh(deployment)

    # Bump config_version so agents learn the desired state changed.
    if deployment.status == "running":
        await config_store.bump_config_version(device.id)

    return deployment


async def stop_deployment(session: AsyncSession, deployment_id: int) -> Deployment:
    deployment = await session.get(Deployment, deployment_id)
    if not deployment:
        raise ValueError(f"Deployment {deployment_id} not found")

    device = await session.get(Device, deployment.device_id)
    if not device:
        raise ValueError(f"Device {deployment.device_id} not found")

    import yaml as pyyaml
    for doc in pyyaml.safe_load_all(deployment.manifests):
        if not doc:
            continue
        ns = doc.get("metadata", {}).get("namespace") or deployment.namespace
        await agent_client.delete_resource(
            device,
            ns,
            doc.get("kind", ""),
            doc.get("metadata", {}).get("name", ""),
        )

    deployment.status = "stopped"
    deployment.status_message = None
    session.add(deployment)

    log = DeploymentLog(
        deployment_id=deployment.id,
        action="stop",
        detail={},
        status="success",
    )
    session.add(log)
    await session.commit()
    await session.refresh(deployment)

    # Bump config_version so agents know the desired state changed.
    await config_store.bump_config_version(device.id)

    return deployment
