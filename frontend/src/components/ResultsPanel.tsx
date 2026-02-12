export default function ResultsPanel({
  status,
  findings,
  recommendations,
}: {
  status: string
  findings: Record<string, any> | null
  recommendations: string[]
}) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>

        {/* Status */}
        <div className="bg-slate-800 p-4 rounded-lg mb-4">
          <p className="text-sm text-slate-400">Status</p>
          <p className="text-lg font-semibold capitalize text-blue-400">{status}</p>
        </div>

        {/* Findings */}
        {findings && (
          <div className="bg-slate-800 p-4 rounded-lg mb-4">
            <h3 className="text-lg font-semibold mb-3">Findings</h3>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {Object.entries(findings).map(([key, value]) => (
                <details key={key} className="bg-slate-700 p-3 rounded cursor-pointer">
                  <summary className="font-medium hover:text-blue-400">
                    {key.replace(/_/g, " ").toUpperCase()}
                  </summary>
                  <pre className="mt-2 text-xs bg-slate-900 p-2 rounded overflow-x-auto">
                    {typeof value === "string" ? value : JSON.stringify(value, null, 2)}
                  </pre>
                </details>
              ))}
            </div>
          </div>
        )}

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <div className="bg-slate-800 p-4 rounded-lg">
            <h3 className="text-lg font-semibold mb-3">Recommendations</h3>
            <ul className="space-y-2">
              {recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-green-400 mt-1">✓</span>
                  <span className="text-sm">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
