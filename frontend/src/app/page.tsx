'use client'

import { useState, useEffect } from 'react'
import AnalysisForm from '@/components/AnalysisForm'
import ResultsPanel from '@/components/ResultsPanel'
import { analyzeRepository, getAnalysisStatus, healthCheck } from '@/lib/api'
import { useAnalysisStore } from '@/lib/store'

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [pollInterval, setPollInterval] = useState<NodeJS.Timeout | null>(null)
  
  const {
    analysisId,
    status,
    findings,
    recommendations,
    setAnalysisId,
    setStatus,
    setFindings,
    setRecommendations,
    reset,
  } = useAnalysisStore()

  useEffect(() => {
    // Health check on mount
    healthCheck().catch(() => {
      setError('Backend API is not available. Make sure the server is running.')
    })
  }, [])

  useEffect(() => {
    if (analysisId && status === 'analyzing') {
      const interval = setInterval(async () => {
        try {
          const result = await getAnalysisStatus(analysisId)
          setStatus(result.status)
          if (result.findings) setFindings(result.findings)
          if (result.recommendations) setRecommendations(result.recommendations)
          
          if (result.status === 'completed' || result.status === 'failed') {
            clearInterval(interval)
          }
        } catch (err) {
          console.error('Failed to poll analysis status:', err)
        }
      }, 3000) // Poll every 3 seconds
      
      setPollInterval(interval)
      return () => clearInterval(interval)
    }
  }, [analysisId, status])

  const handleSubmit = async (data: any) => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await analyzeRepository(data)
      setAnalysisId(response.analysis_id)
      setStatus(response.status)
    } catch (err: any) {
      setError(err.message || 'Failed to start analysis')
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    reset()
    setError(null)
    if (pollInterval) clearInterval(pollInterval)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            🏗️ Code Architect
          </h1>
          <p className="text-slate-400">
            Autonomous code analysis powered by Gemini 3 Pro
          </p>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="bg-red-900/30 border border-red-700 text-red-200 p-4 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Panel */}
          <div className="bg-slate-800/50 backdrop-blur border border-slate-700 p-6 rounded-lg">
            <h2 className="text-xl font-bold mb-4">Start Analysis</h2>
            <AnalysisForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>

          {/* Results Panel */}
          <div className="bg-slate-800/50 backdrop-blur border border-slate-700 p-6 rounded-lg">
            {analysisId ? (
              <>
                <ResultsPanel
                  status={status}
                  findings={findings}
                  recommendations={recommendations}
                />
                <button
                  onClick={handleReset}
                  className="mt-6 w-full px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-lg transition-colors"
                >
                  Start New Analysis
                </button>
              </>
            ) : (
              <div className="flex items-center justify-center h-full min-h-96 text-slate-500">
                <p>Submit a repository URL to start analysis</p>
              </div>
            )}
          </div>
        </div>

        {/* Info Box */}
        <div className="mt-8 bg-blue-900/20 border border-blue-700/50 p-4 rounded-lg text-blue-200">
          <p className="text-sm">
            <strong>About:</strong> This system uses Gemini 3 Pro with Marathon Agent capabilities
            to autonomously analyze code repositories across multiple iterations, providing architecture
            insights, performance recommendations, and security analysis.
          </p>
        </div>
      </div>
    </main>
  )
}
