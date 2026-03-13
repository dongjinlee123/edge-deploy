import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Button, Descriptions, Typography } from 'antd'
import { getApp } from '@/api/apps'
import type { App } from '@/types'

export function AppDetail() {
  const { id } = useParams<{ id: string }>()
  const [app, setApp] = useState<App | null>(null)

  useEffect(() => { getApp(Number(id)).then(setApp) }, [id])

  if (!app) return null

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Typography.Title level={3}>App: {app.name}</Typography.Title>
        <Link to={`/deployments/new?app_id=${app.id}`}>
          <Button type="primary">Deploy to Device</Button>
        </Link>
      </div>

      <Descriptions bordered column={2}>
        <Descriptions.Item label="Image">{app.image}</Descriptions.Item>
        <Descriptions.Item label="Default Tag">{app.default_tag}</Descriptions.Item>
        <Descriptions.Item label="Default Replicas">{app.default_replicas}</Descriptions.Item>
        <Descriptions.Item label="Default Port">{app.default_port ?? '—'}</Descriptions.Item>
        <Descriptions.Item label="Created">{new Date(app.created_at).toLocaleString()}</Descriptions.Item>
        <Descriptions.Item label="Has Custom Template">{app.yaml_template ? 'Yes' : 'No'}</Descriptions.Item>
        {app.default_env && (
          <Descriptions.Item label="Default Env" span={2}>
            <pre style={{ margin: 0, fontSize: 12 }}>
              {JSON.stringify(app.default_env, null, 2)}
            </pre>
          </Descriptions.Item>
        )}
      </Descriptions>

      {app.yaml_template && (
        <div style={{ marginTop: 24 }}>
          <Typography.Title level={5}>YAML Template</Typography.Title>
          <pre style={{ background: '#f5f5f5', padding: 12, borderRadius: 4, overflow: 'auto', fontSize: 12 }}>
            {app.yaml_template}
          </pre>
        </div>
      )}
    </div>
  )
}
