/**
 * google-protobuf 3.21.4 is missing BinaryReader.prototype.readStringRequireUtf8
 * which was added in a later protoc-gen-js release.  Alias it to readString so
 * the generated pb files work without regeneration.
 *
 * After Vite's CJS→ESM transform, google-protobuf's module.exports becomes
 * the default export, so we must use a default import (not namespace import).
 */
import googleProtobuf from 'google-protobuf'

const proto = googleProtobuf.BinaryReader.prototype as any
if (!proto.readStringRequireUtf8) {
  proto.readStringRequireUtf8 = googleProtobuf.BinaryReader.prototype.readString
}
