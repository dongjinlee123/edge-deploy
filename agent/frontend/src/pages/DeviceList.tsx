import { useEffect, useState } from 'react'
import { Button, Form, Input, InputNumber, Modal, Popconfirm, Select, Space, Table, Tag, Typography, message } from 'antd'
import { PlusOutlined, SearchOutlined } from '@ant-design/icons'
import { Link } from 'react-router-dom'
import { createDevice, deleteDevice, getDevices } from '@/api/devices'
import { StatusBadge } from '@/components/StatusBadge'
import type { Device } from '@/types'

const STATUS_OPTIONS = [
  { value: '', label: 'All Status' },
  { value: 'online', label: 'Online' },
  { value: 'offline', label: 'Offline' },
  { value: 'unknown', label: 'Unknown' },
]

export function DeviceList() {
  const [devices, setDevices] = useState<Device[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [searchText, setSearchText] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [form] = Form.useForm()

  const load = () => {
    setLoading(true)
    getDevices()
      .then(setDevices)
      .catch(() => message.error('Failed to load devices'))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const handleCreate = async (values: Partial<Device>) => {
    try {
      await createDevice(values)
      message.success('Device registered')
      setModalOpen(false)
      form.resetFields()
      load()
    } catch (e: any) {
      message.error(`Failed to register device: ${e?.message ?? e}`)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await deleteDevice(id)
      message.success('Device removed')
      load()
    } catch (e: any) {
      message.error(`Failed to remove device: ${e?.message ?? e}`)
    }
  }

  const filteredDevices = devices.filter(d => {
    const matchesSearch = !searchText || d.name.toLowerCase().includes(searchText.toLowerCase())
    const matchesStatus = !statusFilter || d.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const columns = [
    {
      title: 'Status',
      dataIndex: 'status',
      render: (s: string) => <StatusBadge status={s} />,
    },
    {
      title: 'Name',
      dataIndex: 'name',
      render: (name: string, record: Device) => <Link to={`/devices/${record.id}`}>{name}</Link>,
    },
    { title: 'Address', dataIndex: 'address' },
    { title: 'Port', dataIndex: 'agent_port' },
    {
      title: 'Labels',
      dataIndex: 'labels',
      render: (labels: Record<string, string> | null) =>
        labels ? Object.entries(labels).map(([k, v]) => (
          <Tag key={k}>{k}={v}</Tag>
        )) : '—',
    },
    {
      title: 'Last Seen',
      dataIndex: 'last_seen',
      render: (v: string | null) => v ? new Date(v).toLocaleString() : '—',
    },
    {
      title: 'Actions',
      render: (_: unknown, record: Device) => (
        <Space>
          <Popconfirm title="Remove this device?" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger>Remove</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Typography.Title level={3}>Devices</Typography.Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalOpen(true)}>Register Device</Button>
      </div>

      <Space style={{ marginBottom: 16 }}>
        <Input.Search
          placeholder="Search by name"
          prefix={<SearchOutlined />}
          allowClear
          onChange={e => setSearchText(e.target.value)}
          style={{ width: 250 }}
        />
        <Select
          value={statusFilter}
          onChange={setStatusFilter}
          options={STATUS_OPTIONS}
          style={{ width: 140 }}
        />
      </Space>

      <Table dataSource={filteredDevices} columns={columns} rowKey="id" loading={loading} />

      <Modal
        title="Register Device"
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="name" label="Name" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="address" label="IP / Hostname" rules={[{ required: true }]}>
            <Input placeholder="192.168.1.100" />
          </Form.Item>
          <Form.Item name="agent_port" label="Agent Port" initialValue={30080}>
            <InputNumber min={1} max={65535} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}
