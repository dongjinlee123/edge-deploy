import * as jspb from 'google-protobuf'

import * as google_protobuf_timestamp_pb from 'google-protobuf/google/protobuf/timestamp_pb'; // proto import: "google/protobuf/timestamp.proto"


export class AppProto extends jspb.Message {
  getId(): number;
  setId(value: number): AppProto;

  getName(): string;
  setName(value: string): AppProto;

  getImage(): string;
  setImage(value: string): AppProto;

  getDefaultTag(): string;
  setDefaultTag(value: string): AppProto;

  getDefaultReplicas(): number;
  setDefaultReplicas(value: number): AppProto;

  getDefaultPort(): number;
  setDefaultPort(value: number): AppProto;

  getDefaultEnvJson(): string;
  setDefaultEnvJson(value: string): AppProto;

  getYamlTemplate(): string;
  setYamlTemplate(value: string): AppProto;

  getCreatedAt(): google_protobuf_timestamp_pb.Timestamp | undefined;
  setCreatedAt(value?: google_protobuf_timestamp_pb.Timestamp): AppProto;
  hasCreatedAt(): boolean;
  clearCreatedAt(): AppProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): AppProto.AsObject;
  static toObject(includeInstance: boolean, msg: AppProto): AppProto.AsObject;
  static serializeBinaryToWriter(message: AppProto, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): AppProto;
  static deserializeBinaryFromReader(message: AppProto, reader: jspb.BinaryReader): AppProto;
}

export namespace AppProto {
  export type AsObject = {
    id: number;
    name: string;
    image: string;
    defaultTag: string;
    defaultReplicas: number;
    defaultPort: number;
    defaultEnvJson: string;
    yamlTemplate: string;
    createdAt?: google_protobuf_timestamp_pb.Timestamp.AsObject;
  };
}

export class ListAppsRequest extends jspb.Message {
  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ListAppsRequest.AsObject;
  static toObject(includeInstance: boolean, msg: ListAppsRequest): ListAppsRequest.AsObject;
  static serializeBinaryToWriter(message: ListAppsRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ListAppsRequest;
  static deserializeBinaryFromReader(message: ListAppsRequest, reader: jspb.BinaryReader): ListAppsRequest;
}

export namespace ListAppsRequest {
  export type AsObject = {
  };
}

export class ListAppsResponse extends jspb.Message {
  getAppsList(): Array<AppProto>;
  setAppsList(value: Array<AppProto>): ListAppsResponse;
  clearAppsList(): ListAppsResponse;
  addApps(value?: AppProto, index?: number): AppProto;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ListAppsResponse.AsObject;
  static toObject(includeInstance: boolean, msg: ListAppsResponse): ListAppsResponse.AsObject;
  static serializeBinaryToWriter(message: ListAppsResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ListAppsResponse;
  static deserializeBinaryFromReader(message: ListAppsResponse, reader: jspb.BinaryReader): ListAppsResponse;
}

export namespace ListAppsResponse {
  export type AsObject = {
    appsList: Array<AppProto.AsObject>;
  };
}

export class GetAppRequest extends jspb.Message {
  getId(): number;
  setId(value: number): GetAppRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): GetAppRequest.AsObject;
  static toObject(includeInstance: boolean, msg: GetAppRequest): GetAppRequest.AsObject;
  static serializeBinaryToWriter(message: GetAppRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): GetAppRequest;
  static deserializeBinaryFromReader(message: GetAppRequest, reader: jspb.BinaryReader): GetAppRequest;
}

export namespace GetAppRequest {
  export type AsObject = {
    id: number;
  };
}

export class CreateAppRequest extends jspb.Message {
  getName(): string;
  setName(value: string): CreateAppRequest;

  getImage(): string;
  setImage(value: string): CreateAppRequest;

  getDefaultTag(): string;
  setDefaultTag(value: string): CreateAppRequest;

  getDefaultReplicas(): number;
  setDefaultReplicas(value: number): CreateAppRequest;

  getDefaultPort(): number;
  setDefaultPort(value: number): CreateAppRequest;

  getDefaultEnvJson(): string;
  setDefaultEnvJson(value: string): CreateAppRequest;

  getYamlTemplate(): string;
  setYamlTemplate(value: string): CreateAppRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): CreateAppRequest.AsObject;
  static toObject(includeInstance: boolean, msg: CreateAppRequest): CreateAppRequest.AsObject;
  static serializeBinaryToWriter(message: CreateAppRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): CreateAppRequest;
  static deserializeBinaryFromReader(message: CreateAppRequest, reader: jspb.BinaryReader): CreateAppRequest;
}

export namespace CreateAppRequest {
  export type AsObject = {
    name: string;
    image: string;
    defaultTag: string;
    defaultReplicas: number;
    defaultPort: number;
    defaultEnvJson: string;
    yamlTemplate: string;
  };
}

export class UpdateAppRequest extends jspb.Message {
  getId(): number;
  setId(value: number): UpdateAppRequest;

  getName(): string;
  setName(value: string): UpdateAppRequest;

  getImage(): string;
  setImage(value: string): UpdateAppRequest;

  getDefaultTag(): string;
  setDefaultTag(value: string): UpdateAppRequest;

  getDefaultReplicas(): number;
  setDefaultReplicas(value: number): UpdateAppRequest;

  getDefaultPort(): number;
  setDefaultPort(value: number): UpdateAppRequest;

  getDefaultEnvJson(): string;
  setDefaultEnvJson(value: string): UpdateAppRequest;

  getYamlTemplate(): string;
  setYamlTemplate(value: string): UpdateAppRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): UpdateAppRequest.AsObject;
  static toObject(includeInstance: boolean, msg: UpdateAppRequest): UpdateAppRequest.AsObject;
  static serializeBinaryToWriter(message: UpdateAppRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): UpdateAppRequest;
  static deserializeBinaryFromReader(message: UpdateAppRequest, reader: jspb.BinaryReader): UpdateAppRequest;
}

export namespace UpdateAppRequest {
  export type AsObject = {
    id: number;
    name: string;
    image: string;
    defaultTag: string;
    defaultReplicas: number;
    defaultPort: number;
    defaultEnvJson: string;
    yamlTemplate: string;
  };
}

export class DeleteAppRequest extends jspb.Message {
  getId(): number;
  setId(value: number): DeleteAppRequest;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeleteAppRequest.AsObject;
  static toObject(includeInstance: boolean, msg: DeleteAppRequest): DeleteAppRequest.AsObject;
  static serializeBinaryToWriter(message: DeleteAppRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeleteAppRequest;
  static deserializeBinaryFromReader(message: DeleteAppRequest, reader: jspb.BinaryReader): DeleteAppRequest;
}

export namespace DeleteAppRequest {
  export type AsObject = {
    id: number;
  };
}

export class DeleteAppResponse extends jspb.Message {
  getOk(): boolean;
  setOk(value: boolean): DeleteAppResponse;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): DeleteAppResponse.AsObject;
  static toObject(includeInstance: boolean, msg: DeleteAppResponse): DeleteAppResponse.AsObject;
  static serializeBinaryToWriter(message: DeleteAppResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): DeleteAppResponse;
  static deserializeBinaryFromReader(message: DeleteAppResponse, reader: jspb.BinaryReader): DeleteAppResponse;
}

export namespace DeleteAppResponse {
  export type AsObject = {
    ok: boolean;
  };
}

