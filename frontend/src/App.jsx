import { useEffect, useRef, useState } from 'react'
import InputPanel from './components/InputPanel'
import PipelineStatus from './components/PipelineStatus'
import ResultsView from './components/ResultsView'
import ChatPanel from './components/ChatPanel'
import { createJob, getJobStatus } from './api'

export default function App() {
  const [jobId, setJobId] = useState(null)
  const [status, setStatus] = useState(null) 
  const [submitError, setSubmitError] = useState(null)
  const pollRef = useRef(null)

  const isProcessing = status && status.status !== 'done' && status.status !== 'error'

  useEffect(() => {
    return () => clearInterval(pollRef.current)
  }, [])

  async function handleSubmit(source, language) {
    setSubmitError(null)
    setStatus(null)
    clearInterval(pollRef.current)

    try {
      const id = await createJob(source, language)
      setJobId(id)

      pollRef.current = setInterval(async () => {
        try {
          const data = await getJobStatus(id)
          setStatus(data)
          if (data.status === 'done' || data.status === 'error') {
            clearInterval(pollRef.current)
          }
        } catch (err) {
          clearInterval(pollRef.current)
          setSubmitError('Lost connection to the job — is the backend running?')
        }
      }, 2000)
    } catch (err) {
      setSubmitError(err?.response?.data?.detail || 'Could not start the job — is the backend running?')
    }
  }

  return (
    <div className="min-h-screen bg-bg bg-grid bg-grid relative">
      <div className="max-w-6xl mx-auto px-6 py-10 flex flex-col gap-8">
        <header>
          <h1 className="font-display text-4xl md:text-5xl font-extrabold bg-gradient-to-br from-white via-accentGlow to-accent2 bg-clip-text text-transparent">
            AI Video Assistant
          </h1>
          <p className="text-textMuted text-xs uppercase tracking-[0.2em] mt-2">
            Transcribe · Summarise · Chat with your videos
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 flex flex-col gap-4">
            <InputPanel onSubmit={handleSubmit} disabled={isProcessing} />
            {submitError && (
              <div className="text-xs text-danger bg-danger/10 border border-danger/30 rounded-lg px-3 py-2">
                {submitError}
              </div>
            )}
            {status && <PipelineStatus steps={status.steps} error={status.status === 'error' ? status.error : null} />}
          </div>

          <div className="lg:col-span-2 flex flex-col gap-6">
            {status?.status === 'done' && status.result ? (
              <>
                <ResultsView result={status.result} />
                <ChatPanel jobId={jobId} ready={status.steps.rag === 'done'} />
              </>
            ) : (
              <div className="flex flex-col items-center justify-center text-center py-20 px-6 border border-dashed border-border rounded-xl">
                <div className="text-5xl mb-4"></div>
                <div className="font-display text-2xl font-bold mb-2">
                  {isProcessing ? 'Working on it…' : 'Ready to Analyse'}
                </div>
                <p className="text-textMuted text-sm max-w-sm leading-relaxed">
                  {isProcessing
                    ? 'This can take a few minutes depending on video length — track progress in the sidebar.'
                    : 'Paste a YouTube URL, choose your language, and hit Analyse to get started.'}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
