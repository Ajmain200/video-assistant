import { useState } from 'react'

export default function InputPanel({ onSubmit, disabled }) {
  const [source, setSource] = useState('')
  const [language, setLanguage] = useState('english')

  function handleSubmit(e) {
    e.preventDefault()
    if (!source.trim() || disabled) return
    onSubmit(source.trim(), language)
  }

  return (
    <form onSubmit={handleSubmit} className="bg-surface border border-border rounded-xl p-5 flex flex-col gap-4">
      <div className="flex items-center gap-2">
        <span className="text-[10px] font-bold tracking-widest uppercase px-2 py-1 rounded bg-accent/20 text-accentGlow border border-accent/30">
          Input
        </span>
        <span className="text-textMuted text-xs">Paste a YouTube link to get started</span>
      </div>

      <input
        type="text"
        value={source}
        onChange={(e) => setSource(e.target.value)}
        placeholder="https://youtube.com/watch?v=..."
        disabled={disabled}
        className="w-full bg-surface2 border border-border rounded-lg px-4 py-3 text-sm text-text focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 disabled:opacity-50"
      />

      <div className="flex items-center gap-3">
        <label className="text-xs text-textMuted uppercase tracking-wide">Language</label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          disabled={disabled}
          className="bg-surface2 border border-border rounded-lg px-3 py-2 text-sm text-text focus:outline-none focus:border-accent disabled:opacity-50"
        >
          
          
        </select>
      </div>

      <button
        type="submit"
        disabled={disabled || !source.trim()}
        className="mt-1 bg-gradient-to-br from-accent to-[#5b21b6] text-white font-display font-bold uppercase tracking-wide text-sm py-3 rounded-lg transition-transform hover:-translate-y-0.5 hover:shadow-[0_8px_25px_rgba(124,58,237,0.4)] disabled:opacity-40 disabled:hover:translate-y-0 disabled:hover:shadow-none"
      >
        {disabled ? 'Processing…' : ' Analyse '}
      </button>
    </form>
  )
}
