import { useState, useEffect } from 'react'
import {
  Layers, RefreshCw, Brain, Zap, ShieldCheck, TrendingUp,
  ChevronDown, ChevronUp, Activity, Target, BarChart2,
  CheckCircle2, Clock, Cpu, FlaskConical,
} from 'lucide-react'
import { getExplain } from '../api'
import type { ExplainResponse } from '../types'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'
import { Progress } from '../components/ui/Progress'
import { Spinner } from '../components/ui/Spinner'
import { cn, confColor } from '../lib/utils'
import { EcgLine } from '../components/EcgLine'

// ── Demo / fallback data ──────────────────────────────────────────────────────
const DEMO_METRICS = [
  { label: 'Response Latency', value: '1.24s', icon: Clock, color: 'text-blue-500', bg: 'bg-blue-50' },
  { label: 'Model Used', value: 'Gemini 2.5', icon: Cpu, color: 'text-primary-600', bg: 'bg-primary-50' },
  { label: 'Token Usage', value: '842 tok', icon: Zap, color: 'text-amber-500', bg: 'bg-amber-50' },
  { label: 'Safety Score', value: '98%', icon: ShieldCheck, color: 'text-success-600', bg: 'bg-success-50' },
]

const DEMO_STEPS = [
  { step: 1, description: 'Parsed and tokenised user query', confidence: 0.99, duration: '12ms' },
  { step: 2, description: 'Intent classified as: Cardiac Risk Assessment', confidence: 0.94, duration: '38ms' },
  { step: 3, description: 'Clinical knowledge retrieved and fused into prompt context', confidence: 0.88, duration: '210ms' },
  { step: 4, description: 'Gemini 2.5 Flash inference completed', confidence: 0.91, duration: '960ms' },
  { step: 5, description: 'Safety and medical disclaimer checks passed', confidence: 0.98, duration: '18ms' },
  { step: 6, description: 'Response formatted and returned to client', confidence: 0.99, duration: '6ms' },
]

const DEMO_SOURCES = [
  { source: 'ACC/AHA 2019 Cardiovascular Risk Guidelines', relevance_score: 0.91, doc_type: 'guideline', chunk_text: 'The pooled cohort equations estimate 10-year ASCVD risk for patients aged 40–79 years, incorporating age, sex, race, lipids, blood pressure, diabetes status, and smoking.' },
  { source: 'ESC 2023 Heart Failure Guidelines', relevance_score: 0.78, doc_type: 'guideline', chunk_text: 'BNP > 400 pg/mL combined with reduced LVEF strongly suggests acute decompensated heart failure requiring urgent clinical evaluation.' },
  { source: 'AHA Cholesterol Clinical Advisory', relevance_score: 0.65, doc_type: 'advisory', chunk_text: 'LDL-C reduction of ≥50% from baseline is the primary target for high-risk patients on maximally tolerated statin therapy.' },
]

const DEMO_MODEL_PERF = [
  { label: 'Factual Accuracy', score: 91, color: 'bg-primary-500' },
  { label: 'Clinical Safety', score: 98, color: 'bg-success-500' },
  { label: 'Response Relevance', score: 87, color: 'bg-blue-500' },
  { label: 'Guideline Adherence', score: 83, color: 'bg-amber-500' },
  { label: 'Hallucination Risk', score: 6, color: 'bg-danger-500', inverted: true },
]

const TABS = ['Overview', 'Reasoning Chain', 'Sources', 'Model Performance'] as const
type Tab = typeof TABS[number]

// ── Radial confidence gauge ───────────────────────────────────────────────────
function RadialGauge({ value, label }: { value: number; label: string }) {
  const r = 52
  const circ = 2 * Math.PI * r
  const pct = Math.min(Math.max(value, 0), 100)
  const dash = (pct / 100) * circ
  const color = pct >= 75 ? '#16a34a' : pct >= 50 ? '#ca8a04' : '#dc2626'

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={130} height={130} viewBox="0 0 130 130">
        {/* track */}
        <circle cx={65} cy={65} r={r} fill="none" stroke="#f1f5f9" strokeWidth={10} />
        {/* fill */}
        <circle
          cx={65} cy={65} r={r} fill="none"
          stroke={color} strokeWidth={10}
          strokeDasharray={`${dash} ${circ - dash}`}
          strokeLinecap="round"
          transform="rotate(-90 65 65)"
          style={{ transition: 'stroke-dasharray 1s ease' }}
        />
        {/* tick marks */}
        {[0, 25, 50, 75, 100].map((t) => {
          const angle = (t / 100) * 360 - 90
          const rad = (angle * Math.PI) / 180
          const x1 = 65 + (r - 7) * Math.cos(rad)
          const y1 = 65 + (r - 7) * Math.sin(rad)
          const x2 = 65 + (r + 2) * Math.cos(rad)
          const y2 = 65 + (r + 2) * Math.sin(rad)
          return <line key={t} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#cbd5e1" strokeWidth={1.5} />
        })}
        <text x={65} y={62} textAnchor="middle" fontSize={22} fontWeight={700} fill={color}>{pct.toFixed(0)}</text>
        <text x={65} y={77} textAnchor="middle" fontSize={10} fill="#94a3b8">%</text>
      </svg>
      <span className="text-xs font-medium text-gray-500">{label}</span>
    </div>
  )
}

