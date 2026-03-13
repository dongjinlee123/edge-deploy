/**
 * App API — backed by gRPC-Web (AppManagement service via Envoy).
 * Signatures match the old axios-based API.
 */
import { GRPC_HOST } from './grpc-client'
import type { App } from '@/types'

async function _clients() {
  const { AppManagementClient } = await import(
    '../generated/edgedeploy/v1/App_managementServiceClientPb'
  )
  const pb = await import('../generated/edgedeploy/v1/app_management_pb')
  return { AppManagementClient, pb }
}

function _toApp(proto: any): App {
  const cat = proto.getCreatedAt()
  let defaultEnv: Record<string, string> | null = null
  try {
    const raw = proto.getDefaultEnvJson()
    defaultEnv = raw ? JSON.parse(raw) : null
  } catch {}

  return {
    id: proto.getId(),
    name: proto.getName(),
    image: proto.getImage(),
    default_tag: proto.getDefaultTag(),
    default_replicas: proto.getDefaultReplicas(),
    default_port: proto.getDefaultPort() || null,
    default_env: defaultEnv,
    yaml_template: proto.getYamlTemplate() || null,
    created_at: cat ? new Date(cat.getSeconds() * 1000).toISOString() : '',
  }
}

export async function getApps(): Promise<App[]> {
  const { AppManagementClient, pb } = await _clients()
  const client = new AppManagementClient(GRPC_HOST)
  const resp = await client.listApps(new pb.ListAppsRequest(), {})
  return resp.getAppsList().map(_toApp)
}

export async function getApp(id: number): Promise<App> {
  const { AppManagementClient, pb } = await _clients()
  const client = new AppManagementClient(GRPC_HOST)
  const req = new pb.GetAppRequest()
  req.setId(id)
  return _toApp(await client.getApp(req, {}))
}

export async function createApp(data: Partial<App>): Promise<App> {
  const { AppManagementClient, pb } = await _clients()
  const client = new AppManagementClient(GRPC_HOST)
  const req = new pb.CreateAppRequest()
  req.setName(data.name ?? '')
  req.setImage(data.image ?? '')
  req.setDefaultTag(data.default_tag ?? 'latest')
  req.setDefaultReplicas(data.default_replicas ?? 1)
  if (data.default_port) req.setDefaultPort(data.default_port)
  if (data.default_env) req.setDefaultEnvJson(JSON.stringify(data.default_env))
  if (data.yaml_template) req.setYamlTemplate(data.yaml_template)
  return _toApp(await client.createApp(req, {}))
}

export async function updateApp(id: number, data: Partial<App>): Promise<App> {
  const { AppManagementClient, pb } = await _clients()
  const client = new AppManagementClient(GRPC_HOST)
  const req = new pb.UpdateAppRequest()
  req.setId(id)
  if (data.name !== undefined) req.setName(data.name)
  if (data.image !== undefined) req.setImage(data.image)
  if (data.default_tag !== undefined) req.setDefaultTag(data.default_tag)
  if (data.default_replicas !== undefined) req.setDefaultReplicas(data.default_replicas)
  if (data.default_port != null) req.setDefaultPort(data.default_port)
  if (data.default_env !== undefined) req.setDefaultEnvJson(JSON.stringify(data.default_env))
  if (data.yaml_template !== undefined) req.setYamlTemplate(data.yaml_template ?? '')
  return _toApp(await client.updateApp(req, {}))
}

export async function deleteApp(id: number): Promise<void> {
  const { AppManagementClient, pb } = await _clients()
  const client = new AppManagementClient(GRPC_HOST)
  const req = new pb.DeleteAppRequest()
  req.setId(id)
  await client.deleteApp(req, {})
}
