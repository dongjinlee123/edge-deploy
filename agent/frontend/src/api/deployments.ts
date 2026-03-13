/**
 * Deployment API — backed by gRPC-Web (DeploymentManagement service via Envoy).
 * Signatures match the old axios-based API.
 */
import { GRPC_HOST } from './grpc-client'
import type { Deployment, DeploymentLog, Overview } from '@/types'

async function _clients() {
  const { DeploymentManagementClient } = await import(
    '../generated/edgedeploy/v1/Deployment_managementServiceClientPb'
  )
  const pb = await import('../generated/edgedeploy/v1/deployment_management_pb')
  return { DeploymentManagementClient, pb }
}

function _toDeployment(proto: any): Deployment {
  const cat = proto.getCreatedAt()
  return {
    id: proto.getId(),
    app_id: proto.getAppId() || null,
    device_id: proto.getDeviceId(),
    namespace: proto.getNamespace(),
    manifests: proto.getManifests(),
    status: proto.getStatus() as Deployment['status'],
    status_message: proto.getStatusMessage() || null,
    created_at: cat ? new Date(cat.getSeconds() * 1000).toISOString() : '',
  }
}

function _toLog(proto: any): DeploymentLog {
  const cat = proto.getCreatedAt()
  let detail: Record<string, unknown> | null = null
  try {
    const raw = proto.getDetailJson()
    detail = raw ? JSON.parse(raw) : null
  } catch {}
  return {
    id: proto.getId(),
    deployment_id: proto.getDeploymentId(),
    action: proto.getAction(),
    detail,
    status: proto.getStatus() as DeploymentLog['status'],
    created_at: cat ? new Date(cat.getSeconds() * 1000).toISOString() : '',
  }
}

export async function getDeployments(params?: {
  device_id?: number
  app_id?: number
  status?: string
}): Promise<Deployment[]> {
  const { DeploymentManagementClient, pb } = await _clients()
  const client = new DeploymentManagementClient(GRPC_HOST)
  const req = new pb.ListDeploymentsRequest()
  if (params?.device_id != null) req.setDeviceId(params.device_id)
  if (params?.app_id != null) req.setAppId(params.app_id)
  if (params?.status) req.setStatus(params.status)
  const resp = await client.listDeployments(req, {})
  return resp.getDeploymentsList().map(_toDeployment)
}

export async function getDeployment(id: number): Promise<Deployment> {
  const { DeploymentManagementClient, pb } = await _clients()
  const client = new DeploymentManagementClient(GRPC_HOST)
  const req = new pb.GetDeploymentRequest()
  req.setId(id)
  return _toDeployment(await client.getDeployment(req, {}))
}

export async function createFormDeployment(data: {
  app_id: number
  device_id: number
  namespace?: string
  tag?: string
  replicas?: number
  port?: number
  env?: Record<string, string>
}): Promise<Deployment> {
  const { DeploymentManagementClient, pb } = await _clients()
  const client = new DeploymentManagementClient(GRPC_HOST)
  const req = new pb.CreateFormDeploymentRequest()
  req.setAppId(data.app_id)
  req.setDeviceId(data.device_id)
  req.setNamespace(data.namespace ?? 'default')
  if (data.tag) req.setTag(data.tag)
  if (data.replicas) req.setReplicas(data.replicas)
  return _toDeployment(await client.createFormDeployment(req, {}))
}

export async function createYAMLDeployment(data: {
  device_id: number
  namespace?: string
  manifests: string
  app_id?: number
}): Promise<Deployment> {
  const { DeploymentManagementClient, pb } = await _clients()
  const client = new DeploymentManagementClient(GRPC_HOST)
  const req = new pb.CreateYamlDeploymentRequest()
  req.setDeviceId(data.device_id)
  req.setNamespace(data.namespace ?? 'default')
  req.setManifests(data.manifests)
  return _toDeployment(await client.createYamlDeployment(req, {}))
}

export async function deleteDeployment(id: number): Promise<void> {
  const { DeploymentManagementClient, pb } = await _clients()
  const client = new DeploymentManagementClient(GRPC_HOST)
  const req = new pb.DeleteDeploymentRequest()
  req.setId(id)
  await client.deleteDeployment(req, {})
}

export async function restartDeployment(id: number): Promise<Deployment> {
  const { DeploymentManagementClient, pb } = await _clients()
  const client = new DeploymentManagementClient(GRPC_HOST)
  const req = new pb.RestartDeploymentRequest()
  req.setId(id)
  await client.restartDeployment(req, {})
  return getDeployment(id)
}

export async function getDeploymentLogs(id: number): Promise<DeploymentLog[]> {
  const { DeploymentManagementClient, pb } = await _clients()
  const client = new DeploymentManagementClient(GRPC_HOST)
  const req = new pb.GetDeploymentLogsRequest()
  req.setId(id)
  const resp = await client.getDeploymentLogs(req, {})
  return resp.getLogsList().map(_toLog)
}

export async function bulkDeploy(data: {
  app_id: number
  device_ids: number[]
  namespace?: string
  tag?: string
  replicas?: number
}): Promise<Deployment[]> {
  const { DeploymentManagementClient, pb } = await _clients()
  const client = new DeploymentManagementClient(GRPC_HOST)
  const req = new pb.BulkDeployRequest()
  req.setAppId(data.app_id)
  req.setDeviceIdsList(data.device_ids)
  req.setNamespace(data.namespace ?? 'default')
  if (data.tag) req.setTag(data.tag)
  if (data.replicas) req.setReplicas(data.replicas)
  const resp = await client.bulkDeploy(req, {})
  return resp.getDeploymentsList().map(_toDeployment)
}

export async function getOverview(): Promise<Overview> {
  const { DeploymentManagementClient, pb } = await _clients()
  const client = new DeploymentManagementClient(GRPC_HOST)
  const resp = await client.getOverview(new pb.GetOverviewRequest(), {})
  return {
    devices: {
      total: resp.getTotalDevices(),
      online: resp.getOnlineDevices(),
      offline: resp.getTotalDevices() - resp.getOnlineDevices(),
    },
    apps: { total: resp.getTotalApps() },
    deployments: {
      total: resp.getTotalDeployments(),
      running: resp.getRunningDeployments(),
      failed: resp.getFailedDeployments(),
    },
  }
}
