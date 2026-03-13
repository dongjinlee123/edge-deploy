/**
 * Device API — backed by gRPC-Web (DeviceManagement service via Envoy).
 *
 * Function signatures are identical to the old axios-based API so all
 * existing pages continue to work without changes.
 *
 * Prerequisites: run `cd proto && make proto-ts` to populate src/generated/.
 */
import { GRPC_HOST } from './grpc-client'
import type { Device } from '@/types'

// ---- lazy-load generated stubs (populated by `make proto-ts`) ----
// Using dynamic imports so the app still bundles even before stubs exist;
// swap the `false` branch for real imports once stubs are generated.
async function _clients() {
  const { DeviceManagementClient } = await import(
    '../generated/edgedeploy/v1/Device_managementServiceClientPb'
  )
  const pb = await import('../generated/edgedeploy/v1/device_management_pb')
  const commonPb = await import('../generated/edgedeploy/v1/common_pb')
  return { DeviceManagementClient, pb, commonPb }
}

function _toDevice(proto: any): Device {
  const ts = proto.getLastSeen()
  const cat = proto.getCreatedAt()
  return {
    id: proto.getId(),
    name: proto.getName(),
    address: proto.getAddress(),
    agent_port: proto.getAgentPort(),
    status: proto.getStatus() as Device['status'],
    last_seen: ts ? new Date(ts.getSeconds() * 1000).toISOString() : null,
    labels: proto.getLabels()
      ? Object.fromEntries(proto.getLabels().getValuesMap().toObject())
      : null,
    created_at: cat ? new Date(cat.getSeconds() * 1000).toISOString() : '',
  }
}

export async function getDevices(): Promise<Device[]> {
  const { DeviceManagementClient, pb } = await _clients()
  const client = new DeviceManagementClient(GRPC_HOST)
  const req = new pb.ListDevicesRequest()
  const resp = await client.listDevices(req, {})
  return resp.getDevicesList().map(_toDevice)
}

export async function getDevice(id: number): Promise<Device> {
  const { DeviceManagementClient, pb } = await _clients()
  const client = new DeviceManagementClient(GRPC_HOST)
  const req = new pb.GetDeviceRequest()
  req.setId(id)
  const resp = await client.getDevice(req, {})
  return _toDevice(resp)
}

export async function createDevice(data: Partial<Device>): Promise<Device> {
  const { DeviceManagementClient, pb, commonPb } = await _clients()
  const client = new DeviceManagementClient(GRPC_HOST)
  const req = new pb.CreateDeviceRequest()
  req.setName(data.name ?? '')
  req.setAddress(data.address ?? '')
  req.setAgentPort(data.agent_port ?? 30080)
  if (data.labels) {
    const labels = new commonPb.Labels()
    Object.entries(data.labels).forEach(([k, v]) => labels.getValuesMap().set(k, v))
    req.setLabels(labels)
  }
  const resp = await client.createDevice(req, {})
  return _toDevice(resp)
}

export async function updateDevice(id: number, data: Partial<Device>): Promise<Device> {
  const { DeviceManagementClient, pb, commonPb } = await _clients()
  const client = new DeviceManagementClient(GRPC_HOST)
  const req = new pb.UpdateDeviceRequest()
  req.setId(id)
  if (data.name !== undefined) req.setName(data.name)
  if (data.address !== undefined) req.setAddress(data.address)
  if (data.agent_port !== undefined) req.setAgentPort(data.agent_port)
  if (data.labels) {
    const labels = new commonPb.Labels()
    Object.entries(data.labels).forEach(([k, v]) => labels.getValuesMap().set(k, v))
    req.setLabels(labels)
  }
  const resp = await client.updateDevice(req, {})
  return _toDevice(resp)
}

export async function deleteDevice(id: number): Promise<void> {
  const { DeviceManagementClient, pb } = await _clients()
  const client = new DeviceManagementClient(GRPC_HOST)
  const req = new pb.DeleteDeviceRequest()
  req.setId(id)
  await client.deleteDevice(req, {})
}

