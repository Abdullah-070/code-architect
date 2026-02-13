import axios from "axios"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

export async function analyzeRepository(data: {
  repository_url: string
  branch?: string
  focus_areas?: string[]
  depth?: number
}) {
  const response = await api.post("/api/gemini/analyze", data)
  return response.data
}

export async function getAnalysisStatus(analysisId: string) {
  const response = await api.get(`/api/gemini/analyze/${analysisId}`)
  return response.data
}

export async function healthCheck() {
  const response = await api.get("/health")
  return response.data
}
