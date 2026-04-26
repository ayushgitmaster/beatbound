import { useState, useRef, useEffect } from 'react'
import { Send, Mic, MicOff, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react'
import { chat } from '../api'
import type { HistoryMessage, ChatResponse, Source } from '../types'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'
import { Spinner } from '../components/ui/Spinner'
import { cn, confColor } from '../lib/utils'
import { EcgLine } from '../components/EcgLine'

/** Minimal anatomical heart SVG used as the AI avatar */
function HeartAvatar({ size = 32, className = '' }: { size?: number; className?: string }) {
  return (
    <div
      className={`rounded-full bg-primary-600 flex items-center justify-center shrink-0 ${className}`}
      style={{ width: size, height: size }}
    >
      <svg viewBox="0 0 24 24" width={size * 0.55} height={size * 0.55} fill="white">
        <path d="M12 21.593c-5.63-5.539-11-10.297-11-14.402 0-3.791 3.068-5.191 5.281-5.191 1.312 0 4.151.501 5.719 4.457 1.59-3.968 4.464-4.447 5.726-4.447 2.54 0 5.274 1.621 5.274 5.181 0 4.069-5.136 8.625-11 14.402z" />
      </svg>
    </div>
  )
}

interface Message {
  role: 'user' | 'assistant'
  content: string
  response?: ChatResponse
}

function SourceCard({ source }: { source: Source }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="text-xs border border-gray-100 rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-3 py-2 bg-gray-50 hover:bg-gray-100 transition-colors text-left gap-2"
      >
        <span className="font-medium text-gray-700 truncate">{source.source}</span>
        <span className="flex items-center gap-1.5 shrink-0">
          <span className={cn('font-semibold', confColor(source.relevance_score))}>
            {(source.relevance_score * 100).toFixed(0)}%
          </span>
          {open ? <ChevronUp size={12} className="text-gray-400" /> : <ChevronDown size={12} className="text-gray-400" />}
        </span>
      </button>
      {open && (
        <div className="px-3 py-2.5 bg-white text-gray-600 leading-relaxed border-t border-gray-100 animate-fade-in">
          {source.content}
          {source.page != null && <span className="ml-1 text-gray-400">(p.{source.page})</span>}
        </div>
      )}
    </div>
  )
}

