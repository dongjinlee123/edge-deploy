import { Layout, Menu } from 'antd'
import {
  DashboardOutlined,
  DeploymentUnitOutlined,
  AppstoreOutlined,
  CloudServerOutlined,
} from '@ant-design/icons'
import { Link, useLocation } from 'react-router-dom'

const { Sider, Header, Content } = Layout

const menuItems = [
  { key: '/', icon: <DashboardOutlined />, label: <Link to="/">Dashboard</Link> },
  { key: '/devices', icon: <CloudServerOutlined />, label: <Link to="/devices">Devices</Link> },
  { key: '/apps', icon: <AppstoreOutlined />, label: <Link to="/apps">Apps</Link> },
  { key: '/deployments', icon: <DeploymentUnitOutlined />, label: <Link to="/deployments">Deployments</Link> },
]

export function AppLayout({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const selectedKey = menuItems.find(
    (item) => item.key !== '/' && location.pathname.startsWith(item.key)
  )?.key ?? (location.pathname === '/' ? '/' : '')

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible>
        <div style={{ color: 'white', padding: '16px', fontSize: 16, fontWeight: 'bold' }}>
          EdgeDeploy
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[selectedKey]}
          items={menuItems}
        />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 24px', fontSize: 18, fontWeight: 500 }}>
          Edge Deploy Controller
        </Header>
        <Content style={{ margin: '24px', padding: '24px', background: '#fff', borderRadius: 8 }}>
          {children}
        </Content>
      </Layout>
    </Layout>
  )
}
