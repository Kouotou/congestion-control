import { useState } from 'react'

export default function QoEPanel() {
  const [input, setInput] = useState({
    latency_ms: 80,
    jitter_ms: 15,
    packet_loss_pct: 0.4,
    throughput_mbps: 55,
    response_time_ms: 120,
    timeout_rate_pct: 0.5,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function fetchQoE() {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/api/qoe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      })
      if (!response.ok) {
        throw new Error(`QoE request failed: ${response.status}`)
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
          <h2 className="text-2xl font-semibold text-slate-900">QoE Prediction</h2>
          <p className="mt-2 text-slate-600">Estimate overall user experience quality from QoS metrics.</p>
        </div>
        <button
          type="button"
          className="inline-flex items-center rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
          onClick={fetchQoE}
        >
          Predict QoE
        </button>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {[
          { label: 'Latency (ms)', name: 'latency_ms' },
          { label: 'Jitter (ms)', name: 'jitter_ms' },
          { label: 'Packet Loss (%)', name: 'packet_loss_pct' },
          { label: 'Throughput (Mbps)', name: 'throughput_mbps' },
          { label: 'Response Time (ms)', name: 'response_time_ms' },
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

      {loading && <p className="mt-6 text-slate-700">Predicting QoE...</p>}
      {error && <p className="mt-6 text-red-600">{error}</p>}
      {result && (
        <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h3 className="text-xl font-semibold text-slate-900">QoE Result</h3>
          <p className="mt-4 text-slate-700">Score: <span className="font-semibold">{result.qoe_score}</span></p>
          <p className="text-slate-700">Satisfaction: <span className="font-semibold">{result.satisfaction_level}</span></p>
        </div>
      )}
    </section>
  )
}
