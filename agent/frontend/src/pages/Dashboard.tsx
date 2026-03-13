import { useEffect, useState } from 'react'
import { Card, Col, Row, Spin, Statistic, Typography, message } from 'antd'
import {
  CloudServerOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  DeploymentUnitOutlined,
  WarningOutlined,
} from '@ant-design/icons'
import { getOverview } from '@/api/deployments'
import type { Overview } from '@/types'

export function Dashboard() {
  const [data, setData] = useState<Overview | null>(null)

  useEffect(() => {
    getOverview().then(setData).catch(() => message.error('Failed to load dashboard'))
    const t = setInterval(() => {
      if (!document.hidden) {
        getOverview().then(setData)
      }
    }, 15000)
    return () => clearInterval(t)
  }, [])

  if (!data) return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />

  return (
    <div>
      <Typography.Title level={3}>Dashboard</Typography.Title>
      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card>
            <Statistic
              title="Total Devices"
              value={data.devices.total}
              prefix={<CloudServerOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="Online"
              value={data.devices.online}
              valueStyle={{ color: '#3f8600' }}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="Offline"
              value={data.devices.offline}
              valueStyle={{ color: '#cf1322' }}
              prefix={<CloseCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="Total Deployments"
              value={data.deployments.total}
              prefix={<DeploymentUnitOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="Running"
              value={data.deployments.running}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="Failed"
              value={data.deployments.failed}
              valueStyle={{ color: '#cf1322' }}
              prefix={<WarningOutlined />}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}
