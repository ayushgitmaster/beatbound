import { useEffect, useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'
import { getConditions, getSymptoms } from '../api'
import { Badge } from '../components/ui/Badge'
import { Spinner } from '../components/ui/Spinner'
import { EcgLine } from '../components/EcgLine'

function CollapsibleCard({ title, badge, children }: { title: string; badge?: string; children: React.ReactNode }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden bg-white shadow-sm">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3.5 hover:bg-gray-50 transition-colors text-left"
      >
        <div className="flex items-center gap-2">
          <span className="font-medium text-sm text-gray-800">{title}</span>
          {badge != null && <Badge variant="info">{badge}</Badge>}
        </div>
        {open ? <ChevronUp size={16} className="text-gray-400 shrink-0" /> : <ChevronDown size={16} className="text-gray-400 shrink-0" />}
      </button>
      {open && <div className="border-t border-gray-100 animate-fade-in">{children}</div>}
    </div>
  )
}

export default function Resources() {
  const [conditions, setConditions] = useState<Record<string, unknown>>({})
  const [symptoms, setSymptoms] = useState<Record<string, unknown>>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getConditions(), getSymptoms()])
      .then(([c, s]) => { setConditions(c); setSymptoms(s) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="flex flex-col h-screen overflow-y-auto">
      <div className="shrink-0 relative border-b border-gray-100">
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary-600 rounded-r" />
        <div className="pl-7 pr-6 py-3 bg-white flex items-center justify-between gap-4 overflow-hidden">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Clinical Resources</h1>
            <p className="text-xs text-gray-500">Heart conditions, symptoms, and clinical guidance</p>
          </div>
          <EcgLine className="w-36 hidden sm:block" opacity={0.45} />
        </div>
      </div>

      <div className="flex-1 p-6 max-w-3xl mx-auto w-full space-y-6">
        {loading ? (
          <div className="flex justify-center py-16"><Spinner className="h-8 w-8" /></div>
        ) : (
          <>
            <section>
              <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">
                Heart Conditions
              </h2>
              <div className="space-y-2">
                {Object.entries(conditions).map(([key, val]) => {
                  const v = val as Record<string, unknown>
                  const symptoms_list = Array.isArray(v['symptoms']) ? v['symptoms'] as string[] : []
                  const risk_list = Array.isArray(v['risk_factors']) ? v['risk_factors'] as string[] : []
                  const mgmt_list = Array.isArray(v['management']) ? v['management'] as string[] : []
                  return (
                    <CollapsibleCard key={key} title={String(v['name'] ?? key)}>
                      <div className="px-4 py-4 space-y-3 text-sm text-gray-700">
                        {v['description'] != null && (
                          <p className="leading-relaxed">{String(v['description'])}</p>
                        )}
                        {symptoms_list.length > 0 && (
                          <div>
                            <p className="text-xs font-semibold text-gray-500 mb-1.5 uppercase tracking-wide">Symptoms</p>
                            <div className="flex flex-wrap gap-1.5">
                              {symptoms_list.map((s, i) => <Badge key={i} variant="info">{s}</Badge>)}
                            </div>
                          </div>
                        )}
                        {risk_list.length > 0 && (
                          <div>
                            <p className="text-xs font-semibold text-gray-500 mb-1.5 uppercase tracking-wide">Risk Factors</p>
                            <div className="flex flex-wrap gap-1.5">
                              {risk_list.map((r, i) => <Badge key={i} variant="warning">{r}</Badge>)}
                            </div>
                          </div>
                        )}
                        {mgmt_list.length > 0 && (
                          <div>
                            <p className="text-xs font-semibold text-gray-500 mb-1.5 uppercase tracking-wide">Management</p>
                            <ul className="space-y-1">
                              {mgmt_list.map((m, i) => (
                                <li key={i} className="flex gap-2 text-sm">
                                  <span className="text-primary-400 shrink-0">•</span>{m}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </CollapsibleCard>
                  )
                })}
              </div>
            </section>

            <section>
              <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">
                Symptom Guide
              </h2>
              <div className="space-y-2">
                {Object.entries(symptoms).map(([key, val]) => {
                  const v = val as Record<string, unknown>
                  const isEmergency = Boolean(v['emergency'])
                  const badgeLabel = isEmergency ? 'Emergency' : (v['severity'] != null ? String(v['severity']) : undefined)
                  return (
                    <CollapsibleCard
                      key={key}
                      title={String(v['name'] ?? key)}
                      badge={badgeLabel}
                    >
                      <div className="px-4 py-4 space-y-3 text-sm text-gray-700">
                        {v['description'] != null && (
                          <p className="leading-relaxed">{String(v['description'])}</p>
                        )}
                        {isEmergency && (
                          <div className="flex gap-2 items-start bg-danger-50 border border-danger-200 rounded-lg px-3 py-2 text-xs text-danger-700">
                            🚨 This may be an emergency — call 911 immediately.
                          </div>
                        )}
                        {v['advice'] != null && (
                          <p className="text-xs text-gray-600 italic">{String(v['advice'])}</p>
                        )}
                      </div>
                    </CollapsibleCard>
                  )
                })}
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  )
}
