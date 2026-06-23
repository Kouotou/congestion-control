import { useState } from 'react'

export default function ResourceAllocationPanel() {
  const [input, setInput] = useState({
    predicted_concurrent_users: 120,
    predicted_requests_per_second: 15,
    expected_session_duration_minutes: 30,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function fetchAllocation() {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/api/resource-allocation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      })
      if (!response.ok) {
        throw new Error(`Resource allocation failed: ${response.status}`)
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
          <h2 className="text-2xl font-semibold text-slate-900">Resource Allocation</h2>
          <p className="mt-2 text-slate-600">Calculate server, CPU and memory resources for forecast demand.</p>
        </div>
        <button
          type="button"
          className="inline-flex items-center rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
          onClick={fetchAllocation}
        >
          Estimate
        </button>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {[
          { label: 'Predicted Users', name: 'predicted_concurrent_users' },
          { label: 'Predicted Requests / sec', name: 'predicted_requests_per_second' },
          { label: 'Session Duration (min)', name: 'expected_session_duration_minutes' },
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

      {loading && <p className="mt-6 text-slate-700">Estimating resources...</p>}
      {error && <p className="mt-6 text-red-600">{error}</p>}
      {result && (
        <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h3 className="text-xl font-semibold text-slate-900">Allocation Estimate</h3>
          <div className="mt-4 grid gap-3 text-slate-700 sm:grid-cols-2">
            <div>Servers: {result.required_servers}</div>
            <div>CPU target: {result.required_cpu_pct}%</div>
            <div>Memory target: {result.required_memory_gb} GB</div>
            <div>Bandwidth: {result.required_bandwidth_gbps} Gbps</div>
            <div>Throughput: {result.required_throughput_mbps} Mbps</div>
            <div>Latency target: {result.latency_target_ms} ms</div>
          </div>
          <p className="mt-4 text-slate-600">{result.notes}</p>
        </div>
      )}
    </section>
  )
}
