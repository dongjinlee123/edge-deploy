import * as jspb from 'google-protobuf'

import * as google_protobuf_timestamp_pb from 'google-protobuf/google/protobuf/timestamp_pb'; // proto import: "google/protobuf/timestamp.proto"
import * as edgedeploy_v1_common_pb from '../../edgedeploy/v1/common_pb'; // proto import: "edgedeploy/v1/common.proto"


export class RegisterRequest extends jspb.Message {
  getProvisioningToken(): string;
  setProvisioningToken(value: string): RegisterRequest;

  getDeviceName(): string;
  setDeviceName(value: string): RegisterRequest;

  getCsrPem(): string;
  setCsrPem(value: string): RegisterRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): RegisterRequest.AsObject;
  static toObject(includeInstance: boolean, msg: RegisterRequest): RegisterRequest.AsObject;
  static serializeBinaryToWriter(message: RegisterRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): RegisterRequest;
  static deserializeBinaryFromReader(message: RegisterRequest, reader: jspb.BinaryReader): RegisterRequest;
}

export namespace RegisterRequest {
  export type AsObject = {
    provisioningToken: string;
    deviceName: string;
    csrPem: string;
  };
}

export class RegisterResponse extends jspb.Message {
  getDeviceUuid(): string;
  setDeviceUuid(value: string): RegisterResponse;

  getCertPem(): string;
  setCertPem(value: string): RegisterResponse;

  getCaCertPem(): string;
  setCaCertPem(value: string): RegisterResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): RegisterResponse.AsObject;
  static toObject(includeInstance: boolean, msg: RegisterResponse): RegisterResponse.AsObject;
  static serializeBinaryToWriter(message: RegisterResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): RegisterResponse;
  static deserializeBinaryFromReader(message: RegisterResponse, reader: jspb.BinaryReader): RegisterResponse;
}

export namespace RegisterResponse {
  export type AsObject = {
    deviceUuid: string;
    certPem: string;
    caCertPem: string;
  };
}

export class EdgeReport extends jspb.Message {
  getDeviceUuid(): string;
  setDeviceUuid(value: string): EdgeReport;

  getHeartbeat(): Heartbeat | undefined;
  setHeartbeat(value?: Heartbeat): EdgeReport;
  hasHeartbeat(): boolean;
  clearHeartbeat(): EdgeReport;

  getStatusReport(): StatusReport | undefined;
  setStatusReport(value?: StatusReport): EdgeReport;
  hasStatusReport(): boolean;
  clearStatusReport(): EdgeReport;

  getCommandAck(): CommandAck | undefined;
  setCommandAck(value?: CommandAck): EdgeReport;
  hasCommandAck(): boolean;
  clearCommandAck(): EdgeReport;

  getResourceSnapshot(): ResourceSnapshot | undefined;
  setResourceSnapshot(value?: ResourceSnapshot): EdgeReport;
  hasResourceSnapshot(): boolean;
  clearResourceSnapshot(): EdgeReport;

  getLogChunk(): LogChunk | undefined;
  setLogChunk(value?: LogChunk): EdgeReport;
  hasLogChunk(): boolean;
  clearLogChunk(): EdgeReport;

  getPayloadCase(): EdgeReport.PayloadCase;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): EdgeReport.AsObject;
  static toObject(includeInstance: boolean, msg: EdgeReport): EdgeReport.AsObject;
  static serializeBinaryToWriter(message: EdgeReport, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): EdgeReport;
  static deserializeBinaryFromReader(message: EdgeReport, reader: jspb.BinaryReader): EdgeReport;
}

export namespace EdgeReport {
  export type AsObject = {
    deviceUuid: string;
    heartbeat?: Heartbeat.AsObject;
    statusReport?: StatusReport.AsObject;
    commandAck?: CommandAck.AsObject;
    resourceSnapshot?: ResourceSnapshot.AsObject;
    logChunk?: LogChunk.AsObject;
  };

  export enum PayloadCase {
    PAYLOAD_NOT_SET = 0,
    HEARTBEAT = 2,
    STATUS_REPORT = 3,
    COMMAND_ACK = 4,
    RESOURCE_SNAPSHOT = 5,
    LOG_CHUNK = 6,
  }
}

