import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeploymentProto(_message.Message):
    __slots__ = ("id", "app_id", "device_id", "namespace", "manifests", "status", "status_message", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    MANIFESTS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    app_id: int
    device_id: int
    namespace: str
    manifests: str
    status: str
    status_message: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., app_id: _Optional[int] = ..., device_id: _Optional[int] = ..., namespace: _Optional[str] = ..., manifests: _Optional[str] = ..., status: _Optional[str] = ..., status_message: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class DeploymentLogProto(_message.Message):
    __slots__ = ("id", "deployment_id", "action", "detail_json", "status", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    DETAIL_JSON_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    deployment_id: int
    action: str
    detail_json: str
    status: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., deployment_id: _Optional[int] = ..., action: _Optional[str] = ..., detail_json: _Optional[str] = ..., status: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListDeploymentsRequest(_message.Message):
    __slots__ = ("device_id", "app_id", "status")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    device_id: int
    app_id: int
    status: str
    def __init__(self, device_id: _Optional[int] = ..., app_id: _Optional[int] = ..., status: _Optional[str] = ...) -> None: ...

class ListDeploymentsResponse(_message.Message):
    __slots__ = ("deployments",)
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[DeploymentProto]
    def __init__(self, deployments: _Optional[_Iterable[_Union[DeploymentProto, _Mapping]]] = ...) -> None: ...

class GetDeploymentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class CreateFormDeploymentRequest(_message.Message):
    __slots__ = ("app_id", "device_id", "namespace", "tag", "replicas")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    app_id: int
    device_id: int
    namespace: str
    tag: str
    replicas: int
    def __init__(self, app_id: _Optional[int] = ..., device_id: _Optional[int] = ..., namespace: _Optional[str] = ..., tag: _Optional[str] = ..., replicas: _Optional[int] = ...) -> None: ...

class CreateYamlDeploymentRequest(_message.Message):
    __slots__ = ("device_id", "namespace", "manifests")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    MANIFESTS_FIELD_NUMBER: _ClassVar[int]
    device_id: int
    namespace: str
    manifests: str
    def __init__(self, device_id: _Optional[int] = ..., namespace: _Optional[str] = ..., manifests: _Optional[str] = ...) -> None: ...

class DeleteDeploymentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteDeploymentResponse(_message.Message):
    __slots__ = ("ok",)
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...

class RestartDeploymentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class RestartDeploymentResponse(_message.Message):
    __slots__ = ("ok",)
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...

class GetDeploymentLogsRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetDeploymentLogsResponse(_message.Message):
    __slots__ = ("logs",)
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[DeploymentLogProto]
    def __init__(self, logs: _Optional[_Iterable[_Union[DeploymentLogProto, _Mapping]]] = ...) -> None: ...

class BulkDeployRequest(_message.Message):
    __slots__ = ("app_id", "device_ids", "namespace", "tag", "replicas")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_IDS_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    app_id: int
    device_ids: _containers.RepeatedScalarFieldContainer[int]
    namespace: str
    tag: str
    replicas: int
    def __init__(self, app_id: _Optional[int] = ..., device_ids: _Optional[_Iterable[int]] = ..., namespace: _Optional[str] = ..., tag: _Optional[str] = ..., replicas: _Optional[int] = ...) -> None: ...

class BulkDeployResponse(_message.Message):
    __slots__ = ("deployments",)
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[DeploymentProto]
    def __init__(self, deployments: _Optional[_Iterable[_Union[DeploymentProto, _Mapping]]] = ...) -> None: ...

class GetOverviewRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class OverviewProto(_message.Message):
    __slots__ = ("total_devices", "online_devices", "total_apps", "total_deployments", "running_deployments", "failed_deployments")
    TOTAL_DEVICES_FIELD_NUMBER: _ClassVar[int]
    ONLINE_DEVICES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_APPS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    RUNNING_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    FAILED_DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    total_devices: int
    online_devices: int
    total_apps: int
    total_deployments: int
    running_deployments: int
    failed_deployments: int
    def __init__(self, total_devices: _Optional[int] = ..., online_devices: _Optional[int] = ..., total_apps: _Optional[int] = ..., total_deployments: _Optional[int] = ..., running_deployments: _Optional[int] = ..., failed_deployments: _Optional[int] = ...) -> None: ...
