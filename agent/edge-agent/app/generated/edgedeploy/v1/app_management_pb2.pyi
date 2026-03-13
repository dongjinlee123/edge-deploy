import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AppProto(_message.Message):
    __slots__ = ("id", "name", "image", "default_tag", "default_replicas", "default_port", "default_env_json", "yaml_template", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TAG_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PORT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ENV_JSON_FIELD_NUMBER: _ClassVar[int]
    YAML_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    image: str
    default_tag: str
    default_replicas: int
    default_port: int
    default_env_json: str
    yaml_template: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., image: _Optional[str] = ..., default_tag: _Optional[str] = ..., default_replicas: _Optional[int] = ..., default_port: _Optional[int] = ..., default_env_json: _Optional[str] = ..., yaml_template: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ListAppsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListAppsResponse(_message.Message):
    __slots__ = ("apps",)
    APPS_FIELD_NUMBER: _ClassVar[int]
    apps: _containers.RepeatedCompositeFieldContainer[AppProto]
    def __init__(self, apps: _Optional[_Iterable[_Union[AppProto, _Mapping]]] = ...) -> None: ...

class GetAppRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class CreateAppRequest(_message.Message):
    __slots__ = ("name", "image", "default_tag", "default_replicas", "default_port", "default_env_json", "yaml_template")
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TAG_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PORT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ENV_JSON_FIELD_NUMBER: _ClassVar[int]
    YAML_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    image: str
    default_tag: str
    default_replicas: int
    default_port: int
    default_env_json: str
    yaml_template: str
    def __init__(self, name: _Optional[str] = ..., image: _Optional[str] = ..., default_tag: _Optional[str] = ..., default_replicas: _Optional[int] = ..., default_port: _Optional[int] = ..., default_env_json: _Optional[str] = ..., yaml_template: _Optional[str] = ...) -> None: ...

class UpdateAppRequest(_message.Message):
    __slots__ = ("id", "name", "image", "default_tag", "default_replicas", "default_port", "default_env_json", "yaml_template")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TAG_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PORT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ENV_JSON_FIELD_NUMBER: _ClassVar[int]
    YAML_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    image: str
    default_tag: str
    default_replicas: int
    default_port: int
    default_env_json: str
    yaml_template: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., image: _Optional[str] = ..., default_tag: _Optional[str] = ..., default_replicas: _Optional[int] = ..., default_port: _Optional[int] = ..., default_env_json: _Optional[str] = ..., yaml_template: _Optional[str] = ...) -> None: ...

class DeleteAppRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteAppResponse(_message.Message):
    __slots__ = ("ok",)
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...
