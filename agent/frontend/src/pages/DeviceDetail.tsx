import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Descriptions, Spin, Table, Tag, Typography } from 'antd'
import { getDevice } from '@/api/devices'
import { getDeployments } from '@/api/deployments'
import { StatusBadge } from '@/components/StatusBadge'
import type { Device, Deployment } from '@/types'

export function DeviceDetail() {
  const { id } = useParams<{ id: string }>()
  const deviceId = Number(id)
  const [device, setDevice] = useState<Device | null>(null)
  const [deployments, setDeployments] = useState<Deployment[]>([])

  useEffect(() => {
    getDevice(deviceId).then(setDevice)
    getDeployments({ device_id: deviceId }).then(setDeployments)
  }, [deviceId])

  if (!device) return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />

  const deployColumns = [
    { title: 'ID', dataIndex: 'id', render: (v: number) => <Link to={`/deployments/${v}`}>#{v}</Link> },
    { title: 'Namespace', dataIndex: 'namespace' },
    { title: 'Status', dataIndex: 'status', render: (s: string) => <StatusBadge status={s} /> },
    { title: 'Created', dataIndex: 'created_at', render: (v: string) => new Date(v).toLocaleString() },
  ]

  return (
    <div>
      <Typography.Title level={3}>Device: {device.name}</Typography.Title>
      <Descriptions bordered column={2} style={{ marginBottom: 24 }}>
        <Descriptions.Item label="Status"><StatusBadge status={device.status} /></Descriptions.Item>
        <Descriptions.Item label="Address">{device.address}:{device.agent_port}</Descriptions.Item>
        <Descriptions.Item label="Last Seen">{device.last_seen ? new Date(device.last_seen).toLocaleString() : '—'}</Descriptions.Item>
        <Descriptions.Item label="Created">{new Date(device.created_at).toLocaleString()}</Descriptions.Item>
        <Descriptions.Item label="Labels" span={2}>
          {device.labels && Object.keys(device.labels).length > 0
            ? Object.entries(device.labels).map(([k, v]) => (
                <Tag key={k}>{k}={v}</Tag>
              ))
            : '—'}
        </Descriptions.Item>
      </Descriptions>

      <Typography.Title level={4}>Deployments</Typography.Title>
      <Table dataSource={deployments} columns={deployColumns} rowKey="id" size="small" />
    </div>
  )
}
