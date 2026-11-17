function Card({ title, children, className = '' }) {
  return (
    <div className={`relative bg-surface border border-border rounded-xl p-5 overflow-hidden hover:border-accent transition-colors ${className}`}>
      <div className="absolute top-0 left-0 w-[3px] h-full bg-gradient-to-b from-accent to-accent2" />
      <div className="text-[11px] font-bold tracking-widest uppercase text-textMuted mb-3">{title}</div>
      <div className="text-sm leading-relaxed text-text">{children}</div>
    </div>
  )
}

function ListCard({ title, items }) {
  return (
    <Card title={title}>
      {items && items.length > 0 ? (
        <ul className="space-y-2 list-disc list-inside marker:text-accentGlow">
          {items.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      ) : (
        <span className="text-textMuted">None found.</span>
      )}
    </Card>
  )
}

export default function ResultsView({ result }) {
  if (!result) return null

  return (
    <div className="flex flex-col gap-4">
      <Card title=" Session Title">
        <div className="font-display text-xl font-bold text-text">{result.title}</div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
        <Card title=" Summary" className="lg:col-span-3">
          <div className="whitespace-pre-wrap">{result.summary}</div>
        </Card>

        <Card title=" Transcript" className="lg:col-span-2">
          <div className="max-h-72 overflow-y-auto whitespace-pre-wrap text-xs text-textMuted leading-relaxed">
            {result.transcript}
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ListCard title=" Action Items" items={result.action_items} />
        <ListCard title=" Key Decisions" items={result.key_decisions} />
        <ListCard title=" Open Questions" items={result.open_questions} />
      </div>
    </div>
  )
}
