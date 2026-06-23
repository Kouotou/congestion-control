import { useState } from 'react'

export default function QoSPanel() {
  const [input, setInput] = useState({
    predicted_concurrent_users: 120,
    predicted_requests_per_second: 15,
    expected_session_duration_minutes: 30,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function fetchRecommendation() {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/api/qos/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      })
      if (!response.ok) {
        throw new Error(`QoS recommend request failed: ${response.status}`)
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
          <h2 className="text-2xl font-semibold text-slate-900">QoS Recommendation</h2>
          <p className="mt-2 text-slate-600">Get resource and QoS configuration recommendations for forecast traffic.</p>
        </div>
        <button
          type="button"
          className="inline-flex items-center rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
          onClick={fetchRecommendation}
        >
          Recommend
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

      {loading && <p className="mt-6 text-slate-700">Generating QoS recommendation...</p>}
      {error && <p className="mt-6 text-red-600">{error}</p>}
      {result && (
        <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h3 className="text-xl font-semibold text-slate-900">Recommendation</h3>
          <div className="mt-4 grid gap-3 text-slate-700 sm:grid-cols-2">
            <div>Bandwidth (Gbps): {result.required_bandwidth_gbps}</div>
            <div>Throughput (Mbps): {result.required_throughput_mbps}</div>
            <div>Latency Max (ms): {result.maximum_latency_ms}</div>
            <div>Jitter Max (ms): {result.maximum_jitter_ms}</div>
            <div>Packet Loss Max (%): {result.maximum_packet_loss_pct}</div>
            <div>Recommended Servers: {result.required_servers}</div>
            <div>CPU Target (%): {result.required_cpu_pct}</div>
            <div>Memory Target (GB): {result.required_memory_gb}</div>
          </div>
          <p className="mt-4 text-slate-600">Predicted QoE Score: {result.predicted_qoe_score}</p>
          <p className="mt-2 text-slate-500">{result.notes}</p>
        </div>
      )}
    </section>
  )
}
