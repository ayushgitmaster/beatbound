import { Component, type ErrorInfo, type ReactNode } from 'react'

interface Props {
  children: ReactNode
}
interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('App error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError && this.state.error) {
      return (
        <div style={{
          padding: '2rem',
          fontFamily: 'system-ui',
          maxWidth: '600px',
          margin: '2rem auto',
          border: '1px solid #c41e3a',
          borderRadius: '8px',
          backgroundColor: '#fff5f5',
        }}>
          <h1 style={{ color: '#c41e3a', marginTop: 0 }}>Something went wrong</h1>
          <p><strong>{this.state.error.message}</strong></p>
          <p style={{ fontSize: '0.9rem', color: '#666' }}>
            Check the browser console (F12 → Console) for details. Fix the error and refresh.
          </p>
        </div>
      )
    }
    return this.props.children
  }
}
