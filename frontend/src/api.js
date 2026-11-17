import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const client = axios.create({ baseURL: BASE_URL })

export async function createJob(source, language) {
  const { data } = await client.post('/api/jobs', { source, language })
  return data.job_id
}

export async function getJobStatus(jobId) {
  const { data } = await client.get(`/api/jobs/${jobId}`)
  return data
}

export async function askQuestion(jobId, question) {
  const { data } = await client.post(`/api/jobs/${jobId}/chat`, { question })
  return data
}
