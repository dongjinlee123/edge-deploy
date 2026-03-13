import * as jspb from 'google-protobuf'

import * as google_protobuf_timestamp_pb from 'google-protobuf/google/protobuf/timestamp_pb'; // proto import: "google/protobuf/timestamp.proto"
import * as edgedeploy_v1_common_pb from '../../edgedeploy/v1/common_pb'; // proto import: "edgedeploy/v1/common.proto"


export class DeviceProto extends jspb.Message {
  getId(): number;
  setId(value: number): DeviceProto;

  getName(): string;
  setName(value: string): DeviceProto;

  getAddress(): string;
  setAddress(value: string): DeviceProto;

  getAgentPort(): number;
  setAgentPort(value: number): DeviceProto;

  getStatus(): string;
  setStatus(value: string): DeviceProto;

  getLastSeen(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setLastSeen(value?: google_protobuf_timestamp_pb.Timestamp): DeviceProto;
  hasLastSeen(): boolean;
  clearLastSeen(): DeviceProto;

  getLabels(): edgedeploy_v1_common_pb.Labels | undefined;
  setLabels(value?: edgedeploy_v1_common_pb.Labels): DeviceProto;
  hasLabels(): boolean;
  clearLabels(): DeviceProto;

  getCreatedAt(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setCreatedAt(value?: google_protobuf_timestamp_pb.Timestamp): DeviceProto;
  hasCreatedAt(): boolean;
  clearCreatedAt(): DeviceProto;

  getDeviceUuid(): string;
  setDeviceUuid(value: string): DeviceProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeviceProto.AsObject;
  static toObject(includeInstance: boolean, msg: DeviceProto): DeviceProto.AsObject;
  static serializeBinaryToWriter(message: DeviceProto, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeviceProto;
  static deserializeBinaryFromReader(message: DeviceProto, reader: jspb.BinaryReader): DeviceProto;
}

export namespace DeviceProto {
  export type AsObject = {
    id: number;
    name: string;
    address: string;
    agentPort: number;
    status: string;
    lastSeen?: google_protobuf_timestamp_pb.Timestamp.AsObject;
    labels?: edgedeploy_v1_common_pb.Labels.AsObject;
    createdAt?: google_protobuf_timestamp_pb.Timestamp.AsObject;
    deviceUuid: string;
  };
}

export class ListDevicesRequest extends jspb.Message {
  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ListDevicesRequest.AsObject;
  static toObject(includeInstance: boolean, msg: ListDevicesRequest): ListDevicesRequest.AsObject;
  static serializeBinaryToWriter(message: ListDevicesRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ListDevicesRequest;
  static deserializeBinaryFromReader(message: ListDevicesRequest, reader: jspb.BinaryReader): ListDevicesRequest;
}

export namespace ListDevicesRequest {
  export type AsObject = {
  };
}

export class ListDevicesResponse extends jspb.Message {
  getDevicesList(): Array<DeviceProto>;
  setDevicesList(value: Array<DeviceProto>): ListDevicesResponse;
  clearDevicesList(): ListDevicesResponse;
  addDevices(value?: DeviceProto, index?: number): DeviceProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ListDevicesResponse.AsObject;
  static toObject(includeInstance: boolean, msg: ListDevicesResponse): ListDevicesResponse.AsObject;
  static serializeBinaryToWriter(message: ListDevicesResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ListDevicesResponse;
  static deserializeBinaryFromReader(message: ListDevicesResponse, reader: jspb.BinaryReader): ListDevicesResponse;
}

export namespace ListDevicesResponse {
  export type AsObject = {
    devicesList: Array<DeviceProto.AsObject>;
  };
}

export class GetDeviceRequest extends jspb.Message {
  getId(): number;
  setId(value: number): GetDeviceRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GetDeviceRequest.AsObject;
  static toObject(includeInstance: boolean, msg: GetDeviceRequest): GetDeviceRequest.AsObject;
  static serializeBinaryToWriter(message: GetDeviceRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GetDeviceRequest;
  static deserializeBinaryFromReader(message: GetDeviceRequest, reader: jspb.BinaryReader): GetDeviceRequest;
}

export namespace GetDeviceRequest {
  export type AsObject = {
    id: number;
  };
}

export class CreateDeviceRequest extends jspb.Message {
  getName(): string;
  setName(value: string): CreateDeviceRequest;

  getAddress(): string;
  setAddress(value: string): CreateDeviceRequest;

  getAgentPort(): number;
  setAgentPort(value: number): CreateDeviceRequest;

  getLabels(): edgedeploy_v1_common_pb.Labels | undefined;
  setLabels(value?: edgedeploy_v1_common_pb.Labels): CreateDeviceRequest;
  hasLabels(): boolean;
  clearLabels(): CreateDeviceRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CreateDeviceRequest.AsObject;
  static toObject(includeInstance: boolean, msg: CreateDeviceRequest): CreateDeviceRequest.AsObject;
  static serializeBinaryToWriter(message: CreateDeviceRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CreateDeviceRequest;
  static deserializeBinaryFromReader(message: CreateDeviceRequest, reader: jspb.BinaryReader): CreateDeviceRequest;
}

export namespace CreateDeviceRequest {
  export type AsObject = {
    name: string;
    address: string;
    agentPort: number;
    labels?: edgedeploy_v1_common_pb.Labels.AsObject;
  };
}

export class UpdateDeviceRequest extends jspb.Message {
  getId(): number;
  setId(value: number): UpdateDeviceRequest;

  getName(): string;
  setName(value: string): UpdateDeviceRequest;

  getAddress(): string;
  setAddress(value: string): UpdateDeviceRequest;

  getAgentPort(): number;
  setAgentPort(value: number): UpdateDeviceRequest;

  getLabels(): edgedeploy_v1_common_pb.Labels | undefined;
  setLabels(value?: edgedeploy_v1_common_pb.Labels): UpdateDeviceRequest;
  hasLabels(): boolean;
  clearLabels(): UpdateDeviceRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): UpdateDeviceRequest.AsObject;
  static toObject(includeInstance: boolean, msg: UpdateDeviceRequest): UpdateDeviceRequest.AsObject;
  static serializeBinaryToWriter(message: UpdateDeviceRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): UpdateDeviceRequest;
  static deserializeBinaryFromReader(message: UpdateDeviceRequest, reader: jspb.BinaryReader): UpdateDeviceRequest;
}

export namespace UpdateDeviceRequest {
  export type AsObject = {
    id: number;
    name: string;
    address: string;
    agentPort: number;
    labels?: edgedeploy_v1_common_pb.Labels.AsObject;
  };
}

export class DeleteDeviceRequest extends jspb.Message {
  getId(): number;
  setId(value: number): DeleteDeviceRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeleteDeviceRequest.AsObject;
  static toObject(includeInstance: boolean, msg: DeleteDeviceRequest): DeleteDeviceRequest.AsObject;
  static serializeBinaryToWriter(message: DeleteDeviceRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeleteDeviceRequest;
  static deserializeBinaryFromReader(message: DeleteDeviceRequest, reader: jspb.BinaryReader): DeleteDeviceRequest;
}

export namespace DeleteDeviceRequest {
  export type AsObject = {
    id: number;
  };
}

export class DeleteDeviceResponse extends jspb.Message {
  getOk(): boolean;
  setOk(value: boolean): DeleteDeviceResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeleteDeviceResponse.AsObject;
  static toObject(includeInstance: boolean, msg: DeleteDeviceResponse): DeleteDeviceResponse.AsObject;
  static serializeBinaryToWriter(message: DeleteDeviceResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeleteDeviceResponse;
  static deserializeBinaryFromReader(message: DeleteDeviceResponse, reader: jspb.BinaryReader): DeleteDeviceResponse;
}

export namespace DeleteDeviceResponse {
  export type AsObject = {
    ok: boolean;
  };
}

export class PingDeviceRequest extends jspb.Message {
  getId(): number;
  setId(value: number): PingDeviceRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): PingDeviceRequest.AsObject;
  static toObject(includeInstance: boolean, msg: PingDeviceRequest): PingDeviceRequest.AsObject;
  static serializeBinaryToWriter(message: PingDeviceRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): PingDeviceRequest;
  static deserializeBinaryFromReader(message: PingDeviceRequest, reader: jspb.BinaryReader): PingDeviceRequest;
}

export namespace PingDeviceRequest {
  export type AsObject = {
    id: number;
  };
}

export class PingDeviceResponse extends jspb.Message {
  getReachable(): boolean;
  setReachable(value: boolean): PingDeviceResponse;

  getMessage(): string;
  setMessage(value: string): PingDeviceResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): PingDeviceResponse.AsObject;
  static toObject(includeInstance: boolean, msg: PingDeviceResponse): PingDeviceResponse.AsObject;
  static serializeBinaryToWriter(message: PingDeviceResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): PingDeviceResponse;
  static deserializeBinaryFromReader(message: PingDeviceResponse, reader: jspb.BinaryReader): PingDeviceResponse;
}

export namespace PingDeviceResponse {
  export type AsObject = {
    reachable: boolean;
    message: string;
  };
}

