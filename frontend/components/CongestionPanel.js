import { useState } from 'react'

export default function CongestionPanel() {
  const [input, setInput] = useState({
    concurrent_users: 120,
    requests_per_second: 15,
    traffic_volume_mb: 40,
    network_utilization: 65,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function fetchCongestion() {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/api/congestion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      })
      if (!response.ok) {
        throw new Error(`Congestion request failed: ${response.status}`)
      }
      setResult(await response.json())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">Congestion Detection</h2>
          <p className="mt-2 text-slate-600">Estimate the current congestion risk level for the network.</p>
        </div>
        <button
          type="button"
          className="inline-flex items-center rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
          onClick={fetchCongestion}
        >
          Evaluate
        </button>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {[
          { label: 'Concurrent Users', name: 'concurrent_users' },
          { label: 'Requests / sec', name: 'requests_per_second' },
          { label: 'Traffic Volume (MB)', name: 'traffic_volume_mb' },
          { label: 'Network Utilization (%)', name: 'network_utilization' },
        ].map((field) => (
          <label key={field.name} className="block rounded-2xl border border-slate-200 bg-slate-50 p-4">
            <span className="text-sm font-medium text-slate-700">{field.label}</span>
            <input
              type="number"
              value={input[field.name]}
              onChange={(e) => setInput({ ...input, [field.name]: Number(e.target.value) })}
              className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-slate-900 outline-none focus:border-slate-500"
            />
          </label>
        ))}
      </div>

      {loading && <p className="mt-6 text-slate-700">Evaluating congestion...</p>}
      {error && <p className="mt-6 text-red-600">{error}</p>}
      {result && (
        <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h3 className="text-xl font-semibold text-slate-900">Congestion Result</h3>
          <p className="mt-4 text-slate-700">State: <span className="font-semibold">{result.state}</span></p>
          <p className="text-slate-700">Probability: <span className="font-semibold">{result.probability}</span></p>
        </div>
      )}
    </section>
  )
}
