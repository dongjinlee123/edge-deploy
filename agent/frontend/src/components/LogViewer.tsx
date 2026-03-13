interface Props {
  logs: string
  maxHeight?: number
}

export function LogViewer({ logs, maxHeight = 400 }: Props) {
  return (
    <div
      style={{
        background: '#1e1e1e',
        color: '#d4d4d4',
        padding: 16,
        borderRadius: 4,
        fontFamily: 'monospace',
        fontSize: 13,
        maxHeight,
        overflowY: 'auto',
        whiteSpace: 'pre-wrap',
        wordBreak: 'break-all',
      }}
    >
      {logs || 'No logs'}
    </div>
  )
}
