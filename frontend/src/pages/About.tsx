import { Shield, Layers, Bot, FlaskConical, BarChart3 } from 'lucide-react'
import { Card, CardContent } from '../components/ui/Card'
import { Badge } from '../components/ui/Badge'

const FEATURES = [
  { icon: Bot, title: 'RAG Chat', desc: 'Gemini 2.5 Flash + ChromaDB retrieval over clinical guidelines. Fallback warning when no evidence found.' },
  { icon: FlaskConical, title: 'Lab Parser', desc: 'AI-powered PDF parsing with regex + OCR. Extracts troponin, LDL, HDL, glucose, eGFR, BNP.' },
  { icon: BarChart3, title: 'Risk Dashboard', desc: 'ASCVD (Pooled Cohort), CHA₂DS₂-VASc, HAS-BLED, and GRACE scores with colour-coded risk bars.' },
  { icon: Layers, title: 'Explainability', desc: 'Full reasoning chain: retrieved documents, relevance scores, and step-by-step clinical rationale.' },
]

const STACK = [
  { label: 'Frontend', value: 'React 19 · TypeScript · Tailwind CSS · Vite' },
  { label: 'Backend', value: 'FastAPI · Python 3.11+' },
  { label: 'AI / RAG', value: 'LangChain · ChromaDB · sentence-transformers' },
  { label: 'LLM', value: 'Google Gemini 2.5 Flash' },
]

export default function About() {
  return (
    <div className="flex flex-col h-screen overflow-y-auto">
      <div className="px-6 py-4 border-b border-gray-100 bg-white shrink-0">
        <h1 className="text-lg font-semibold text-gray-900">About BeatBound</h1>
        <p className="text-xs text-gray-500">RAG-Based Multimodal Cardiac Decision Support System</p>
      </div>

      <div className="flex-1 p-6 max-w-3xl mx-auto w-full space-y-8">
        {/* Hero */}
        <div className="text-center py-8">
          <div className="w-20 h-20 rounded-3xl bg-primary-50 border border-primary-100 flex items-center justify-center mx-auto mb-4">
            <span className="text-4xl">🫀</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">BeatBound DSS</h2>
          <p className="text-sm text-gray-500 max-w-md mx-auto leading-relaxed">
            A production-grade cardiac decision support system combining retrieval-augmented generation,
            multimodal lab parsing, and evidence-based risk calculators.
          </p>
          <div className="flex justify-center gap-2 mt-4">
            <Badge variant="info">v3.0.0</Badge>
            <Badge variant="success">Production Ready</Badge>
          </div>
        </div>

        {/* Features */}
        <section>
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">Core Features</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <Card key={title}>
                <CardContent className="pt-4">
                  <div className="flex gap-3">
                    <div className="w-9 h-9 rounded-xl bg-primary-50 flex items-center justify-center shrink-0">
                      <Icon size={18} className="text-primary-600" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-gray-900 mb-0.5">{title}</p>
                      <p className="text-xs text-gray-500 leading-relaxed">{desc}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Tech stack */}
        <section>
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">Technology Stack</h3>
          <Card>
            <CardContent className="pt-4 divide-y divide-gray-100">
              {STACK.map(({ label, value }) => (
                <div key={label} className="flex justify-between py-2.5 text-sm first:pt-0 last:pb-0">
                  <span className="text-gray-500 font-medium">{label}</span>
                  <span className="text-gray-800 text-right max-w-xs">{value}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </section>

        {/* Disclaimer */}
        <Card>
          <CardContent className="pt-4">
            <div className="flex gap-3">
              <Shield size={20} className="text-warning-500 shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-semibold text-gray-800 mb-1">Medical Disclaimer</p>
                <p className="text-xs text-gray-500 leading-relaxed">
                  BeatBound is an educational and research tool. It does not constitute medical advice,
                  diagnosis, or treatment. Always consult a qualified healthcare professional for medical decisions.
                  In emergencies, call 911 immediately.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <p className="text-center text-xs text-gray-400 pb-4">
          Designed by <span className="font-medium text-gray-600">Ayush Sharma &amp; Janvi Chauhan</span>
        </p>
      </div>
    </div>
  )
}
