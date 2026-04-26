import { useState, useRef } from 'react'
import { Upload, FileText, Sparkles, AlertTriangle } from 'lucide-react'
import { uploadReport, labAiAnalysis } from '../api'
import type { LabUploadResponse, SummaryRow } from '../types'
import { Button } from '../components/ui/Button'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card'
import { Badge } from '../components/ui/Badge'
import { EcgLine } from '../components/EcgLine'

function ValueCard({ label, value, normal }: { label: string; value: string; normal: string }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow">
      <p className="text-xs text-gray-500 mb-1">{label}</p>
      <p className="text-xl font-bold text-gray-900">{value || '—'}</p>
      <p className="text-[11px] text-gray-400 mt-1">Normal: {normal}</p>
    </div>
  )
}

function ResultsTable({ rows }: { rows: SummaryRow[] }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200">
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-gray-50 border-b border-gray-200">
            <th className="text-left px-4 py-3 font-medium text-gray-600">Test</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Value</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Normal Range</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {rows.map((r, i) => (
            <tr key={i} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-medium text-gray-900">{r.test}</td>
              <td className="px-4 py-3 text-gray-700">{r.value}</td>
              <td className="px-4 py-3 text-gray-500">{r.normal_range}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function Lab() {
  const [file, setFile] = useState<File | null>(null)
  const [result, setResult] = useState<LabUploadResponse | null>(null)
  const [analysis, setAnalysis] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingAI, setLoadingAI] = useState(false)
  const [error, setError] = useState('')
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = (f: File) => {
    setFile(f)
    setResult(null)
    setAnalysis('')
    setError('')
  }

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  const upload = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const res = await uploadReport(file)
      setResult(res)
    } catch (e: unknown) {
      const detail = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(detail ?? 'Failed to parse the report. Please try a PDF file.')
    } finally {
      setLoading(false)
    }
  }

  const runAI = async () => {
    if (!result?.rag_prompt) return
    setLoadingAI(true)
    try {
      const res = await labAiAnalysis(result.rag_prompt)
      setAnalysis(res.analysis)
    } catch {
      setError('AI analysis failed. Please try again.')
    } finally {
      setLoadingAI(false)
    }
  }

  return (
    <div className="flex flex-col h-screen overflow-y-auto">
      <div className="shrink-0 relative border-b border-gray-100">
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary-600 rounded-r" />
        <div className="pl-7 pr-6 py-3 bg-white flex items-center justify-between gap-4 overflow-hidden">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Upload Lab Report</h1>
            <p className="text-xs text-gray-500">PDF lab reports are parsed automatically using AI-assisted OCR.</p>
          </div>
          <EcgLine className="w-36 hidden sm:block" opacity={0.45} />
        </div>
      </div>

      <div className="flex-1 p-6 space-y-6">
        {/* Upload zone */}
        <Card>
          <CardContent className="pt-5">
            <div
              onDrop={onDrop}
              onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
              onDragLeave={() => setDragging(false)}
              onClick={() => inputRef.current?.click()}
              className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors ${
                dragging ? 'border-primary-400 bg-primary-50' : 'border-gray-200 hover:border-primary-300 hover:bg-gray-50'
              }`}
            >
              <Upload size={32} className="mx-auto mb-3 text-gray-300" />
              <p className="text-sm font-medium text-gray-700 mb-1">
                {file ? file.name : 'Drop your lab report here'}
              </p>
              <p className="text-xs text-gray-400">
                {file ? `${(file.size / 1024).toFixed(1)} KB` : 'PDF or image · max 20 MB'}
              </p>
              <input
                ref={inputRef}
                type="file"
                accept=".pdf,image/*"
                className="hidden"
                onChange={(e) => { if (e.target.files?.[0]) handleFile(e.target.files[0]) }}
              />
            </div>
            {file && (
              <div className="mt-4 flex justify-center">
                <Button onClick={upload} loading={loading} className="gap-2">
                  <FileText size={16} />
                  {loading ? 'Parsing…' : 'Parse Report'}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {error && (
          <div className="flex gap-2 items-center bg-danger-50 border border-danger-500 rounded-xl px-4 py-3 text-sm text-danger-700">
            <AlertTriangle size={16} className="shrink-0" />
            {error}
          </div>
        )}

        {/* Extracted values */}
        {result && result.summary_table.length > 0 && (
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Extracted Lab Values</CardTitle>
                <Badge variant="success">{result.summary_table.length} values found</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-4">
                {result.summary_table.slice(0, 6).map((r) => (
                  <ValueCard key={r.test} label={r.test} value={r.value} normal={r.normal_range} />
                ))}
              </div>
              <ResultsTable rows={result.summary_table} />
              <div className="mt-4 flex justify-end">
                <Button variant="secondary" onClick={runAI} loading={loadingAI} className="gap-2">
                  <Sparkles size={15} />
                  {loadingAI ? 'Analysing…' : 'Get AI Clinical Analysis'}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {result && result.summary_table.length === 0 && !loading && (
          <Card>
            <CardContent className="pt-5 text-center py-10">
              <p className="text-sm text-gray-500">No recognised cardiovascular values were found in this document.</p>
              <p className="text-xs text-gray-400 mt-1">Try uploading a PDF with troponin, cholesterol, or glucose values.</p>
            </CardContent>
          </Card>
        )}

        {/* AI Analysis */}
        {analysis && (
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Sparkles size={16} className="text-primary-600" />
                <CardTitle>AI Clinical Analysis</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <div className="bg-primary-50 rounded-xl p-4 text-sm text-gray-800 leading-relaxed whitespace-pre-wrap border border-primary-100">
                {analysis}
              </div>
              <p className="text-xs text-gray-400 mt-3">
                ⚕️ This analysis is AI-generated. Always have results reviewed by a qualified physician.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
