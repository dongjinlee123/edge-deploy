import * as jspb from 'google-protobuf'

import * as google_protobuf_timestamp_pb from 'google-protobuf/google/protobuf/timestamp_pb'; // proto import: "google/protobuf/timestamp.proto"


export class Labels extends jspb.Message {
  getValuesMap(): jspb.Map<string, string>;
  clearValuesMap(): Labels;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): Labels.AsObject;
  static toObject(includeInstance: boolean, msg: Labels): Labels.AsObject;
  static serializeBinaryToWriter(message: Labels, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): Labels;
  static deserializeBinaryFromReader(message: Labels, reader: jspb.BinaryReader): Labels;
}

export namespace Labels {
  export type AsObject = {
    valuesMap: Array<[string, string]>;
  };
}

export class ResourceRef extends jspb.Message {
  getNamespace(): string;
  setNamespace(value: string): ResourceRef;

  getKind(): string;
  setKind(value: string): ResourceRef;

  getName(): string;
  setName(value: string): ResourceRef;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): ResourceRef.AsObject;
  static toObject(includeInstance: boolean, msg: ResourceRef): ResourceRef.AsObject;
  static serializeBinaryToWriter(message: ResourceRef, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): ResourceRef;
  static deserializeBinaryFromReader(message: ResourceRef, reader: jspb.BinaryReader): ResourceRef;
}

export namespace ResourceRef {
  export type AsObject = {
    namespace: string;
    kind: string;
    name: string;
  };
}

