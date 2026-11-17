const STEP_LABELS = [
  { key: 'audio', label: 'Audio Processing' },
  { key: 'transcript', label: 'Transcription' },
  { key: 'title', label: 'Title Generation' },
  { key: 'summary', label: 'Summarisation' },
  { key: 'extract', label: 'Extraction' },
  { key: 'rag', label: 'RAG Indexing' },
]

function dotClass(state) {
  if (state === 'active') return 'bg-accentGlow shadow-[0_0_8px_#9f67ff] dot-active'
  if (state === 'done') return 'bg-success'
  return 'bg-border'
}

export default function PipelineStatus({ steps, error }) {
  return (
    <div className="bg-surface border border-border rounded-xl p-5 flex flex-col gap-2">
      <span className="text-[10px] font-bold tracking-widest uppercase px-2 py-1 rounded bg-success/15 text-success border border-success/30 w-fit mb-1">
        Pipeline Status
      </span>
      {STEP_LABELS.map(({ key, icon, label }) => (
        <div key={key} className="flex items-center gap-3 px-3 py-2 bg-surface2 border border-border rounded-lg text-xs">
          <div className={`w-2 h-2 rounded-full flex-shrink-0 ${dotClass(steps?.[key])}`} />
          <span>{icon} {label}</span>
        </div>
      ))}
      {error && (
        <div className="mt-2 text-xs text-danger bg-danger/10 border border-danger/30 rounded-lg px-3 py-2">
           {error}
        </div>
      )}
    </div>
  )
}
