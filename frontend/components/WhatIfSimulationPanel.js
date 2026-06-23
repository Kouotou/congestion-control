import { useState } from 'react'

export default function WhatIfSimulationPanel() {
  const [input, setInput] = useState({
    concurrent_users: 80,
    requests_per_second: 20,
    latency_ms: 120,
    jitter_ms: 25,
    packet_loss_pct: 0.4,
    timeout_rate_pct: 1.0,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function submitSimulation() {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/api/what-if', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      })
      if (!response.ok) {
        throw new Error(`Simulation failed: ${response.status}`)
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
          <h2 className="text-2xl font-semibold text-slate-900">What-if Simulation</h2>
          <p className="mt-2 text-slate-600">Explore QoE impact for tuned latency and packet loss scenarios.</p>
        </div>
        <button
          type="button"
          className="inline-flex items-center rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
          onClick={submitSimulation}
        >
          Simulate
        </button>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {[
          { label: 'Concurrent Users', name: 'concurrent_users' },
          { label: 'Requests / sec', name: 'requests_per_second' },
          { label: 'Latency (ms)', name: 'latency_ms' },
          { label: 'Jitter (ms)', name: 'jitter_ms' },
          { label: 'Packet Loss (%)', name: 'packet_loss_pct' },
          { label: 'Timeout Rate (%)', name: 'timeout_rate_pct' },
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

      {loading && <p className="mt-6 text-slate-700">Running simulation...</p>}
      {error && <p className="mt-6 text-red-600">{error}</p>}
      {result && (
        <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h3 className="text-xl font-semibold text-slate-900">Simulation Results</h3>
          <div className="mt-4 grid gap-3 sm:grid-cols-2 text-slate-700">
            <div>Predicted QoE: {result.predicted_qoe_score}</div>
            <div>Bisector Score: {result.qoe_score_description}</div>
            <div>Latency: {result.latency_ms} ms</div>
            <div>Packet Loss: {result.packet_loss_pct}%</div>
            <div>Jitter: {result.jitter_ms} ms</div>
          </div>
          <p className="mt-4 text-slate-600">{result.recommendation}</p>
        </div>
      )}
    </section>
  )
}
