import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from edgedeploy.v1 import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterRequest(_message.Message):
    __slots__ = ("provisioning_token", "device_name", "csr_pem")
    PROVISIONING_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    CSR_PEM_FIELD_NUMBER: _ClassVar[int]
    provisioning_token: str
    device_name: str
    csr_pem: str
    def __init__(self, provisioning_token: _Optional[str] = ..., device_name: _Optional[str] = ..., csr_pem: _Optional[str] = ...) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ("device_uuid", "cert_pem", "ca_cert_pem")
    DEVICE_UUID_FIELD_NUMBER: _ClassVar[int]
    CERT_PEM_FIELD_NUMBER: _ClassVar[int]
    CA_CERT_PEM_FIELD_NUMBER: _ClassVar[int]
    device_uuid: str
    cert_pem: str
    ca_cert_pem: str
    def __init__(self, device_uuid: _Optional[str] = ..., cert_pem: _Optional[str] = ..., ca_cert_pem: _Optional[str] = ...) -> None: ...

class EdgeReport(_message.Message):
    __slots__ = ("device_uuid", "heartbeat", "status_report", "command_ack", "resource_snapshot", "log_chunk")
    DEVICE_UUID_FIELD_NUMBER: _ClassVar[int]
    HEARTBEAT_FIELD_NUMBER: _ClassVar[int]
    STATUS_REPORT_FIELD_NUMBER: _ClassVar[int]
    COMMAND_ACK_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    LOG_CHUNK_FIELD_NUMBER: _ClassVar[int]
    device_uuid: str
    heartbeat: Heartbeat
    status_report: StatusReport
    command_ack: CommandAck
    resource_snapshot: ResourceSnapshot
    log_chunk: LogChunk
    def __init__(self, device_uuid: _Optional[str] = ..., heartbeat: _Optional[_Union[Heartbeat, _Mapping]] = ..., status_report: _Optional[_Union[StatusReport, _Mapping]] = ..., command_ack: _Optional[_Union[CommandAck, _Mapping]] = ..., resource_snapshot: _Optional[_Union[ResourceSnapshot, _Mapping]] = ..., log_chunk: _Optional[_Union[LogChunk, _Mapping]] = ...) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = ("ts", "agent_version", "config_version", "cpu_usage_percent", "memory_usage_percent")
    TS_FIELD_NUMBER: _ClassVar[int]
    AGENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    CPU_USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    ts: _timestamp_pb2.Timestamp
    agent_version: str
    config_version: int
    cpu_usage_percent: float
    memory_usage_percent: float
    def __init__(self, ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., agent_version: _Optional[str] = ..., config_version: _Optional[int] = ..., cpu_usage_percent: _Optional[float] = ..., memory_usage_percent: _Optional[float] = ...) -> None: ...

class StatusReport(_message.Message):
    __slots__ = ("device_uuid", "status", "message", "ts")
    DEVICE_UUID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    device_uuid: str
    status: str
    message: str
    ts: _timestamp_pb2.Timestamp
    def __init__(self, device_uuid: _Optional[str] = ..., status: _Optional[str] = ..., message: _Optional[str] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CommandAck(_message.Message):
    __slots__ = ("command_id", "success", "message", "result_json")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESULT_JSON_FIELD_NUMBER: _ClassVar[int]
    command_id: str
    success: bool
    message: str
    result_json: str
    def __init__(self, command_id: _Optional[str] = ..., success: bool = ..., message: _Optional[str] = ..., result_json: _Optional[str] = ...) -> None: ...

class ResourceSnapshot(_message.Message):
    __slots__ = ("command_id", "namespace", "resources_json")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_JSON_FIELD_NUMBER: _ClassVar[int]
    command_id: str
    namespace: str
    resources_json: str
    def __init__(self, command_id: _Optional[str] = ..., namespace: _Optional[str] = ..., resources_json: _Optional[str] = ...) -> None: ...

class LogChunk(_message.Message):
    __slots__ = ("command_id", "pod_name", "namespace", "data", "eof")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    EOF_FIELD_NUMBER: _ClassVar[int]
    command_id: str
    pod_name: str
    namespace: str
    data: bytes
    eof: bool
    def __init__(self, command_id: _Optional[str] = ..., pod_name: _Optional[str] = ..., namespace: _Optional[str] = ..., data: _Optional[bytes] = ..., eof: bool = ...) -> None: ...

class EdgeCommand(_message.Message):
    __slots__ = ("command_id", "apply_manifests", "delete_resource", "restart_deployment", "get_resources", "get_pod_logs", "config_sync")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    APPLY_MANIFESTS_FIELD_NUMBER: _ClassVar[int]
    DELETE_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    RESTART_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    GET_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    GET_POD_LOGS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_SYNC_FIELD_NUMBER: _ClassVar[int]
    command_id: str
    apply_manifests: ApplyManifestsCommand
    delete_resource: DeleteResourceCommand
    restart_deployment: RestartDeploymentCommand
    get_resources: GetResourcesCommand
    get_pod_logs: GetPodLogsCommand
    config_sync: ConfigSyncCommand
    def __init__(self, command_id: _Optional[str] = ..., apply_manifests: _Optional[_Union[ApplyManifestsCommand, _Mapping]] = ..., delete_resource: _Optional[_Union[DeleteResourceCommand, _Mapping]] = ..., restart_deployment: _Optional[_Union[RestartDeploymentCommand, _Mapping]] = ..., get_resources: _Optional[_Union[GetResourcesCommand, _Mapping]] = ..., get_pod_logs: _Optional[_Union[GetPodLogsCommand, _Mapping]] = ..., config_sync: _Optional[_Union[ConfigSyncCommand, _Mapping]] = ...) -> None: ...

class ApplyManifestsCommand(_message.Message):
    __slots__ = ("manifests", "namespace")
    MANIFESTS_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    manifests: str
    namespace: str
    def __init__(self, manifests: _Optional[str] = ..., namespace: _Optional[str] = ...) -> None: ...

class DeleteResourceCommand(_message.Message):
    __slots__ = ("namespace", "kind", "name")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    kind: str
    name: str
    def __init__(self, namespace: _Optional[str] = ..., kind: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class RestartDeploymentCommand(_message.Message):
    __slots__ = ("namespace", "name")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    name: str
    def __init__(self, namespace: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class GetResourcesCommand(_message.Message):
    __slots__ = ("namespace",)
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    def __init__(self, namespace: _Optional[str] = ...) -> None: ...

class GetPodLogsCommand(_message.Message):
    __slots__ = ("namespace", "pod_name", "tail")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    TAIL_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    pod_name: str
    tail: int
    def __init__(self, namespace: _Optional[str] = ..., pod_name: _Optional[str] = ..., tail: _Optional[int] = ...) -> None: ...

class ConfigSyncCommand(_message.Message):
    __slots__ = ("desired_config_json", "config_version")
    DESIRED_CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    desired_config_json: str
    config_version: int
    def __init__(self, desired_config_json: _Optional[str] = ..., config_version: _Optional[int] = ...) -> None: ...