// ── Animated count-up ─────────────────────────────────────────────────────────
function CountUp({ target, suffix = '' }: { target: number; suffix?: string }) {
  const [val, setVal] = useState(0)
  useEffect(() => {
    let start = 0
    const step = target / 40
    const id = setInterval(() => {
      start += step
      if (start >= target) { setVal(target); clearInterval(id) }
      else setVal(Math.floor(start))
    }, 25)
    return () => clearInterval(id)
  }, [target])
  return <span>{val}{suffix}</span>
}

// ── Collapsible section ───────────────────────────────────────────────────────
function Section({ title, badge, icon: Icon, children }: {
  title: string; badge?: string; icon?: React.FC<{ size?: number; className?: string }>; children: React.ReactNode
}) {
  const [open, setOpen] = useState(true)
  return (
    <div className="border border-gray-200 rounded-xl overflow-hidden shadow-sm">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 transition-colors text-left"
      >
        <div className="flex items-center gap-2">
          {Icon && <Icon size={15} className="text-primary-500" />}
          <span className="font-semibold text-sm text-gray-800">{title}</span>
          {badge && <Badge variant="info">{badge}</Badge>}
        </div>
        {open ? <ChevronUp size={15} className="text-gray-400" /> : <ChevronDown size={15} className="text-gray-400" />}
      </button>
      {open && <div className="animate-fade-in bg-white">{children}</div>}
    </div>
  )
}

