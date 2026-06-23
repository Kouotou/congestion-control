import { useState } from 'react'

export default function ForecastPanel() {
  const [input, setInput] = useState({
    concurrent_users: 120,
    requests_per_second: 15,
    traffic_volume_mb: 40,
    network_utilization: 65,
  })
  const [forecast, setForecast] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function fetchForecast() {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('/api/forecast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      })
      if (!response.ok) {
        throw new Error(`Forecast request failed: ${response.status}`)
      }
      const data = await response.json()
      setForecast(data)
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
          <h2 className="text-2xl font-semibold text-slate-900">Traffic Forecasting</h2>
          <p className="mt-2 text-slate-600">Create short-term traffic forecasts from current network KPIs.</p>
        </div>
        <button
          type="button"
          className="inline-flex items-center rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
          onClick={fetchForecast}
        >
          Run Forecast
        </button>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {[
          { label: 'Concurrent Users', name: 'concurrent_users', type: 'number' },
          { label: 'Requests / sec', name: 'requests_per_second', type: 'number' },
          { label: 'Traffic Volume (MB)', name: 'traffic_volume_mb', type: 'number' },
          { label: 'Network Utilization (%)', name: 'network_utilization', type: 'number' },
        ].map((field) => (
          <label key={field.name} className="block rounded-2xl border border-slate-200 bg-slate-50 p-4">
            <span className="text-sm font-medium text-slate-700">{field.label}</span>
            <input
              type={field.type}
              value={input[field.name]}
              onChange={(e) => setInput({ ...input, [field.name]: Number(e.target.value) })}
              className="mt-2 w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-slate-900 outline-none focus:border-slate-500"
            />
          </label>
        ))}
      </div>

      {loading && <p className="mt-6 text-slate-700">Running forecast...</p>}
      {error && <p className="mt-6 text-red-600">{error}</p>}
      {forecast && (
        <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <h3 className="text-xl font-semibold text-slate-900">Forecast Results</h3>
          <div className="mt-4 grid gap-4 text-slate-700 sm:grid-cols-2">
            {forecast.map((item) => (
              <div key={item.horizon_minutes} className="rounded-2xl bg-white p-4 shadow-sm">
                <div className="text-sm font-medium text-slate-500">Horizon</div>
                <div className="mt-1 text-xl font-semibold text-slate-900">{item.horizon_minutes} min</div>
                <div className="mt-2 text-sm text-slate-700">Users: {item.predicted_concurrent_users}</div>
                <div className="text-sm text-slate-700">RPS: {item.predicted_requests_per_second}</div>
                <div className="text-sm text-slate-700">Utilization: {item.predicted_network_utilization}%</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  )
}
