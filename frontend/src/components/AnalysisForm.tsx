export default function AnalysisForm({
  onSubmit,
  isLoading,
}: {
  onSubmit: (data: any) => void
  isLoading: boolean
}) {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const data = {
      repository_url: formData.get("repository_url"),
      branch: formData.get("branch") || "main",
      focus_areas: (formData.get("focus_areas") as string)
        ?.split(",")
        .map((s) => s.trim())
        .filter(Boolean) || ["architecture", "performance", "security"],
      depth: parseInt(formData.get("depth") as string) || 3,
    }
    onSubmit(data)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="repository_url" className="block text-sm font-medium mb-2">
          Repository URL
        </label>
        <input
          type="text"
          id="repository_url"
          name="repository_url"
          placeholder="https://github.com/user/repo"
          required
          disabled={isLoading}
          className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label htmlFor="branch" className="block text-sm font-medium mb-2">
          Branch
        </label>
        <input
          type="text"
          id="branch"
          name="branch"
          placeholder="main"
          disabled={isLoading}
          className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label htmlFor="focus_areas" className="block text-sm font-medium mb-2">
          Focus Areas (comma-separated)
        </label>
        <input
          type="text"
          id="focus_areas"
          name="focus_areas"
          placeholder="architecture, performance, security"
          disabled={isLoading}
          className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label htmlFor="depth" className="block text-sm font-medium mb-2">
          Analysis Depth (1-5)
        </label>
        <input
          type="number"
          id="depth"
          name="depth"
          min="1"
          max="5"
          defaultValue="3"
          disabled={isLoading}
          className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white font-semibold rounded-lg transition-colors"
      >
        {isLoading ? "Analyzing..." : "Start Analysis"}
      </button>
    </form>
  )
}
