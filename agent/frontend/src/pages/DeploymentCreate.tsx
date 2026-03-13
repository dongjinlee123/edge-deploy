import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import {
  Button, Form, Input, InputNumber, Select, Tabs, Typography, message,
} from 'antd'
import { createFormDeployment, createYAMLDeployment } from '@/api/deployments'
import { getDevices } from '@/api/devices'
import { getApps } from '@/api/apps'
import { EnvEditor } from '@/components/EnvEditor'
import type { App, Device } from '@/types'

export function DeploymentCreate() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const preselectedAppId = searchParams.get('app_id') ? Number(searchParams.get('app_id')) : undefined

  const [devices, setDevices] = useState<Device[]>([])
  const [apps, setApps] = useState<App[]>([])
  const [formForm] = Form.useForm()
  const [yamlForm] = Form.useForm()
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    getDevices().then(setDevices)
    getApps().then(setApps)
  }, [])

  const handleFormSubmit = async (values: {
    app_id: number
    device_id: number
    namespace: string
    tag?: string
    replicas?: number
    port?: number
    env?: Record<string, string>
  }) => {
    setLoading(true)
    try {
      const d = await createFormDeployment(values)
      message.success('Deployment created')
      navigate(`/deployments/${d.id}`)
    } catch (err: any) {
      message.error(`Deploy failed: ${err?.message ?? err}`)
    } finally {
      setLoading(false)
    }
  }

  const handleYAMLSubmit = async (values: {
    device_id: number
    namespace: string
    manifests: string
  }) => {
    setLoading(true)
    try {
      const d = await createYAMLDeployment(values)
      message.success('Deployment created')
      navigate(`/deployments/${d.id}`)
    } catch (err: any) {
      message.error(`Apply YAML failed: ${err?.message ?? err}`)
    } finally {
      setLoading(false)
    }
  }

  const deviceOptions = devices.map(d => ({ value: d.id, label: `${d.name} (${d.address})` }))
  const appOptions = apps.map(a => ({ value: a.id, label: a.name }))

  const formTab = (
    <Form
      form={formForm}
      layout="vertical"
      onFinish={handleFormSubmit}
      initialValues={{ namespace: 'default', app_id: preselectedAppId }}
    >
      <Form.Item name="app_id" label="App" rules={[{ required: true }]}>
        <Select options={appOptions} placeholder="Select app" />
      </Form.Item>
      <Form.Item name="device_id" label="Target Device" rules={[{ required: true }]}>
        <Select options={deviceOptions} placeholder="Select device" />
      </Form.Item>
      <Form.Item name="namespace" label="Namespace" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="tag" label="Image Tag (overrides app default)">
        <Input placeholder="latest" />
      </Form.Item>
      <Form.Item name="replicas" label="Replicas">
        <InputNumber min={0} />
      </Form.Item>
      <Form.Item name="port" label="Container Port">
        <InputNumber min={1} max={65535} />
      </Form.Item>
      <Form.Item name="env" label="Environment Variables">
        <EnvEditor />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>Deploy</Button>
      </Form.Item>
    </Form>
  )

  const yamlTab = (
    <Form
      form={yamlForm}
      layout="vertical"
      onFinish={handleYAMLSubmit}
      initialValues={{ namespace: 'default' }}
    >
      <Form.Item name="device_id" label="Target Device" rules={[{ required: true }]}>
        <Select options={deviceOptions} placeholder="Select device" />
      </Form.Item>
      <Form.Item name="namespace" label="Namespace" rules={[{ required: true }]}>
        <Input />
      </Form.Item>
      <Form.Item name="manifests" label="YAML Manifests" rules={[{ required: true }]}>
        <Input.TextArea
          rows={16}
          placeholder="Paste your Kubernetes YAML here (multi-doc separated by ---)"
          style={{ fontFamily: 'monospace', fontSize: 13 }}
        />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>Apply YAML</Button>
      </Form.Item>
    </Form>
  )

  return (
    <div>
      <Typography.Title level={3}>New Deployment</Typography.Title>
      <Tabs
        items={[
          { key: 'form', label: 'Form Mode', children: formTab },
          { key: 'yaml', label: 'Raw YAML Mode', children: yamlTab },
        ]}
      />
    </div>
  )
}