function AssistantBubble({ msg }: { msg: Message }) {
  const [showSources, setShowSources] = useState(false)
  const r = msg.response
  const hasSources = r && r.sources.length > 0
  const avgScore = hasSources
    ? r!.relevance_scores.reduce((a, b) => a + b, 0) / r!.relevance_scores.length
    : 0

  return (
    <div className="flex gap-3 animate-slide-up">
      <HeartAvatar size={32} className="mt-1" />
      <div className="max-w-[80%] space-y-2">
        {r?.is_fallback && (
          <div className="flex gap-2 items-start bg-warning-50 border border-warning-500 rounded-xl px-3 py-2 text-xs text-warning-600">
            <AlertTriangle size={13} className="shrink-0 mt-0.5" />
            <span>{r.fallback_warning}</span>
          </div>
        )}
        <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
          <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">{msg.content}</p>
        </div>
        {hasSources && (
          <div>
            <button
              onClick={() => setShowSources(!showSources)}
              className="text-xs text-primary-600 hover:text-primary-800 font-medium flex items-center gap-1"
            >
              {showSources ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
              {showSources ? 'Hide' : 'Show'} {r!.sources.length} source{r!.sources.length !== 1 ? 's' : ''}
              <span className="text-gray-400 font-normal ml-1">
                · avg {(avgScore * 100).toFixed(0)}% match
              </span>
            </button>
            {showSources && (
              <div className="mt-2 space-y-1.5 animate-fade-in">
                {r!.sources.map((s, i) => <SourceCard key={i} source={s} />)}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

const SUGGESTIONS = [
  'What are the symptoms of a heart attack?',
  'When should I start statin therapy?',
  'Explain the ASCVD risk score',
  'What does troponin elevation mean?',
]

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [voiceMode, setVoiceMode] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const history: HistoryMessage[] = messages.map((m) => ({ role: m.role, content: m.content }))

  const send = async () => {
    const text = input.trim()
    if (!text || loading) return
    setInput('')
    setError('')
    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setLoading(true)
    try {
      const res = await chat(text, history)
      setMessages((prev) => [...prev, { role: 'assistant', content: res.answer, response: res }])
    } catch (e: unknown) {
      const detail = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(detail ?? 'Could not connect to BeatBound server. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <div className="shrink-0 relative border-b border-gray-100">
        <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary-600 rounded-r" />
        <div className="pl-7 pr-6 py-3 bg-white flex items-center justify-between gap-4 overflow-hidden">
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Chat Assistant</h1>
            <p className="text-xs text-gray-500">Powered by Gemini · cardiac knowledge AI</p>
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <EcgLine className="w-36 hidden sm:block" opacity={0.55} />
            <Badge variant="info">AI-Powered</Badge>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-5 ecg-paper">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center py-16 animate-fade-in">
            {/* Anatomical heart illustration */}
            <div className="relative w-20 h-20 mb-5">
              <div className="absolute inset-0 rounded-full bg-primary-50 animate-pulse" />
              <div className="absolute inset-0 flex items-center justify-center">
                <svg viewBox="0 0 64 64" width="52" height="52" fill="none">
                  <path
                    d="M32 56C17 43 6 34 6 22c0-7.7 6.3-14 14-14 4.5 0 8.5 2.2 11 5.7A13.9 13.9 0 0 1 42 8c7.7 0 14 6.3 14 14 0 12-11 21-24 34z"
                    fill="#fecdd3" stroke="#e11d48" strokeWidth="1.5"
                  />
                  <path d="M32 14 Q28 8 24 6" stroke="#e11d48" strokeWidth="1.2" strokeLinecap="round" fill="none" />
                  <path d="M34 14 Q38 8 42 7" stroke="#e11d48" strokeWidth="1.2" strokeLinecap="round" fill="none" />
                  <path d="M32 22 L32 42" stroke="#f43f5e" strokeWidth="0.8" strokeDasharray="2 2" />
                  <path d="M14 36 L18 36 L20 33 L22 25 L24 37 L26 36 L32 36" stroke="#e11d48" strokeWidth="1.2" fill="none" strokeLinecap="round" />
                </svg>
              </div>
            </div>
            <h2 className="text-lg font-semibold text-gray-800 mb-1">BeatBound Cardiac AI</h2>
            <p className="text-sm text-gray-500 max-w-xs">
              Ask me anything about cardiac health, risk factors, medications, or symptoms.
              I reference clinical cardiology guidelines in my answers.
            </p>
            <div className="mt-5 grid grid-cols-2 gap-2 max-w-sm w-full">
              {SUGGESTIONS.map((q) => (
                <button
                  key={q}
                  onClick={() => setInput(q)}
                  className="text-left text-xs bg-white border border-gray-200 text-gray-700 rounded-xl px-3 py-2.5 hover:border-primary-300 hover:bg-primary-50 transition-colors shadow-sm"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m, i) =>
          m.role === 'user' ? (
            <div key={i} className="flex justify-end animate-slide-up">
              <div className="max-w-[70%] bg-primary-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 shadow-sm">
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{m.content}</p>
              </div>
            </div>
          ) : (
            <AssistantBubble key={i} msg={m} />
          )
        )}

        {loading && (
          <div className="flex gap-3 animate-fade-in">
            <HeartAvatar size={32} />
            <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm flex items-center gap-2">
              <Spinner className="h-4 w-4" />
              <span className="text-sm text-gray-500">Retrieving clinical evidence…</span>
            </div>
          </div>
        )}

        {error && (
          <div className="flex gap-2 items-center bg-danger-50 border border-danger-500 rounded-xl px-4 py-3 text-sm text-danger-700 animate-fade-in">
            <AlertTriangle size={16} className="shrink-0" />
            {error}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div className="shrink-0 px-6 py-4 bg-white border-t border-gray-100">
        <div className="flex gap-2 items-end">
          <div className="flex-1">
            <textarea
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKey}
              placeholder="Ask about heart health, medications, or risk factors…"
              className="w-full resize-none rounded-xl border border-gray-300 px-4 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-primary-400 focus:ring-2 focus:ring-primary-100 transition max-h-36 overflow-y-auto"
              style={{ minHeight: '42px' }}
              onInput={(e) => {
                const t = e.target as HTMLTextAreaElement
                t.style.height = 'auto'
                t.style.height = Math.min(t.scrollHeight, 144) + 'px'
              }}
            />
          </div>
          <Button
            variant={voiceMode ? 'secondary' : 'ghost'}
            size="icon"
            onClick={() => setVoiceMode(!voiceMode)}
            title="Voice mode (ElevenLabs placeholder)"
          >
            {voiceMode ? <Mic size={17} className="text-primary-600" /> : <MicOff size={17} className="text-gray-400" />}
          </Button>
          <Button onClick={send} loading={loading} size="icon">
            <Send size={17} />
          </Button>
        </div>
        <p className="text-[10px] text-gray-400 mt-1.5 text-center">
          BeatBound is an AI assistant — not a substitute for professional medical advice.
        </p>
      </div>
    </div>
  )
}
