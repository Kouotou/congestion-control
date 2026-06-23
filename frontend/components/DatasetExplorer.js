import { useEffect, useState } from 'react'

export default function DatasetExplorer() {
  const [datasets, setDatasets] = useState([])
  const [selected, setSelected] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function loadDatasets() {
      try {
        const res = await fetch('/api/datasets')
        if (!res.ok) {
          throw new Error(`Failed to load datasets: ${res.status}`)
        }
        const data = await res.json()
        setDatasets(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    loadDatasets()
  }, [])

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-2xl font-semibold text-slate-900">Dataset Explorer</h2>
      <p className="mt-2 text-slate-600">Browse the platform datasets and inspect schema metadata.</p>

      {loading ? (
        <p className="mt-4 text-slate-700">Loading datasets...</p>
      ) : error ? (
        <p className="mt-4 text-red-600">{error}</p>
      ) : (
        <div className="mt-6 space-y-4">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 text-sm">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-4 py-3 text-left font-medium text-slate-700">Dataset</th>
                  <th className="px-4 py-3 text-left font-medium text-slate-700">Type</th>
                  <th className="px-4 py-3 text-right font-medium text-slate-700">Rows</th>
                  <th className="px-4 py-3 text-right font-medium text-slate-700">Columns</th>
                  <th className="px-4 py-3 text-left font-medium text-slate-700">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 bg-white">
                {datasets.map((dataset) => (
                  <tr key={dataset.dataset_id}>
                    <td className="px-4 py-3 text-slate-900">
                      <div className="font-semibold">{dataset.name}</div>
                      <div className="text-slate-500 text-xs">{dataset.filename}</div>
                    </td>
                    <td className="px-4 py-3 text-slate-700">{dataset.dataset_type}</td>
                    <td className="px-4 py-3 text-right text-slate-700">{dataset.row_count}</td>
                    <td className="px-4 py-3 text-right text-slate-700">{dataset.column_count}</td>
                    <td className="px-4 py-3">
                      <button
                        type="button"
                        className="rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
                        onClick={() => setSelected(dataset)}
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {selected && (
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
              <h3 className="text-xl font-semibold text-slate-900">{selected.name}</h3>
              <p className="mt-2 text-slate-700">{selected.description}</p>
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                <div className="rounded-2xl bg-white p-4 shadow-sm">
                  <div className="text-sm text-slate-500">Dataset ID</div>
                  <div className="mt-1 font-medium text-slate-900">{selected.dataset_id}</div>
                </div>
                <div className="rounded-2xl bg-white p-4 shadow-sm">
                  <div className="text-sm text-slate-500">Columns</div>
                  <div className="mt-1 text-slate-900">{selected.columns.join(', ')}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  )
}
