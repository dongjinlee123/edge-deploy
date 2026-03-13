import { useEffect, useState } from 'react'
import { Button, Select, Space, Table, Typography, message } from 'antd'
import { PlusOutlined } from '@ant-design/icons'
import { Link } from 'react-router-dom'
import { getDeployments } from '@/api/deployments'
import { getDevices } from '@/api/devices'
import { StatusBadge } from '@/components/StatusBadge'
import type { Deployment, Device } from '@/types'

const STATUS_OPTIONS = [
  { value: '', label: 'All' },
  { value: 'running', label: 'Running' },
  { value: 'failed', label: 'Failed' },
  { value: 'deploying', label: 'Deploying' },
  { value: 'stopped', label: 'Stopped' },
  { value: 'pending', label: 'Pending' },
]

export function DeploymentList() {
  const [deployments, setDeployments] = useState<Deployment[]>([])
  const [devices, setDevices] = useState<Device[]>([])
  const [statusFilter, setStatusFilter] = useState('')

  const load = () => {
    getDeployments(statusFilter ? { status: statusFilter } : {})
      .then(setDeployments)
      .catch(() => message.error('Failed to load deployments'))
  }

  useEffect(() => {
    getDevices()
      .then(setDevices)
      .catch(() => message.error('Failed to load devices'))
  }, [])
  useEffect(() => { load() }, [statusFilter])

  const deviceMap = Object.fromEntries(devices.map(d => [d.id, d.name]))

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      render: (v: number) => <Link to={`/deployments/${v}`}>#{v}</Link>,
    },
    {
      title: 'Device',
      dataIndex: 'device_id',
      render: (id: number) => deviceMap[id] ?? id,
    },
    { title: 'Namespace', dataIndex: 'namespace' },
    {
      title: 'Status',
      dataIndex: 'status',
      render: (s: string) => <StatusBadge status={s} />,
    },
    {
      title: 'Message',
      dataIndex: 'status_message',
      render: (v: string | null) => <span style={{ fontSize: 12 }}>{v ?? '—'}</span>,
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      render: (v: string) => new Date(v).toLocaleString(),
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Typography.Title level={3}>Deployments</Typography.Title>
        <Space>
          <Select
            value={statusFilter}
            onChange={setStatusFilter}
            options={STATUS_OPTIONS}
            style={{ width: 120 }}
          />
          <Link to="/deployments/new">
            <Button type="primary" icon={<PlusOutlined />}>New Deployment</Button>
          </Link>
        </Space>
      </div>

      <Table dataSource={deployments} columns={columns} rowKey="id" />
    </div>
  )
}