export class Heartbeat extends jspb.Message {
  getTs(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setTs(value?: google_protobuf_timestamp_pb.Timestamp): Heartbeat;
  hasTs(): boolean;
  clearTs(): Heartbeat;

  getAgentVersion(): string;
  setAgentVersion(value: string): Heartbeat;

  getConfigVersion(): number;
  setConfigVersion(value: number): Heartbeat;

  getCpuUsagePercent(): number;
  setCpuUsagePercent(value: number): Heartbeat;

  getMemoryUsagePercent(): number;
  setMemoryUsagePercent(value: number): Heartbeat;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Heartbeat.AsObject;
  static toObject(includeInstance: boolean, msg: Heartbeat): Heartbeat.AsObject;
  static serializeBinaryToWriter(message: Heartbeat, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Heartbeat;
  static deserializeBinaryFromReader(message: Heartbeat, reader: jspb.BinaryReader): Heartbeat;
}

export namespace Heartbeat {
  export type AsObject = {
    ts?: google_protobuf_timestamp_pb.Timestamp.AsObject;
    agentVersion: string;
    configVersion: number;
    cpuUsagePercent: number;
    memoryUsagePercent: number;
  };
}

export class StatusReport extends jspb.Message {
  getDeviceUuid(): string;
  setDeviceUuid(value: string): StatusReport;

  getStatus(): string;
  setStatus(value: string): StatusReport;

  getMessage(): string;
  setMessage(value: string): StatusReport;

  getTs(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setTs(value?: google_protobuf_timestamp_pb.Timestamp): StatusReport;
  hasTs(): boolean;
  clearTs(): StatusReport;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): StatusReport.AsObject;
  static toObject(includeInstance: boolean, msg: StatusReport): StatusReport.AsObject;
  static serializeBinaryToWriter(message: StatusReport, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): StatusReport;
  static deserializeBinaryFromReader(message: StatusReport, reader: jspb.BinaryReader): StatusReport;
}

export namespace StatusReport {
  export type AsObject = {
    deviceUuid: string;
    status: string;
    message: string;
    ts?: google_protobuf_timestamp_pb.Timestamp.AsObject;
  };
}

export class CommandAck extends jspb.Message {
  getCommandId(): string;
  setCommandId(value: string): CommandAck;

  getSuccess(): boolean;
  setSuccess(value: boolean): CommandAck;

  getMessage(): string;
  setMessage(value: string): CommandAck;

  getResultJson(): string;
  setResultJson(value: string): CommandAck;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CommandAck.AsObject;
  static toObject(includeInstance: boolean, msg: CommandAck): CommandAck.AsObject;
  static serializeBinaryToWriter(message: CommandAck, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CommandAck;
  static deserializeBinaryFromReader(message: CommandAck, reader: jspb.BinaryReader): CommandAck;
}

export namespace CommandAck {
  export type AsObject = {
    commandId: string;
    success: boolean;
    message: string;
    resultJson: string;
  };
}

export class ResourceSnapshot extends jspb.Message {
  getCommandId(): string;
  setCommandId(value: string): ResourceSnapshot;

  getNamespace(): string;
  setNamespace(value: string): ResourceSnapshot;

  getResourcesJson(): string;
  setResourcesJson(value: string): ResourceSnapshot;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ResourceSnapshot.AsObject;
  static toObject(includeInstance: boolean, msg: ResourceSnapshot): ResourceSnapshot.AsObject;
  static serializeBinaryToWriter(message: ResourceSnapshot, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ResourceSnapshot;
  static deserializeBinaryFromReader(message: ResourceSnapshot, reader: jspb.BinaryReader): ResourceSnapshot;
}

export namespace ResourceSnapshot {
  export type AsObject = {
    commandId: string;
    namespace: string;
    resourcesJson: string;
  };
}

export class LogChunk extends jspb.Message {
  getCommandId(): string;
  setCommandId(value: string): LogChunk;

  getPodName(): string;
  setPodName(value: string): LogChunk;

  getNamespace(): string;
  setNamespace(value: string): LogChunk;

  getData(): Uint8Array | string;
  getData_asU8(): Uint8Array;
  getData_asB64(): string;
  setData(value: Uint8Array | string): LogChunk;

  getEof(): boolean;
  setEof(value: boolean): LogChunk;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): LogChunk.AsObject;
  static toObject(includeInstance: boolean, msg: LogChunk): LogChunk.AsObject;
  static serializeBinaryToWriter(message: LogChunk, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): LogChunk;
  static deserializeBinaryFromReader(message: LogChunk, reader: jspb.BinaryReader): LogChunk;
}

export namespace LogChunk {
  export type AsObject = {
    commandId: string;
    podName: string;
    namespace: string;
    data: Uint8Array | string;
    eof: boolean;
  };
}

export class EdgeCommand extends jspb.Message {
  getCommandId(): string;
  setCommandId(value: string): EdgeCommand;

  getApplyManifests(): ApplyManifestsCommand | undefined;
  setApplyManifests(value?: ApplyManifestsCommand): EdgeCommand;
  hasApplyManifests(): boolean;
  clearApplyManifests(): EdgeCommand;

  getDeleteResource(): DeleteResourceCommand | undefined;
  setDeleteResource(value?: DeleteResourceCommand): EdgeCommand;
  hasDeleteResource(): boolean;
  clearDeleteResource(): EdgeCommand;

  getRestartDeployment(): RestartDeploymentCommand | undefined;
  setRestartDeployment(value?: RestartDeploymentCommand): EdgeCommand;
  hasRestartDeployment(): boolean;
  clearRestartDeployment(): EdgeCommand;

  getGetResources(): GetResourcesCommand | undefined;
  setGetResources(value?: GetResourcesCommand): EdgeCommand;
  hasGetResources(): boolean;
  clearGetResources(): EdgeCommand;

  getGetPodLogs(): GetPodLogsCommand | undefined;
  setGetPodLogs(value?: GetPodLogsCommand): EdgeCommand;
  hasGetPodLogs(): boolean;
  clearGetPodLogs(): EdgeCommand;

  getConfigSync(): ConfigSyncCommand | undefined;
  setConfigSync(value?: ConfigSyncCommand): EdgeCommand;
  hasConfigSync(): boolean;
  clearConfigSync(): EdgeCommand;

  getPayloadCase(): EdgeCommand.PayloadCase;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): EdgeCommand.AsObject;
  static toObject(includeInstance: boolean, msg: EdgeCommand): EdgeCommand.AsObject;
  static serializeBinaryToWriter(message: EdgeCommand, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): EdgeCommand;
  static deserializeBinaryFromReader(message: EdgeCommand, reader: jspb.BinaryReader): EdgeCommand;
}

export namespace EdgeCommand {
  export type AsObject = {
    commandId: string;
    applyManifests?: ApplyManifestsCommand.AsObject;
    deleteResource?: DeleteResourceCommand.AsObject;
    restartDeployment?: RestartDeploymentCommand.AsObject;
    getResources?: GetResourcesCommand.AsObject;
    getPodLogs?: GetPodLogsCommand.AsObject;
    configSync?: ConfigSyncCommand.AsObject;
  };

  export enum PayloadCase {
    PAYLOAD_NOT_SET = 0,
    APPLY_MANIFESTS = 2,
    DELETE_RESOURCE = 3,
    RESTART_DEPLOYMENT = 4,
    GET_RESOURCES = 5,
    GET_POD_LOGS = 6,
    CONFIG_SYNC = 7,
  }
}

export class ApplyManifestsCommand extends jspb.Message {
  getManifests(): string;
  setManifests(value: string): ApplyManifestsCommand;

  getNamespace(): string;
  setNamespace(value: string): ApplyManifestsCommand;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ApplyManifestsCommand.AsObject;
  static toObject(includeInstance: boolean, msg: ApplyManifestsCommand): ApplyManifestsCommand.AsObject;
  static serializeBinaryToWriter(message: ApplyManifestsCommand, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ApplyManifestsCommand;
  static deserializeBinaryFromReader(message: ApplyManifestsCommand, reader: jspb.BinaryReader): ApplyManifestsCommand;
}

export namespace ApplyManifestsCommand {
  export type AsObject = {
    manifests: string;
    namespace: string;
  };
}

export class DeleteResourceCommand extends jspb.Message {
  getNamespace(): string;
  setNamespace(value: string): DeleteResourceCommand;

  getKind(): string;
  setKind(value: string): DeleteResourceCommand;

  getName(): string;
  setName(value: string): DeleteResourceCommand;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeleteResourceCommand.AsObject;
  static toObject(includeInstance: boolean, msg: DeleteResourceCommand): DeleteResourceCommand.AsObject;
  static serializeBinaryToWriter(message: DeleteResourceCommand, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeleteResourceCommand;
  static deserializeBinaryFromReader(message: DeleteResourceCommand, reader: jspb.BinaryReader): DeleteResourceCommand;
}

export namespace DeleteResourceCommand {
  export type AsObject = {
    namespace: string;
    kind: string;
    name: string;
  };
}

export class RestartDeploymentCommand extends jspb.Message {
  getNamespace(): string;
  setNamespace(value: string): RestartDeploymentCommand;

  getName(): string;
  setName(value: string): RestartDeploymentCommand;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): RestartDeploymentCommand.AsObject;
  static toObject(includeInstance: boolean, msg: RestartDeploymentCommand): RestartDeploymentCommand.AsObject;
  static serializeBinaryToWriter(message: RestartDeploymentCommand, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): RestartDeploymentCommand;
  static deserializeBinaryFromReader(message: RestartDeploymentCommand, reader: jspb.BinaryReader): RestartDeploymentCommand;
}

export namespace RestartDeploymentCommand {
  export type AsObject = {
    namespace: string;
    name: string;
  };
}

export class GetResourcesCommand extends jspb.Message {
  getNamespace(): string;
  setNamespace(value: string): GetResourcesCommand;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GetResourcesCommand.AsObject;
  static toObject(includeInstance: boolean, msg: GetResourcesCommand): GetResourcesCommand.AsObject;
  static serializeBinaryToWriter(message: GetResourcesCommand, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GetResourcesCommand;
  static deserializeBinaryFromReader(message: GetResourcesCommand, reader: jspb.BinaryReader): GetResourcesCommand;
}

export namespace GetResourcesCommand {
  export type AsObject = {
    namespace: string;
  };
}

export class GetPodLogsCommand extends jspb.Message {
  getNamespace(): string;
  setNamespace(value: string): GetPodLogsCommand;

  getPodName(): string;
  setPodName(value: string): GetPodLogsCommand;

  getTail(): number;
  setTail(value: number): GetPodLogsCommand;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GetPodLogsCommand.AsObject;
  static toObject(includeInstance: boolean, msg: GetPodLogsCommand): GetPodLogsCommand.AsObject;
  static serializeBinaryToWriter(message: GetPodLogsCommand, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GetPodLogsCommand;
  static deserializeBinaryFromReader(message: GetPodLogsCommand, reader: jspb.BinaryReader): GetPodLogsCommand;
}

export namespace GetPodLogsCommand {
  export type AsObject = {
    namespace: string;
    podName: string;
    tail: number;
  };
}

export class ConfigSyncCommand extends jspb.Message {
  getDesiredConfigJson(): string;
  setDesiredConfigJson(value: string): ConfigSyncCommand;

  getConfigVersion(): number;
  setConfigVersion(value: number): ConfigSyncCommand;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ConfigSyncCommand.AsObject;
  static toObject(includeInstance: boolean, msg: ConfigSyncCommand): ConfigSyncCommand.AsObject;
  static serializeBinaryToWriter(message: ConfigSyncCommand, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ConfigSyncCommand;
  static deserializeBinaryFromReader(message: ConfigSyncCommand, reader: jspb.BinaryReader): ConfigSyncCommand;
}

export namespace ConfigSyncCommand {
  export type AsObject = {
    desiredConfigJson: string;
    configVersion: number;
  };
}

