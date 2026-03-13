"""Kubernetes manager: apply/delete/status/restart/logs via dynamic client."""
import logging
from typing import Any

import yaml
from kubernetes import client, config as k8s_config
from kubernetes.client.exceptions import ApiException
from kubernetes.dynamic import DynamicClient

logger = logging.getLogger(__name__)


def load_k8s_config(in_cluster: bool = True) -> None:
    if in_cluster:
        k8s_config.load_incluster_config()
    else:
        k8s_config.load_kube_config()


def _get_dynamic_client() -> DynamicClient:
    return DynamicClient(client.ApiClient())


def apply_manifests(yaml_str: str, namespace: str = "default") -> dict[str, Any]:
    """Parse multi-doc YAML and apply each resource (create or patch)."""
    docs = list(yaml.safe_load_all(yaml_str))
    applied = []
    errors = []

    dyn = _get_dynamic_client()

    for doc in docs:
        if doc is None:
            continue
        try:
            api_version = doc.get("apiVersion", "v1")
            kind = doc.get("kind", "")
            name = doc.get("metadata", {}).get("name", "")
            ns = doc.get("metadata", {}).get("namespace", namespace)

            resource = dyn.resources.get(api_version=api_version, kind=kind)

            # Try to get existing resource
            try:
                resource.get(name=name, namespace=ns)
                # Exists — patch it
                result = resource.patch(
                    body=doc,
                    name=name,
                    namespace=ns,
                    content_type="application/merge-patch+json",
                )
                action = "patched"
            except ApiException as e:
                if e.status == 404:
                    result = resource.create(body=doc, namespace=ns)
                    action = "created"
                else:
                    raise

            applied.append(
                {
                    "kind": kind,
                    "name": name,
                    "namespace": ns,
                    "action": action,
                }
            )
            logger.info("%s %s/%s in %s", action, kind, name, ns)
        except Exception as exc:
            msg = f"{doc.get('kind','?')}/{doc.get('metadata',{}).get('name','?')}: {exc}"
            logger.error("apply error: %s", msg)
            errors.append(msg)

    return {"applied": applied, "errors": errors}


def get_resources(namespace: str) -> dict[str, Any]:
    """Return deployments, services, pods in a namespace."""
    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()

    deployments = []
    try:
        for d in apps_v1.list_namespaced_deployment(namespace).items:
            deployments.append(_deployment_summary(d))
    except ApiException as e:
        logger.warning("list deployments: %s", e)

    services = []
    try:
        for s in core_v1.list_namespaced_service(namespace).items:
            services.append(_service_summary(s))
    except ApiException as e:
        logger.warning("list services: %s", e)

    pods = []
    try:
        for p in core_v1.list_namespaced_pod(namespace).items:
            pods.append(_pod_summary(p))
    except ApiException as e:
        logger.warning("list pods: %s", e)

    return {"deployments": deployments, "services": services, "pods": pods}


def get_resource(namespace: str, kind: str, name: str) -> dict[str, Any]:
    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()

    kind_lower = kind.lower()
    if kind_lower == "deployment":
        obj = apps_v1.read_namespaced_deployment(name, namespace)
        summary = _deployment_summary(obj)
        pods = _pods_for_selector(
            namespace,
            obj.spec.selector.match_labels,
        )
        summary["pods"] = pods
        return summary
    elif kind_lower == "service":
        obj = core_v1.read_namespaced_service(name, namespace)
        return _service_summary(obj)
    elif kind_lower == "pod":
        obj = core_v1.read_namespaced_pod(name, namespace)
        return _pod_summary(obj)
    else:
        dyn = _get_dynamic_client()
        resource = dyn.resources.get(api_version="v1", kind=kind)
        result = resource.get(name=name, namespace=namespace)
        return result.to_dict()


def delete_resource(namespace: str, kind: str, name: str) -> None:
    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()

    kind_lower = kind.lower()
    if kind_lower == "deployment":
        apps_v1.delete_namespaced_deployment(name, namespace)
    elif kind_lower == "service":
        core_v1.delete_namespaced_service(name, namespace)
    elif kind_lower == "pod":
        core_v1.delete_namespaced_pod(name, namespace)
    else:
        dyn = _get_dynamic_client()
        resource = dyn.resources.get(api_version="v1", kind=kind)
        resource.delete(name=name, namespace=namespace)


def restart_deployment(namespace: str, name: str) -> None:
    """Trigger rolling restart by patching annotations."""
    import datetime

    apps_v1 = client.AppsV1Api()
    patch = {
        "spec": {
            "template": {
                "metadata": {
                    "annotations": {
                        "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow().isoformat()
                    }
                }
            }
        }
    }
    apps_v1.patch_namespaced_deployment(name, namespace, patch)


def get_pod_logs(namespace: str, pod_name: str, container: str | None = None, tail: int = 200) -> str:
    core_v1 = client.CoreV1Api()
    kwargs: dict[str, Any] = {"tail_lines": tail}
    if container:
        kwargs["container"] = container
    return core_v1.read_namespaced_pod_log(pod_name, namespace, **kwargs)


def check_k3s_connectivity() -> tuple[bool, str]:
    try:
        v1 = client.VersionApi()
        info = v1.get_code()
        return True, info.git_version
    except Exception as e:
        return False, str(e)


# ---- helpers ----

def _deployment_summary(d: Any) -> dict[str, Any]:
    status = d.status
    return {
        "kind": "Deployment",
        "name": d.metadata.name,
        "namespace": d.metadata.namespace,
        "replicas": d.spec.replicas,
        "ready_replicas": status.ready_replicas or 0,
        "available_replicas": status.available_replicas or 0,
        "updated_replicas": status.updated_replicas or 0,
        "conditions": [
            {"type": c.type, "status": c.status, "message": c.message}
            for c in (status.conditions or [])
        ],
    }


def _service_summary(s: Any) -> dict[str, Any]:
    return {
        "kind": "Service",
        "name": s.metadata.name,
        "namespace": s.metadata.namespace,
        "type": s.spec.type,
        "cluster_ip": s.spec.cluster_ip,
        "ports": [
            {
                "port": p.port,
                "target_port": str(p.target_port),
                "node_port": p.node_port,
                "protocol": p.protocol,
            }
            for p in (s.spec.ports or [])
        ],
    }


def _pod_summary(p: Any) -> dict[str, Any]:
    return {
        "name": p.metadata.name,
        "namespace": p.metadata.namespace,
        "phase": p.status.phase,
        "node": p.spec.node_name,
        "ip": p.status.pod_ip,
        "containers": [
            {
                "name": cs.name,
                "ready": cs.ready,
                "restart_count": cs.restart_count,
                "state": _container_state(cs.state),
            }
            for cs in (p.status.container_statuses or [])
        ],
    }


def _container_state(state: Any) -> str:
    if state.running:
        return "running"
    if state.waiting:
        return f"waiting:{state.waiting.reason}"
    if state.terminated:
        return f"terminated:{state.terminated.reason}"
    return "unknown"


def _pods_for_selector(namespace: str, labels: dict[str, str]) -> list[dict[str, Any]]:
    core_v1 = client.CoreV1Api()
    selector = ",".join(f"{k}={v}" for k, v in labels.items())
    pods = core_v1.list_namespaced_pod(namespace, label_selector=selector)
    return [_pod_summary(p) for p in pods.items]
