import { Button, Input, Space } from 'antd'
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons'

interface Props {
  value?: Record<string, string>
  onChange?: (v: Record<string, string>) => void
}

export function EnvEditor({ value = {}, onChange }: Props) {
  const pairs = Object.entries(value)

  const update = (pairs: [string, string][]) => {
    onChange?.(Object.fromEntries(pairs.filter(([k]) => k)))
  }

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      {pairs.map(([k, v], i) => (
        <Space key={i}>
          <Input
            placeholder="KEY"
            value={k}
            onChange={(e) => {
              const next = [...pairs] as [string, string][]
              next[i] = [e.target.value, v]
              update(next)
            }}
          />
          <Input
            placeholder="value"
            value={v}
            onChange={(e) => {
              const next = [...pairs] as [string, string][]
              next[i] = [k, e.target.value]
              update(next)
            }}
          />
          <MinusCircleOutlined
            onClick={() => {
              const next = pairs.filter((_, idx) => idx !== i) as [string, string][]
              update(next)
            }}
          />
        </Space>
      ))}
      <Button
        type="dashed"
        icon={<PlusOutlined />}
        onClick={() => update([...pairs, ['', '']] as [string, string][])}
      >
        Add env var
      </Button>
    </Space>
  )
}
