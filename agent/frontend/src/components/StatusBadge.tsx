import { Badge } from 'antd'

const statusMap: Record<string, 'success' | 'error' | 'warning' | 'processing' | 'default'> = {
  online: 'success',
  running: 'success',
  offline: 'error',
  failed: 'error',
  deploying: 'processing',
  pending: 'warning',
  stopped: 'default',
  unknown: 'default',
}

export function StatusBadge({ status }: { status: string }) {
  return <Badge status={statusMap[status] ?? 'default'} text={status} />
}
