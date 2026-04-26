import { useState } from 'react'
import { AlertTriangle, Send } from 'lucide-react'
import { symptomAssess } from '../api'
import { Button } from '../components/ui/Button'
import { Card, CardContent } from '../components/ui/Card'
import { Badge } from '../components/ui/Badge'
import { Spinner } from '../components/ui/Spinner'
import { EcgLine } from '../components/EcgLine'

const COMMON = [
  'Chest pain that radiates to my left arm',
  'Sudden shortness of breath at rest',
  'Heart palpitations lasting 10 minutes',
  'Swollen ankles and fatigue',
  'Dizziness and near-fainting episode',
]

export default function Symptom() {
  const [input, setInput] = useState('')
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const assess = async () => {
    if (!input.trim()) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await symptomAssess(input.trim())
      setResult(res)
    } catch {
      setError('Failed to assess symptoms. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const level = result ? String(result.emergency_level ?? '').toUpperCase() : ''
  const levelColor =
    level === 'HIGH' ? 'bg-danger-50 border-danger-500 text-danger-700' :
    level === 'MEDIUM' ? 'bg-warning-50 border-warning-500 text-warning-700' :
    'bg-success-50 border-success-500 text-success-700'

  const identifiedSymptoms = result?.identified_symptoms != null && Array.isArray(result.identified_symptoms)
    ? result.identified_symptoms as string[]
    : null
  const recommendedActions = result?.recommended_actions != null && Array.isArray(result.recommended_actions)
    ? result.recommended_actions as string[]
    : null

  return (
    <div className="flex flex-col h-screen overflow-y-auto">
      <div className="shrink-0 relative border-b border-gray-100">
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary-600 rounded-r" />
        <div className="pl-7 pr-6 py-3 bg-white flex items-center justify-between gap-4 overflow-hidden">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Symptom Checker</h1>
            <p className="text-xs text-gray-500">Describe your symptoms for an AI-powered cardiac assessment</p>
          </div>
          <EcgLine className="w-36 hidden sm:block" opacity={0.45} />
        </div>
      </div>

      <div className="flex-1 p-6 max-w-2xl mx-auto w-full space-y-5">
        <Card>
          <CardContent className="pt-5 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Describe your symptoms</label>
              <textarea
                rows={4}
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="e.g. I have been having sharp chest pain that radiates to my jaw for the past 20 minutes…"
                className="w-full border border-gray-300 rounded-xl px-4 py-3 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-200 focus:border-primary-400 transition resize-none"
              />
            </div>
            <div className="flex flex-wrap gap-2">
              {COMMON.map(s => (
                <button
                  key={s}
                  onClick={() => setInput(s)}
                  className="text-xs bg-gray-50 border border-gray-200 text-gray-600 rounded-full px-3 py-1 hover:bg-primary-50 hover:border-primary-200 hover:text-primary-700 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
            <Button onClick={assess} loading={loading} className="w-full gap-2">
              <Send size={16} />
              {loading ? 'Assessing…' : 'Assess Symptoms'}
            </Button>
          </CardContent>
        </Card>

        {error && (
          <div className="flex gap-2 items-center bg-danger-50 border border-danger-500 rounded-xl px-4 py-3 text-sm text-danger-700">
            <AlertTriangle size={16} className="shrink-0" />
            {error}
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-12">
            <Spinner className="h-7 w-7" />
          </div>
        )}

        {result && !loading && (
          <Card>
            <div className="px-5 pt-5 pb-3 flex items-center justify-between">
              <h3 className="text-base font-semibold text-gray-900">Assessment Result</h3>
              {level && (
                <Badge variant={level === 'HIGH' ? 'danger' : level === 'MEDIUM' ? 'warning' : 'success'}>
                  {level} urgency
                </Badge>
              )}
            </div>
            <div className="px-5 pb-5 space-y-4">
              {level && (
                <div className={`border rounded-xl px-4 py-3 text-sm font-medium ${levelColor}`}>
                  {level === 'HIGH' ? '🚨 ' : level === 'MEDIUM' ? '⚠️ ' : '✅ '}
                  Emergency level: {level}
                </div>
              )}
              {result.reasoning != null && (
                <div>
                  <p className="text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">Clinical Reasoning</p>
                  <p className="text-sm text-gray-700 leading-relaxed">{String(result.reasoning)}</p>
                </div>
              )}
              {identifiedSymptoms && identifiedSymptoms.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">Identified Symptoms</p>
                  <div className="flex flex-wrap gap-2">
                    {identifiedSymptoms.map((s, i) => <Badge key={i} variant="info">{s}</Badge>)}
                  </div>
                </div>
              )}
              {recommendedActions && recommendedActions.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wide">Recommended Actions</p>
                  <ul className="space-y-1">
                    {recommendedActions.map((a, i) => (
                      <li key={i} className="flex gap-2 text-sm text-gray-700">
                        <span className="text-primary-500 shrink-0">•</span>
                        {a}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <p className="text-xs text-gray-400 border-t border-gray-100 pt-3">
                ⚕️ This is an AI-generated assessment for informational purposes only. Call emergency services immediately for severe symptoms.
              </p>
            </div>
          </Card>
        )}
      </div>
    </div>
  )
}
