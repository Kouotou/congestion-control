import { useState } from 'react'

export default function WhatIfPanel() {
  const [input, setInput] = useState({
    concurrent_users: 120,
    requests_per_second: 15,
    traffic_volume_mb: 40,
    network_utilization: 65,
    latency_ms: 80,
    jitter_ms: 15,
    packet_loss_pct: 0.4,
    throughput_mbps: 55,
    response_time_ms: 120,
    timeout_rate_pct: 0.5,
    expected_session_duration_minutes: 30,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function runSimulation() {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/api/what-if', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      })
      if (!response.ok) {
        throw new Error(`What-if request failed: ${response.status}`)
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
          <h2 className="text-2xl font-semibold text-slate-900">What-If Simulator</h2>
          <p className="mt-2 text-slate-600">Run scenario analysis for forecast traffic, congestion, QoE, and QoS.</p>
        </div>
        <button
          type="button"
          className="inline-flex items-center rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
          onClick={runSimulation}
        >
          Simulate
        </button>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {[
          { label: 'Concurrent Users', name: 'concurrent_users' },
          { label: 'Requests / sec', name: 'requests_per_second' },
          { label: 'Traffic Volume (MB)', name: 'traffic_volume_mb' },
          { label: 'Network Utilization (%)', name: 'network_utilization' },
          { label: 'Latency (ms)', name: 'latency_ms' },
          { label: 'Jitter (ms)', name: 'jitter_ms' },
          { label: 'Packet Loss (%)', name: 'packet_loss_pct' },
          { label: 'Throughput (Mbps)', name: 'throughput_mbps' },
          { label: 'Response Time (ms)', name: 'response_time_ms' },
          { label: 'Timeout Rate (%)', name: 'timeout_rate_pct' },
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

      {loading && <p className="mt-6 text-slate-700">Running scenario...</p>}
      {error && <p className="mt-6 text-red-600">{error}</p>}
      {result && (
        <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h3 className="text-xl font-semibold text-slate-900">What-If Results</h3>
          <div className="mt-4 space-y-4 text-slate-700">
            <div>
              <span className="font-semibold">Congestion:</span> {result.congestion.state} ({result.congestion.probability})
            </div>
            <div>
              <span className="font-semibold">QoE Score:</span> {result.qoe.qoe_score} - {result.qoe.satisfaction_level}
            </div>
            <div>
              <span className="font-semibold">Required Bandwidth:</span> {result.qos_recommendation.required_bandwidth_gbps} Gbps
            </div>
            <div>
              <span className="font-semibold">Required Servers:</span> {result.qos_recommendation.required_servers}
            </div>
            <div className="text-sm text-slate-600">Forecast Input: users {result.forecast_input.concurrent_users}, rps {result.forecast_input.requests_per_second}, utilization {result.forecast_input.network_utilization}%</div>
          </div>
        </div>
      )}
    </section>
  )
}
