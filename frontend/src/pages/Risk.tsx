import { useState } from 'react'
import { Calculator, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react'
import { riskScore } from '../api'
import type { RiskScoreRequest, RiskScoreResponse, RiskScore } from '../types'
import { Button } from '../components/ui/Button'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card'
import { Badge } from '../components/ui/Badge'
import { Progress } from '../components/ui/Progress'
import { Spinner } from '../components/ui/Spinner'
import { riskBgColor, riskBarColor, riskColor } from '../lib/utils'
import { EcgLine } from '../components/EcgLine'

const RISK_LEVEL_COLORS: Record<string, string> = {
  LOW:      'bg-success-50 border-success-500 text-success-600',
  MODERATE: 'bg-warning-50 border-warning-500 text-warning-600',
  HIGH:     'bg-danger-50 border-danger-500 text-danger-600',
  CRITICAL: 'bg-danger-50 border-danger-600 text-danger-700',
  UNKNOWN:  'bg-gray-50 border-gray-300 text-gray-600',
}

function RiskScoreCard({ score }: { score: RiskScore }) {
  const [expanded, setExpanded] = useState(false)
  const barColor = riskBarColor(score.risk_category)

  return (
    <div className={`border rounded-xl p-4 space-y-3 ${riskBgColor(score.risk_category)}`}>
      <div className="flex items-center justify-between">
        <h4 className="font-semibold text-gray-900 text-sm">{score.name}</h4>
        <Badge
          variant={
            score.risk_category.toLowerCase().includes('low') ? 'success' :
            score.risk_category.toLowerCase().includes('high') ? 'danger' : 'warning'
          }
        >
          {score.risk_category}
        </Badge>
      </div>

      {score.risk_percent != null && (
        <div>
          <div className="flex justify-between text-xs text-gray-600 mb-1">
            <span>10-year risk</span>
            <span className={`font-bold ${riskColor(score.risk_category)}`}>{score.risk_percent.toFixed(1)}%</span>
          </div>
          <Progress value={Math.min(score.risk_percent, 100)} max={100} color={barColor} />
        </div>
      )}
      {score.score != null && score.risk_percent == null && (
        <p className="text-2xl font-bold text-gray-900">{score.score}<span className="text-sm font-normal text-gray-500 ml-1">pts</span></p>
      )}

      <p className="text-xs text-gray-600 leading-relaxed">{score.interpretation}</p>

      {score.breakdown && score.breakdown.length > 0 && (
        <div>
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-gray-500 hover:text-gray-700 flex items-center gap-1"
          >
            {expanded ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
            {expanded ? 'Hide' : 'Show'} breakdown
          </button>
          {expanded && (
            <div className="mt-2 space-y-1 animate-fade-in">
              {score.breakdown.map((b, i) => (
                <div key={i} className="flex justify-between text-xs py-1 border-b border-black/5 last:border-0">
                  <span className="text-gray-600">{b.label}</span>
                  <span className="flex gap-2">
                    <span className="text-gray-800">{String(b.value)}</span>
                    {b.points != null && (
                      <span className={b.points > 0 ? 'text-danger-600 font-semibold' : 'text-gray-400'}>
                        {b.points > 0 ? `+${b.points}` : '0'}
                      </span>
                    )}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="block text-xs font-medium text-gray-600 mb-1">{label}</label>
      {children}
    </div>
  )
}

const inp = 'w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-200 focus:border-primary-400 transition'
const chk = 'w-4 h-4 rounded border-gray-300 text-primary-600 focus:ring-primary-400'

export default function Risk() {
  const [form, setForm] = useState<RiskScoreRequest>({
    age: 55,
    sex: 'male',
    race: 'white',
    total_cholesterol: 210,
    hdl_cholesterol: 45,
    ldl_cholesterol: 130,
    systolic_bp: 135,
    is_smoker: false,
    has_diabetes: false,
    on_bp_treatment: false,
    has_af: false,
    has_heart_failure: false,
    has_hypertension: false,
    has_vascular_disease: false,
    stroke_tia_history: false,
    labile_inr: false,
    on_antiplatelet_or_nsaid: false,
    alcohol_use: false,
    renal_disease: false,
    liver_disease: false,
    bleeding_history: false,
    heart_rate: 72,
    creatinine: 1.0,
    killip_class: 1,
    cardiac_arrest: false,
    st_deviation: false,
    elevated_enzymes: false,
  })
  const [result, setResult] = useState<RiskScoreResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showAdvanced, setShowAdvanced] = useState(false)

  const set = (k: keyof RiskScoreRequest, v: unknown) => setForm(f => ({ ...f, [k]: v }))
  const num = (k: keyof RiskScoreRequest) => (e: React.ChangeEvent<HTMLInputElement>) =>
    set(k, e.target.value === '' ? undefined : Number(e.target.value))
  const bool = (k: keyof RiskScoreRequest) => (e: React.ChangeEvent<HTMLInputElement>) =>
    set(k, e.target.checked)

  const calculate = async () => {
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await riskScore(form)
      setResult(res)
    } catch (e: unknown) {
      const detail = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(detail ?? 'Calculation failed. Please check your inputs.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen overflow-y-auto">
      <div className="shrink-0 relative border-b border-gray-100">
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary-600 rounded-r" />
        <div className="pl-7 pr-6 py-3 bg-white flex items-center justify-between gap-4 overflow-hidden">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Risk Dashboard</h1>
            <p className="text-xs text-gray-500">ASCVD · CHA₂DS₂-VASc · HAS-BLED · GRACE — all in one calculation</p>
          </div>
          <EcgLine className="w-36 hidden sm:block" opacity={0.45} />
        </div>
      </div>

      <div className="flex-1 p-6 grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
        {/* Input form */}
        <Card>
          <CardHeader>
            <CardTitle>Patient Parameters</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Field label="Age">
                <input type="number" min={18} max={120} value={form.age ?? ''} onChange={num('age')} className={inp} />
              </Field>
              <Field label="Sex">
                <select value={form.sex ?? ''} onChange={e => set('sex', e.target.value)} className={inp}>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </Field>
              <Field label="Race">
                <select value={form.race ?? ''} onChange={e => set('race', e.target.value)} className={inp}>
                  <option value="white">White</option>
                  <option value="african_american">African American</option>
                  <option value="other">Other</option>
                </select>
              </Field>
              <Field label="Total Cholesterol (mg/dL)">
                <input type="number" value={form.total_cholesterol ?? ''} onChange={num('total_cholesterol')} className={inp} />
              </Field>
              <Field label="HDL-C (mg/dL)">
                <input type="number" value={form.hdl_cholesterol ?? ''} onChange={num('hdl_cholesterol')} className={inp} />
              </Field>
              <Field label="Systolic BP (mmHg)">
                <input type="number" value={form.systolic_bp ?? ''} onChange={num('systolic_bp')} className={inp} />
              </Field>
            </div>

            <div className="grid grid-cols-2 gap-x-4 gap-y-2.5">
              {[
                { k: 'is_smoker', l: 'Current smoker' },
                { k: 'has_diabetes', l: 'Diabetes' },
                { k: 'on_bp_treatment', l: 'On BP treatment' },
                { k: 'has_hypertension', l: 'Hypertension' },
                { k: 'has_af', l: 'Atrial fibrillation' },
                { k: 'has_heart_failure', l: 'Heart failure' },
                { k: 'has_vascular_disease', l: 'Vascular disease' },
                { k: 'stroke_tia_history', l: 'Stroke/TIA history' },
              ].map(({ k, l }) => (
                <label key={k} className="flex items-center gap-2 cursor-pointer text-sm text-gray-700">
                  <input type="checkbox" checked={!!form[k as keyof RiskScoreRequest]} onChange={bool(k as keyof RiskScoreRequest)} className={chk} />
                  {l}
                </label>
              ))}
            </div>

            {/* Advanced (GRACE + HAS-BLED) */}
            <button
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="text-xs text-primary-600 hover:text-primary-800 flex items-center gap-1 font-medium"
            >
              {showAdvanced ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
              {showAdvanced ? 'Hide' : 'Show'} GRACE / HAS-BLED parameters
            </button>
            {showAdvanced && (
              <div className="animate-fade-in space-y-4 border-t border-gray-100 pt-4">
                <div className="grid grid-cols-2 gap-3">
                  <Field label="Heart Rate (bpm)">
                    <input type="number" value={form.heart_rate ?? ''} onChange={num('heart_rate')} className={inp} />
                  </Field>
                  <Field label="Creatinine (mg/dL)">
                    <input type="number" step="0.1" value={form.creatinine ?? ''} onChange={num('creatinine')} className={inp} />
                  </Field>
                  <Field label="Killip Class">
                    <select value={form.killip_class ?? 1} onChange={e => set('killip_class', Number(e.target.value))} className={inp}>
                      {[1,2,3,4].map(k => <option key={k} value={k}>Class {k}</option>)}
                    </select>
                  </Field>
                </div>
                <div className="grid grid-cols-2 gap-x-4 gap-y-2.5">
                  {[
                    { k: 'cardiac_arrest', l: 'Cardiac arrest at admission' },
                    { k: 'st_deviation', l: 'ST-segment deviation' },
                    { k: 'elevated_enzymes', l: 'Elevated cardiac enzymes' },
                    { k: 'labile_inr', l: 'Labile INR' },
                    { k: 'on_antiplatelet_or_nsaid', l: 'Antiplatelet/NSAID use' },
                    { k: 'alcohol_use', l: 'Alcohol use' },
                    { k: 'renal_disease', l: 'Renal disease' },
                    { k: 'liver_disease', l: 'Liver disease' },
                    { k: 'bleeding_history', l: 'Bleeding history' },
                  ].map(({ k, l }) => (
                    <label key={k} className="flex items-center gap-2 cursor-pointer text-sm text-gray-700">
                      <input type="checkbox" checked={!!form[k as keyof RiskScoreRequest]} onChange={bool(k as keyof RiskScoreRequest)} className={chk} />
                      {l}
                    </label>
                  ))}
                </div>
              </div>
            )}

            <Button onClick={calculate} loading={loading} className="w-full gap-2" size="lg">
              <Calculator size={17} />
              {loading ? 'Calculating…' : 'Calculate All Risk Scores'}
            </Button>

            {error && (
              <div className="flex gap-2 items-center bg-danger-50 border border-danger-500 rounded-xl px-3 py-2.5 text-xs text-danger-700">
                <AlertTriangle size={13} className="shrink-0" />
                {error}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Results */}
        <div className="space-y-4">
          {loading && (
            <div className="flex items-center justify-center py-16">
              <Spinner className="h-8 w-8" />
            </div>
          )}
          {result && !loading && (
            <>
              {/* Overall banner */}
              <div className={`border rounded-xl px-5 py-4 ${RISK_LEVEL_COLORS[result.risk_level]}`}>
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-base">Overall Risk Level</span>
                  <Badge variant={result.risk_level === 'LOW' ? 'success' : result.risk_level === 'MODERATE' ? 'warning' : 'danger'}>
                    {result.risk_level}
                  </Badge>
                </div>
                <p className="text-sm">{result.explanation}</p>
                <p className="text-sm mt-2 font-medium">{result.overall_recommendation}</p>
              </div>

              {/* Individual scores */}
              {result.scores.map((s, i) => <RiskScoreCard key={i} score={s} />)}
            </>
          )}
          {!result && !loading && (
            <div className="flex flex-col items-center justify-center py-20 text-center text-gray-400">
              <Calculator size={40} className="mb-3 text-gray-200" />
              <p className="text-sm">Fill in the patient parameters and click Calculate.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
