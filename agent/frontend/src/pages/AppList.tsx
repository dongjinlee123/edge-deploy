import { useEffect, useState } from 'react'
import { Button, Form, Input, InputNumber, Modal, Popconfirm, Space, Table, Typography, message } from 'antd'
import { PlusOutlined, SearchOutlined } from '@ant-design/icons'
import { Link } from 'react-router-dom'
import { createApp, deleteApp, getApps } from '@/api/apps'
import type { App } from '@/types'

export function AppList() {
  const [apps, setApps] = useState<App[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [searchText, setSearchText] = useState('')
  const [form] = Form.useForm()

  const load = () => {
    setLoading(true)
    getApps()
      .then(setApps)
      .catch(() => message.error('Failed to load apps'))
      .finally(() => setLoading(false))
  }
  useEffect(() => { load() }, [])

  const handleCreate = async (values: Partial<App>) => {
    await createApp(values)
    message.success('App created')
    setModalOpen(false)
    form.resetFields()
    load()
  }

  const handleDelete = async (id: number) => {
    await deleteApp(id)
    message.success('App deleted')
    load()
  }

  const filteredApps = apps.filter(a =>
    !searchText || a.name.toLowerCase().includes(searchText.toLowerCase())
  )

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      render: (name: string, record: App) => <Link to={`/apps/${record.id}`}>{name}</Link>,
    },
    { title: 'Image', dataIndex: 'image' },
    { title: 'Default Tag', dataIndex: 'default_tag' },
    { title: 'Replicas', dataIndex: 'default_replicas' },
    { title: 'Port', dataIndex: 'default_port', render: (v: number | null) => v ?? '—' },
    {
      title: 'Created',
      dataIndex: 'created_at',
      render: (v: string) => new Date(v).toLocaleString(),
    },
    {
      title: 'Actions',
      render: (_: unknown, record: App) => (
        <Space>
          <Link to={`/deployments/new?app_id=${record.id}`}><Button size="small" type="primary">Deploy</Button></Link>
          <Popconfirm title="Delete this app?" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger>Delete</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Typography.Title level={3}>Apps</Typography.Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalOpen(true)}>New App</Button>
      </div>

      <Input.Search
        placeholder="Search by name"
        prefix={<SearchOutlined />}
        allowClear
        onChange={e => setSearchText(e.target.value)}
        style={{ width: 250, marginBottom: 16 }}
      />

      <Table dataSource={filteredApps} columns={columns} rowKey="id" loading={loading} />

      <Modal
        title="New App Definition"
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        onOk={() => form.submit()}
        width={600}
      >
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="name" label="App Name" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="image" label="Image" rules={[{ required: true }]}>
            <Input placeholder="192.168.11.136:30002/korail/myapp" />
          </Form.Item>
          <Form.Item name="default_tag" label="Default Tag" initialValue="latest">
            <Input />
          </Form.Item>
          <Form.Item name="default_replicas" label="Default Replicas" initialValue={1}>
            <InputNumber min={1} />
          </Form.Item>
          <Form.Item name="default_port" label="Container Port">
            <InputNumber min={1} max={65535} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}
