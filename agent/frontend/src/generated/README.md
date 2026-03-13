# Generated gRPC-Web TypeScript stubs

This directory is populated by running:

```bash
# Requires: protoc + protoc-gen-grpc-web
cd proto && make proto-ts
```

Install the tools (macOS):
```bash
brew install protobuf
# Download protoc-gen-grpc-web from:
# https://github.com/grpc/grpc-web/releases
# and place it on your PATH
```

After generation this directory will contain:
```
edgedeploy/v1/
  common_pb.js / common_pb.d.ts
  edge_control_pb.js / edge_control_pb.d.ts
  DeviceManagementServiceClientPb.ts
  device_management_pb.js / device_management_pb.d.ts
  AppManagementServiceClientPb.ts
  app_management_pb.js / app_management_pb.d.ts
  DeploymentManagementServiceClientPb.ts
  deployment_management_pb.js / deployment_management_pb.d.ts
```
