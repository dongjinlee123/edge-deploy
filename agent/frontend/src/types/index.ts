export interface Device {
  id: number
  name: string
  address: string
  agent_port: number
  status: 'online' | 'offline' | 'unknown'
  last_seen: string | null
  labels: Record<string, string> | null
  created_at: string
}

export interface App {
  id: number
  name: string
  image: string
  default_tag: string
  default_replicas: number
  default_port: number | null
  default_env: Record<string, string> | null
  yaml_template: string | null
  created_at: string
}

export interface Deployment {
  id: number
  app_id: number | null
  device_id: number
  namespace: string
  manifests: string
  status: 'pending' | 'deploying' | 'running' | 'failed' | 'stopped'
  status_message: string | null
  created_at: string
}

export interface DeploymentLog {
  id: number
  deployment_id: number
  action: string
  detail: Record<string, unknown> | null
  status: 'success' | 'failure'
  created_at: string
}

export interface Overview {
  devices: { total: number; online: number; offline: number }
  apps: { total: number }
  deployments: { total: number; running: number; failed: number }
}
