import { createBrowserRouter } from 'react-router-dom'
import { AppLayout } from '@/components/Layout'
import { Dashboard } from '@/pages/Dashboard'
import { DeviceList } from '@/pages/DeviceList'
import { DeviceDetail } from '@/pages/DeviceDetail'
import { AppList } from '@/pages/AppList'
import { AppDetail } from '@/pages/AppDetail'
import { DeploymentList } from '@/pages/DeploymentList'
import { DeploymentCreate } from '@/pages/DeploymentCreate'
import { DeploymentDetail } from '@/pages/DeploymentDetail'

function wrap(element: React.ReactNode) {
  return <AppLayout>{element}</AppLayout>
}

export const router = createBrowserRouter([
  { path: '/', element: wrap(<Dashboard />) },
  { path: '/devices', element: wrap(<DeviceList />) },
  { path: '/devices/:id', element: wrap(<DeviceDetail />) },
  { path: '/apps', element: wrap(<AppList />) },
  { path: '/apps/:id', element: wrap(<AppDetail />) },
  { path: '/deployments', element: wrap(<DeploymentList />) },
  { path: '/deployments/new', element: wrap(<DeploymentCreate />) },
  { path: '/deployments/:id', element: wrap(<DeploymentDetail />) },
])
