import { create } from "zustand"

interface AnalysisState {
  analysisId: string | null
  status: string
  findings: Record<string, any> | null
  recommendations: string[]
  setAnalysisId: (id: string) => void
  setStatus: (status: string) => void
  setFindings: (findings: Record<string, any>) => void
  setRecommendations: (recommendations: string[]) => void
  reset: () => void
}

export const useAnalysisStore = create<AnalysisState>((set) => ({
  analysisId: null,
  status: "idle",
  findings: null,
  recommendations: [],
  setAnalysisId: (id) => set({ analysisId: id }),
  setStatus: (status) => set({ status }),
  setFindings: (findings) => set({ findings }),
  setRecommendations: (recommendations) => set({ recommendations }),
  reset: () =>
    set({
      analysisId: null,
      status: "idle",
      findings: null,
      recommendations: [],
    }),
}))
