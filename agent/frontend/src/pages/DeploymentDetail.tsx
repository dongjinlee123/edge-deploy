import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import {
  Button, Descriptions, Popconfirm, Space, Spin, Table, Tabs, Tag, Typography, message,
} from 'antd'
import { ReloadOutlined, DeleteOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import {
  deleteDeployment,
  getDeployment,
  getDeploymentLogs,
  restartDeployment,
} from '@/api/deployments'
import { StatusBadge } from '@/components/StatusBadge'
import type { Deployment, DeploymentLog } from '@/types'

export function DeploymentDetail() {
  const { id } = useParams<{ id: string }>()
  const deploymentId = Number(id)
  const navigate = useNavigate()
  const [deployment, setDeployment] = useState<Deployment | null>(null)
  const [logs, setLogs] = useState<DeploymentLog[]>([])

  const load = () => {
    getDeployment(deploymentId).then(setDeployment)
    getDeploymentLogs(deploymentId).then(setLogs)
  }

  useEffect(() => { load() }, [deploymentId])

  const handleRestart = async () => {
    try {
      await restartDeployment(deploymentId)
      message.success('Rolling restart triggered')
      load()
    } catch (e: any) {
      message.error(`Restart failed: ${e?.message ?? e}`)
    }
  }

  const handleDelete = async () => {
    try {
      await deleteDeployment(deploymentId)
      message.success('Deployment deleted')
      navigate('/deployments')
    } catch (e: any) {
      message.error(`Delete failed: ${e?.message ?? e}`)
    }
  }

  if (!deployment) return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />

  const logColumns = [
    { title: 'Action', dataIndex: 'action' },
    {
      title: 'Status',
      dataIndex: 'status',
      render: (s: string) => <Tag color={s === 'success' ? 'green' : 'red'}>{s}</Tag>,
    },
    {
      title: 'Detail',
      dataIndex: 'detail',
      render: (v: unknown) => (
        <pre style={{ fontSize: 11, margin: 0, maxWidth: 400, overflow: 'auto' }}>
          {JSON.stringify(v, null, 2)}
        </pre>
      ),
    },
    { title: 'Time', dataIndex: 'created_at', render: (v: string) => new Date(v).toLocaleString() },
  ]

  const manifestTab = (
    <pre style={{ background: '#f5f5f5', padding: 12, borderRadius: 4, overflow: 'auto', fontSize: 12 }}>
      {deployment.manifests}
    </pre>
  )

  const auditTab = (
    <Table dataSource={logs} columns={logColumns} rowKey="id" size="small" />
  )

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Typography.Title level={3}>Deployment #{deployment.id}</Typography.Title>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={handleRestart}>Restart</Button>
          <Popconfirm title="Stop this deployment?" onConfirm={handleDelete}>
            <Button danger icon={<DeleteOutlined />}>Stop & Delete</Button>
          </Popconfirm>
        </Space>
      </div>

      <Descriptions bordered column={2} style={{ marginBottom: 24 }}>
        <Descriptions.Item label="Status"><StatusBadge status={deployment.status} /></Descriptions.Item>
        <Descriptions.Item label="Namespace">{deployment.namespace}</Descriptions.Item>
        <Descriptions.Item label="Device ID">{deployment.device_id}</Descriptions.Item>
        <Descriptions.Item label="App ID">{deployment.app_id ?? '—'}</Descriptions.Item>
        <Descriptions.Item label="Created">{new Date(deployment.created_at).toLocaleString()}</Descriptions.Item>
        {deployment.status_message && (
          <Descriptions.Item label="Message" span={2}>
            {deployment.status_message}
          </Descriptions.Item>
        )}
      </Descriptions>

      <Tabs
        items={[
          { key: 'manifests', label: 'Manifests', children: manifestTab },
          { key: 'audit', label: 'Audit Log', children: auditTab },
        ]}
      />
    </div>
  )
}