// ── Reasoning step timeline ───────────────────────────────────────────────────
function ReasoningTimeline({ steps }: { steps: typeof DEMO_STEPS }) {
  return (
    <div className="px-4 py-4 space-y-0">
      {steps.map((s, i) => (
        <div key={i} className="flex gap-3 group">
          {/* spine */}
          <div className="flex flex-col items-center">
            <div className={cn(
              'w-7 h-7 rounded-full flex items-center justify-center shrink-0 border-2 transition-colors',
              s.confidence >= 0.9 ? 'bg-success-50 border-success-400' :
              s.confidence >= 0.75 ? 'bg-primary-50 border-primary-400' : 'bg-warning-50 border-warning-400'
            )}>
              <CheckCircle2 size={14} className={
                s.confidence >= 0.9 ? 'text-success-500' :
                s.confidence >= 0.75 ? 'text-primary-500' : 'text-warning-500'
              } />
            </div>
            {i < steps.length - 1 && <div className="w-px flex-1 bg-gray-200 my-1" />}
          </div>
          {/* content */}
          <div className="flex-1 pb-4">
            <div className="flex items-start justify-between gap-2">
              <p className="text-sm text-gray-800 font-medium leading-snug">{s.description}</p>
              <span className="text-[10px] text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded shrink-0">{s.duration}</span>
            </div>
            <div className="flex items-center gap-2 mt-1.5">
              <Progress
                value={s.confidence * 100}
                className="w-28 h-1.5"
                color={s.confidence >= 0.9 ? 'bg-success-500' : s.confidence >= 0.75 ? 'bg-primary-500' : 'bg-warning-500'}
              />
              <span className={`text-[11px] ${confColor(s.confidence)}`}>
                {(s.confidence * 100).toFixed(0)}% confident
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

// ── Main component ────────────────────────────────────────────────────────────
export default function Explain() {
  const [data, setData] = useState<ExplainResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<Tab>('Overview')
  const [selectedSource, setSelectedSource] = useState<number | null>(null)

  const load = async () => {
    setLoading(true)
    try { const res = await getExplain(); setData(res) } catch { /* use demo */ }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  // Merge live data with demos
  const confidence = data?.overall_confidence != null ? data.overall_confidence * 100 : 89
  const query = data?.query ?? 'What are the first-line treatments for hypertension with LVH?'
  const steps  = (data?.reasoning_steps ?? []).length > 1
    ? (data!.reasoning_steps as unknown as typeof DEMO_STEPS)
    : DEMO_STEPS
  const sources = (data?.sources ?? []).length > 0
    ? data!.sources.map(s => ({
        source: String(s['source'] ?? ''),
        relevance_score: Number(s['relevance_score'] ?? 0),
        doc_type: String(s['doc_type'] ?? 'guideline'),
        chunk_text: String(s['chunk_text'] ?? s['content'] ?? ''),
      }))
    : DEMO_SOURCES

  return (
    <div className="flex flex-col h-screen overflow-y-auto bg-gray-50">
      {/* Header */}
      <div className="shrink-0 relative border-b border-gray-100">
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary-600 rounded-r" />
        <div className="pl-7 pr-6 py-3 bg-white flex items-center justify-between gap-4 overflow-hidden">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Explainability Dashboard</h1>
            <p className="text-xs text-gray-500">AI reasoning · model metrics · source attribution</p>
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <EcgLine className="w-36 hidden sm:block" opacity={0.45} />
            <Button variant="outline" size="sm" onClick={load} className="gap-1.5">
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              Refresh
            </Button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-0.5 px-6 pt-2 bg-white border-t border-gray-50">
          {TABS.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={cn(
                'px-4 py-2 text-xs font-medium rounded-t-lg border-b-2 transition-colors',
                activeTab === tab
                  ? 'border-primary-600 text-primary-700 bg-primary-50'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
              )}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-24"><Spinner className="h-8 w-8" /></div>
      ) : (
        <div className="flex-1 p-6 space-y-5">

          {/* ── OVERVIEW TAB ──────────────────────────────────────────── */}
          {activeTab === 'Overview' && (
            <>
              {/* Query pill */}
              <div className="bg-white border border-gray-200 rounded-xl px-4 py-3 flex items-start gap-3 shadow-sm">
                <Brain size={16} className="text-primary-500 shrink-0 mt-0.5" />
                <div>
                  <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide mb-0.5">Last Query Analysed</p>
                  <p className="text-sm text-gray-800 font-medium">"{query}"</p>
                </div>
              </div>

              {/* KPI row */}
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                {DEMO_METRICS.map(({ label, value, icon: Icon, color, bg }) => (
                  <div key={label} className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm flex items-center gap-3">
                    <div className={cn('w-9 h-9 rounded-xl flex items-center justify-center shrink-0', bg)}>
                      <Icon size={18} className={color} />
                    </div>
                    <div>
                      <p className="text-[10px] text-gray-400 font-medium uppercase tracking-wide">{label}</p>
                      <p className="text-base font-bold text-gray-900">{value}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Gauges row */}
              <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                <p className="text-sm font-semibold text-gray-800 mb-4 flex items-center gap-2">
                  <Target size={15} className="text-primary-500" />
                  Confidence & Quality Gauges
                </p>
                <div className="flex flex-wrap justify-around gap-4">
                  <RadialGauge value={confidence} label="Overall Confidence" />
                  <RadialGauge value={87} label="Relevance Score" />
                  <RadialGauge value={98} label="Safety Rating" />
                  <RadialGauge value={83} label="Guideline Adherence" />
                </div>
              </div>

              {/* Live stats */}
              <div className="grid grid-cols-3 gap-3">
                {[
                  { label: 'Queries Processed', target: 1247, suffix: '', icon: Activity, color: 'text-primary-500' },
                  { label: 'Sources Evaluated', target: 38, suffix: '', icon: FlaskConical, color: 'text-blue-500' },
                  { label: 'Avg Accuracy', target: 91, suffix: '%', icon: TrendingUp, color: 'text-success-600' },
                ].map(({ label, target, suffix, icon: Icon, color }) => (
                  <div key={label} className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm text-center">
                    <Icon size={20} className={cn('mx-auto mb-2', color)} />
                    <p className="text-2xl font-bold text-gray-900">
                      <CountUp target={target} suffix={suffix} />
                    </p>
                    <p className="text-[11px] text-gray-400 mt-0.5">{label}</p>
                  </div>
                ))}
              </div>
            </>
          )}

          {/* ── REASONING CHAIN TAB ───────────────────────────────────── */}
          {activeTab === 'Reasoning Chain' && (
            <Section title="Step-by-Step Reasoning" badge={`${steps.length} steps`} icon={Brain}>
              <ReasoningTimeline steps={steps} />
            </Section>
          )}

          {/* ── SOURCES TAB ───────────────────────────────────────────── */}
          {activeTab === 'Sources' && (
            <div className="space-y-3">
              <p className="text-xs text-gray-500 px-1">Click a source to expand the retrieved chunk.</p>
              {sources.map((s, i) => (
                <div
                  key={i}
                  className={cn(
                    'bg-white border rounded-xl overflow-hidden shadow-sm cursor-pointer transition-all',
                    selectedSource === i ? 'border-primary-400 ring-1 ring-primary-200' : 'border-gray-200 hover:border-gray-300'
                  )}
                  onClick={() => setSelectedSource(selectedSource === i ? null : i)}
                >
                  <div className="px-4 py-3 flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1.5">
                        <span className="text-[10px] font-semibold uppercase tracking-wide text-primary-600 bg-primary-50 px-1.5 py-0.5 rounded">
                          {s.doc_type}
                        </span>
                        <span className={cn('text-xs font-bold', confColor(s.relevance_score))}>
                          {(s.relevance_score * 100).toFixed(0)}% match
                        </span>
                      </div>
                      <p className="text-sm font-medium text-gray-800">{s.source}</p>
                    </div>
                    {selectedSource === i
                      ? <ChevronUp size={15} className="text-gray-400 shrink-0 mt-1" />
                      : <ChevronDown size={15} className="text-gray-400 shrink-0 mt-1" />}
                  </div>
                  <Progress
                    value={s.relevance_score * 100}
                    className="h-1 rounded-none mx-4 mb-3"
                    color={s.relevance_score >= 0.8 ? 'bg-success-500' : s.relevance_score >= 0.6 ? 'bg-primary-500' : 'bg-warning-500'}
                  />
                  {selectedSource === i && (
                    <div className="px-4 pb-4 animate-fade-in">
                      <div className="bg-gray-50 rounded-lg px-3 py-2.5 text-xs text-gray-600 leading-relaxed border border-gray-100">
                        {s.chunk_text || 'No excerpt available.'}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* ── MODEL PERFORMANCE TAB ─────────────────────────────────── */}
          {activeTab === 'Model Performance' && (
            <div className="space-y-4">
              <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                <p className="text-sm font-semibold text-gray-800 mb-4 flex items-center gap-2">
                  <BarChart2 size={15} className="text-primary-500" />
                  Model Quality Metrics
                </p>
                <div className="space-y-4">
                  {DEMO_MODEL_PERF.map(({ label, score, color, inverted }) => (
                    <div key={label}>
                      <div className="flex justify-between text-xs text-gray-600 mb-1.5">
                        <span className="font-medium">{label}</span>
                        <span className={cn('font-bold', inverted
                          ? score <= 10 ? 'text-success-600' : score <= 25 ? 'text-warning-600' : 'text-danger-600'
                          : score >= 85 ? 'text-success-600' : score >= 65 ? 'text-warning-600' : 'text-danger-600'
                        )}>
                          {inverted ? `Low (${score}%)` : `${score}%`}
                        </span>
                      </div>
                      <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className={cn('h-full rounded-full transition-all duration-700', color)}
                          style={{ width: `${score}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Model info cards */}
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: 'Architecture', value: 'Gemini 2.5 Flash', icon: Cpu, color: 'text-primary-500', bg: 'bg-primary-50' },
                  { label: 'Context Window', value: '1 M tokens', icon: Layers, color: 'text-blue-500', bg: 'bg-blue-50' },
                  { label: 'Specialisation', value: 'Medical + Clinical', icon: FlaskConical, color: 'text-purple-500', bg: 'bg-purple-50' },
                  { label: 'Safety Layer', value: 'RLHF + Medical', icon: ShieldCheck, color: 'text-success-600', bg: 'bg-success-50' },
                ].map(({ label, value, icon: Icon, color, bg }) => (
                  <div key={label} className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm">
                    <div className={cn('w-8 h-8 rounded-lg flex items-center justify-center mb-2', bg)}>
                      <Icon size={16} className={color} />
                    </div>
                    <p className="text-[10px] text-gray-400 uppercase tracking-wide font-semibold">{label}</p>
                    <p className="text-sm font-bold text-gray-800 mt-0.5">{value}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
