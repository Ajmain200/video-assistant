import { useState, useRef, useEffect } from 'react'
import { askQuestion } from '../api'

export default function ChatPanel({ jobId, ready }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [thinking, setThinking] = useState(false)
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, thinking])

  async function handleSend(e) {
    e.preventDefault()
    const question = input.trim()
    if (!question || thinking || !ready) return

    setMessages((m) => [...m, { role: 'user', content: question }])
    setInput('')
    setThinking(true)

    try {
      const { answer } = await askQuestion(jobId, question)
      setMessages((m) => [...m, { role: 'assistant', content: answer }])
    } catch (err) {
      const detail = err?.response?.data?.detail || 'Something went wrong answering that.'
      setMessages((m) => [...m, { role: 'assistant', content: ` ${detail}` }])
    } finally {
      setThinking(false)
    }
  }

  return (
    <div className="bg-surface border border-border rounded-xl p-5 flex flex-col gap-4">
      <div className="font-display text-lg font-bold"> Chat with your video</div>

      <div ref={scrollRef} className="bg-surface2 border border-border rounded-lg p-4 max-h-96 overflow-y-auto flex flex-col gap-3">
        {messages.length === 0 && (
          <div className="text-center text-textMuted text-sm py-8">
            {ready ? 'Ask anything about the video transcript.' : 'The chat unlocks once indexing is complete.'}
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`flex flex-col gap-1 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
            <span className={`text-[10px] font-bold tracking-widest uppercase ${msg.role === 'user' ? 'text-accentGlow' : 'text-accent2'}`}>
              {msg.role === 'user' ? 'You' : 'Assistant'}
            </span>
            <div
              className={`px-4 py-2 rounded-xl text-sm leading-relaxed max-w-[90%] whitespace-pre-wrap ${
                msg.role === 'user'
                  ? 'bg-accent/15 border border-accent/25'
                  : 'bg-accent2/10 border border-accent2/20'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {thinking && <div className="text-xs text-textMuted">Thinking…</div>}
      </div>

      <form onSubmit={handleSend} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={ready ? 'What were the main decisions made?' : 'Waiting for indexing to finish…'}
          disabled={!ready || thinking}
          className="flex-1 bg-surface2 border border-border rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-accent disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!ready || thinking || !input.trim()}
          className="bg-gradient-to-br from-accent to-[#5b21b6] text-white font-display font-bold text-sm px-5 rounded-lg disabled:opacity-40"
        >
          Send 
        </button>
      </form>
    </div>
  )
}
