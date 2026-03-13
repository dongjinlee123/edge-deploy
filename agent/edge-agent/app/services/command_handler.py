"""Dispatch an EdgeCommand to the local k8s_manager and return an EdgeReport."""
import asyncio
import json
import logging
from functools import partial

from app.config import settings

logger = logging.getLogger(__name__)


async def handle(command):
    """Return an EdgeReport (CommandAck, ResourceSnapshot, or LogChunk)."""
    # Lazy imports so the module is safe to load before stubs are compiled.
    from edgedeploy.v1 import edge_control_pb2
    from app.services import k8s_manager

    cmd_id = command.command_id
    which = command.WhichOneof("payload")
    loop = asyncio.get_running_loop()

    try:
        if which == "apply_manifests":
            p = command.apply_manifests
            result = await loop.run_in_executor(
                None, partial(k8s_manager.apply_manifests, p.manifests, p.namespace)
            )
            return _ack(cmd_id, True, "applied", json.dumps(result))

        elif which == "delete_resource":
            p = command.delete_resource
            await loop.run_in_executor(
                None, partial(k8s_manager.delete_resource, p.namespace, p.kind, p.name)
            )
            return _ack(cmd_id, True, "deleted", "{}")

        elif which == "restart_deployment":
            p = command.restart_deployment
            await loop.run_in_executor(
                None, partial(k8s_manager.restart_deployment, p.namespace, p.name)
            )
            return _ack(cmd_id, True, "restarted", "{}")

        elif which == "get_resources":
            p = command.get_resources
            result = await loop.run_in_executor(
                None, partial(k8s_manager.get_resources, p.namespace)
            )
            return edge_control_pb2.EdgeReport(
                device_uuid=settings.device_uuid,
                resource_snapshot=edge_control_pb2.ResourceSnapshot(
                    command_id=cmd_id,
                    namespace=p.namespace,
                    resources_json=json.dumps(result),
                ),
            )

        elif which == "get_pod_logs":
            p = command.get_pod_logs
            logs = await loop.run_in_executor(
                None,
                partial(k8s_manager.get_pod_logs, p.namespace, p.pod_name, None, p.tail),
            )
            data = logs.encode("utf-8") if isinstance(logs, str) else logs
            return edge_control_pb2.EdgeReport(
                device_uuid=settings.device_uuid,
                log_chunk=edge_control_pb2.LogChunk(
                    command_id=cmd_id,
                    pod_name=p.pod_name,
                    namespace=p.namespace,
                    data=data,
                    eof=True,
                ),
            )

        elif which == "config_sync":
            p = command.config_sync
            import json as _json
            from app.services import config_cache
            try:
                desired = _json.loads(p.desired_config_json)
            except Exception:
                desired = {}
            desired["config_version"] = p.config_version
            config_cache.save(desired)
            # Apply all running deployments from the synced config.
            applied_errors = []
            for dep in desired.get("deployments", []):
                try:
                    await loop.run_in_executor(
                        None,
                        partial(k8s_manager.apply_manifests, dep["manifests"], dep["namespace"]),
                    )
                except Exception as exc:
                    applied_errors.append(str(exc))
            if applied_errors:
                return _ack(cmd_id, False, "; ".join(applied_errors), "{}")
            return _ack(cmd_id, True, f"synced v={p.config_version}", "{}")

        else:
            logger.warning("Unhandled command type: %s", which)
            return _ack(cmd_id, False, f"unhandled command: {which}", "{}")

    except Exception as exc:
        logger.error("Command %s (%s) failed: %s", cmd_id, which, exc)
        return _ack(cmd_id, False, str(exc), "{}")


def _ack(command_id: str, success: bool, message: str, result_json: str):
    from edgedeploy.v1 import edge_control_pb2
    return edge_control_pb2.EdgeReport(
        device_uuid=settings.device_uuid,
        command_ack=edge_control_pb2.CommandAck(
            command_id=command_id,
            success=success,
            message=message,
            result_json=result_json,
        ),
    )
