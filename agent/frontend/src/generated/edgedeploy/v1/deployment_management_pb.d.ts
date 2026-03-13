import * as jspb from 'google-protobuf'

import * as google_protobuf_timestamp_pb from 'google-protobuf/google/protobuf/timestamp_pb'; // proto import: "google/protobuf/timestamp.proto"


export class DeploymentProto extends jspb.Message {
  getId(): number;
  setId(value: number): DeploymentProto;

  getAppId(): number;
  setAppId(value: number): DeploymentProto;

  getDeviceId(): number;
  setDeviceId(value: number): DeploymentProto;

  getNamespace(): string;
  setNamespace(value: string): DeploymentProto;

  getManifests(): string;
  setManifests(value: string): DeploymentProto;

  getStatus(): string;
  setStatus(value: string): DeploymentProto;

  getStatusMessage(): string;
  setStatusMessage(value: string): DeploymentProto;

  getCreatedAt(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setCreatedAt(value?: google_protobuf_timestamp_pb.Timestamp): DeploymentProto;
  hasCreatedAt(): boolean;
  clearCreatedAt(): DeploymentProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeploymentProto.AsObject;
  static toObject(includeInstance: boolean, msg: DeploymentProto): DeploymentProto.AsObject;
  static serializeBinaryToWriter(message: DeploymentProto, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeploymentProto;
  static deserializeBinaryFromReader(message: DeploymentProto, reader: jspb.BinaryReader): DeploymentProto;
}

export namespace DeploymentProto {
  export type AsObject = {
    id: number;
    appId: number;
    deviceId: number;
    namespace: string;
    manifests: string;
    status: string;
    statusMessage: string;
    createdAt?: google_protobuf_timestamp_pb.Timestamp.AsObject;
  };
}

export class DeploymentLogProto extends jspb.Message {
  getId(): number;
  setId(value: number): DeploymentLogProto;

  getDeploymentId(): number;
  setDeploymentId(value: number): DeploymentLogProto;

  getAction(): string;
  setAction(value: string): DeploymentLogProto;

  getDetailJson(): string;
  setDetailJson(value: string): DeploymentLogProto;

  getStatus(): string;
  setStatus(value: string): DeploymentLogProto;

  getCreatedAt(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setCreatedAt(value?: google_protobuf_timestamp_pb.Timestamp): DeploymentLogProto;
  hasCreatedAt(): boolean;
  clearCreatedAt(): DeploymentLogProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeploymentLogProto.AsObject;
  static toObject(includeInstance: boolean, msg: DeploymentLogProto): DeploymentLogProto.AsObject;
  static serializeBinaryToWriter(message: DeploymentLogProto, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeploymentLogProto;
  static deserializeBinaryFromReader(message: DeploymentLogProto, reader: jspb.BinaryReader): DeploymentLogProto;
}

export namespace DeploymentLogProto {
  export type AsObject = {
    id: number;
    deploymentId: number;
    action: string;
    detailJson: string;
    status: string;
    createdAt?: google_protobuf_timestamp_pb.Timestamp.AsObject;
  };
}

export class ListDeploymentsRequest extends jspb.Message {
  getDeviceId(): number;
  setDeviceId(value: number): ListDeploymentsRequest;
  hasDeviceId(): boolean;
  clearDeviceId(): ListDeploymentsRequest;

  getAppId(): number;
  setAppId(value: number): ListDeploymentsRequest;
  hasAppId(): boolean;
  clearAppId(): ListDeploymentsRequest;

  getStatus(): string;
  setStatus(value: string): ListDeploymentsRequest;
  hasStatus(): boolean;
  clearStatus(): ListDeploymentsRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ListDeploymentsRequest.AsObject;
  static toObject(includeInstance: boolean, msg: ListDeploymentsRequest): ListDeploymentsRequest.AsObject;
  static serializeBinaryToWriter(message: ListDeploymentsRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ListDeploymentsRequest;
  static deserializeBinaryFromReader(message: ListDeploymentsRequest, reader: jspb.BinaryReader): ListDeploymentsRequest;
}

export namespace ListDeploymentsRequest {
  export type AsObject = {
    deviceId?: number;
    appId?: number;
    status?: string;
  };

  export enum DeviceIdCase {
    _DEVICE_ID_NOT_SET = 0,
    DEVICE_ID = 1,
  }

  export enum AppIdCase {
    _APP_ID_NOT_SET = 0,
    APP_ID = 2,
  }

  export enum StatusCase {
    _STATUS_NOT_SET = 0,
    STATUS = 3,
  }
}

export class ListDeploymentsResponse extends jspb.Message {
  getDeploymentsList(): Array<DeploymentProto>;
  setDeploymentsList(value: Array<DeploymentProto>): ListDeploymentsResponse;
  clearDeploymentsList(): ListDeploymentsResponse;
  addDeployments(value?: DeploymentProto, index?: number): DeploymentProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ListDeploymentsResponse.AsObject;
  static toObject(includeInstance: boolean, msg: ListDeploymentsResponse): ListDeploymentsResponse.AsObject;
  static serializeBinaryToWriter(message: ListDeploymentsResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ListDeploymentsResponse;
  static deserializeBinaryFromReader(message: ListDeploymentsResponse, reader: jspb.BinaryReader): ListDeploymentsResponse;
}

export namespace ListDeploymentsResponse {
  export type AsObject = {
    deploymentsList: Array<DeploymentProto.AsObject>;
  };
}

export class GetDeploymentRequest extends jspb.Message {
  getId(): number;
  setId(value: number): GetDeploymentRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GetDeploymentRequest.AsObject;
  static toObject(includeInstance: boolean, msg: GetDeploymentRequest): GetDeploymentRequest.AsObject;
  static serializeBinaryToWriter(message: GetDeploymentRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GetDeploymentRequest;
  static deserializeBinaryFromReader(message: GetDeploymentRequest, reader: jspb.BinaryReader): GetDeploymentRequest;
}

export namespace GetDeploymentRequest {
  export type AsObject = {
    id: number;
  };
}

export class CreateFormDeploymentRequest extends jspb.Message {
  getAppId(): number;
  setAppId(value: number): CreateFormDeploymentRequest;

  getDeviceId(): number;
  setDeviceId(value: number): CreateFormDeploymentRequest;

  getNamespace(): string;
  setNamespace(value: string): CreateFormDeploymentRequest;

  getTag(): string;
  setTag(value: string): CreateFormDeploymentRequest;

  getReplicas(): number;
  setReplicas(value: number): CreateFormDeploymentRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CreateFormDeploymentRequest.AsObject;
  static toObject(includeInstance: boolean, msg: CreateFormDeploymentRequest): CreateFormDeploymentRequest.AsObject;
  static serializeBinaryToWriter(message: CreateFormDeploymentRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CreateFormDeploymentRequest;
  static deserializeBinaryFromReader(message: CreateFormDeploymentRequest, reader: jspb.BinaryReader): CreateFormDeploymentRequest;
}

export namespace CreateFormDeploymentRequest {
  export type AsObject = {
    appId: number;
    deviceId: number;
    namespace: string;
    tag: string;
    replicas: number;
  };
}

export class CreateYamlDeploymentRequest extends jspb.Message {
  getDeviceId(): number;
  setDeviceId(value: number): CreateYamlDeploymentRequest;

  getNamespace(): string;
  setNamespace(value: string): CreateYamlDeploymentRequest;

  getManifests(): string;
  setManifests(value: string): CreateYamlDeploymentRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CreateYamlDeploymentRequest.AsObject;
  static toObject(includeInstance: boolean, msg: CreateYamlDeploymentRequest): CreateYamlDeploymentRequest.AsObject;
  static serializeBinaryToWriter(message: CreateYamlDeploymentRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CreateYamlDeploymentRequest;
  static deserializeBinaryFromReader(message: CreateYamlDeploymentRequest, reader: jspb.BinaryReader): CreateYamlDeploymentRequest;
}

export namespace CreateYamlDeploymentRequest {
  export type AsObject = {
    deviceId: number;
    namespace: string;
    manifests: string;
  };
}

export class DeleteDeploymentRequest extends jspb.Message {
  getId(): number;
  setId(value: number): DeleteDeploymentRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeleteDeploymentRequest.AsObject;
  static toObject(includeInstance: boolean, msg: DeleteDeploymentRequest): DeleteDeploymentRequest.AsObject;
  static serializeBinaryToWriter(message: DeleteDeploymentRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeleteDeploymentRequest;
  static deserializeBinaryFromReader(message: DeleteDeploymentRequest, reader: jspb.BinaryReader): DeleteDeploymentRequest;
}

export namespace DeleteDeploymentRequest {
  export type AsObject = {
    id: number;
  };
}

export class DeleteDeploymentResponse extends jspb.Message {
  getOk(): boolean;
  setOk(value: boolean): DeleteDeploymentResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeleteDeploymentResponse.AsObject;
  static toObject(includeInstance: boolean, msg: DeleteDeploymentResponse): DeleteDeploymentResponse.AsObject;
  static serializeBinaryToWriter(message: DeleteDeploymentResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeleteDeploymentResponse;
  static deserializeBinaryFromReader(message: DeleteDeploymentResponse, reader: jspb.BinaryReader): DeleteDeploymentResponse;
}

export namespace DeleteDeploymentResponse {
  export type AsObject = {
    ok: boolean;
  };
}

export class RestartDeploymentRequest extends jspb.Message {
  getId(): number;
  setId(value: number): RestartDeploymentRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): RestartDeploymentRequest.AsObject;
  static toObject(includeInstance: boolean, msg: RestartDeploymentRequest): RestartDeploymentRequest.AsObject;
  static serializeBinaryToWriter(message: RestartDeploymentRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): RestartDeploymentRequest;
  static deserializeBinaryFromReader(message: RestartDeploymentRequest, reader: jspb.BinaryReader): RestartDeploymentRequest;
}

export namespace RestartDeploymentRequest {
  export type AsObject = {
    id: number;
  };
}

export class RestartDeploymentResponse extends jspb.Message {
  getOk(): boolean;
  setOk(value: boolean): RestartDeploymentResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): RestartDeploymentResponse.AsObject;
  static toObject(includeInstance: boolean, msg: RestartDeploymentResponse): RestartDeploymentResponse.AsObject;
  static serializeBinaryToWriter(message: RestartDeploymentResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): RestartDeploymentResponse;
  static deserializeBinaryFromReader(message: RestartDeploymentResponse, reader: jspb.BinaryReader): RestartDeploymentResponse;
}

export namespace RestartDeploymentResponse {
  export type AsObject = {
    ok: boolean;
  };
}

export class GetDeploymentLogsRequest extends jspb.Message {
  getId(): number;
  setId(value: number): GetDeploymentLogsRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GetDeploymentLogsRequest.AsObject;
  static toObject(includeInstance: boolean, msg: GetDeploymentLogsRequest): GetDeploymentLogsRequest.AsObject;
  static serializeBinaryToWriter(message: GetDeploymentLogsRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GetDeploymentLogsRequest;
  static deserializeBinaryFromReader(message: GetDeploymentLogsRequest, reader: jspb.BinaryReader): GetDeploymentLogsRequest;
}

export namespace GetDeploymentLogsRequest {
  export type AsObject = {
    id: number;
  };
}

export class GetDeploymentLogsResponse extends jspb.Message {
  getLogsList(): Array<DeploymentLogProto>;
  setLogsList(value: Array<DeploymentLogProto>): GetDeploymentLogsResponse;
  clearLogsList(): GetDeploymentLogsResponse;
  addLogs(value?: DeploymentLogProto, index?: number): DeploymentLogProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GetDeploymentLogsResponse.AsObject;
  static toObject(includeInstance: boolean, msg: GetDeploymentLogsResponse): GetDeploymentLogsResponse.AsObject;
  static serializeBinaryToWriter(message: GetDeploymentLogsResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GetDeploymentLogsResponse;
  static deserializeBinaryFromReader(message: GetDeploymentLogsResponse, reader: jspb.BinaryReader): GetDeploymentLogsResponse;
}

export namespace GetDeploymentLogsResponse {
  export type AsObject = {
    logsList: Array<DeploymentLogProto.AsObject>;
  };
}

export class BulkDeployRequest extends jspb.Message {
  getAppId(): number;
  setAppId(value: number): BulkDeployRequest;

  getDeviceIdsList(): Array<number>;
  setDeviceIdsList(value: Array<number>): BulkDeployRequest;
  clearDeviceIdsList(): BulkDeployRequest;
  addDeviceIds(value: number, index?: number): BulkDeployRequest;

  getNamespace(): string;
  setNamespace(value: string): BulkDeployRequest;

  getTag(): string;
  setTag(value: string): BulkDeployRequest;

  getReplicas(): number;
  setReplicas(value: number): BulkDeployRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): BulkDeployRequest.AsObject;
  static toObject(includeInstance: boolean, msg: BulkDeployRequest): BulkDeployRequest.AsObject;
  static serializeBinaryToWriter(message: BulkDeployRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): BulkDeployRequest;
  static deserializeBinaryFromReader(message: BulkDeployRequest, reader: jspb.BinaryReader): BulkDeployRequest;
}

export namespace BulkDeployRequest {
  export type AsObject = {
    appId: number;
    deviceIdsList: Array<number>;
    namespace: string;
    tag: string;
    replicas: number;
  };
}

export class BulkDeployResponse extends jspb.Message {
  getDeploymentsList(): Array<DeploymentProto>;
  setDeploymentsList(value: Array<DeploymentProto>): BulkDeployResponse;
  clearDeploymentsList(): BulkDeployResponse;
  addDeployments(value?: DeploymentProto, index?: number): DeploymentProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): BulkDeployResponse.AsObject;
  static toObject(includeInstance: boolean, msg: BulkDeployResponse): BulkDeployResponse.AsObject;
  static serializeBinaryToWriter(message: BulkDeployResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): BulkDeployResponse;
  static deserializeBinaryFromReader(message: BulkDeployResponse, reader: jspb.BinaryReader): BulkDeployResponse;
}

export namespace BulkDeployResponse {
  export type AsObject = {
    deploymentsList: Array<DeploymentProto.AsObject>;
  };
}

export class GetOverviewRequest extends jspb.Message {
  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GetOverviewRequest.AsObject;
  static toObject(includeInstance: boolean, msg: GetOverviewRequest): GetOverviewRequest.AsObject;
  static serializeBinaryToWriter(message: GetOverviewRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GetOverviewRequest;
  static deserializeBinaryFromReader(message: GetOverviewRequest, reader: jspb.BinaryReader): GetOverviewRequest;
}

export namespace GetOverviewRequest {
  export type AsObject = {
  };
}

export class OverviewProto extends jspb.Message {
  getTotalDevices(): number;
  setTotalDevices(value: number): OverviewProto;

  getOnlineDevices(): number;
  setOnlineDevices(value: number): OverviewProto;

  getTotalApps(): number;
  setTotalApps(value: number): OverviewProto;

  getTotalDeployments(): number;
  setTotalDeployments(value: number): OverviewProto;

  getRunningDeployments(): number;
  setRunningDeployments(value: number): OverviewProto;

  getFailedDeployments(): number;
  setFailedDeployments(value: number): OverviewProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): OverviewProto.AsObject;
  static toObject(includeInstance: boolean, msg: OverviewProto): OverviewProto.AsObject;
  static serializeBinaryToWriter(message: OverviewProto, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): OverviewProto;
  static deserializeBinaryFromReader(message: OverviewProto, reader: jspb.BinaryReader): OverviewProto;
}

export namespace OverviewProto {
  export type AsObject = {
    totalDevices: number;
    onlineDevices: number;
    totalApps: number;
    totalDeployments: number;
    runningDeployments: number;
    failedDeployments: number;
  };
}

