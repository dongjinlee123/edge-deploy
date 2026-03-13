"""Generate K8s YAML from form input using Jinja2 templates."""
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader

_TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
_jinja_env = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)), trim_blocks=True, lstrip_blocks=True)


def build_manifests(
    name: str,
    image: str,
    tag: str,
    replicas: int,
    namespace: str,
    port: Optional[int] = None,
    env: Optional[dict] = None,
) -> str:
    """Render Deployment + optional Service YAML, separated by ---."""
    ctx = {
        "name": name,
        "image": image,
        "tag": tag,
        "replicas": replicas,
        "namespace": namespace,
        "port": port,
        "env": env or {},
    }

    deployment_yaml = _jinja_env.get_template("deployment.yaml.j2").render(**ctx)
    parts = [deployment_yaml]

    if port:
        service_yaml = _jinja_env.get_template("service.yaml.j2").render(**ctx)
        parts.append(service_yaml)

    return "\n---\n".join(parts)
