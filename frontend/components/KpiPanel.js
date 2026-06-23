export default function KpiPanel({ kpis = [] }) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-2xl font-semibold text-slate-900">KPI Monitoring</h2>
      <p className="mt-2 text-slate-600">Monitor the key performance indicators that affect congestion and QoE.</p>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {kpis.map((kpi) => (
          <div key={kpi.name} className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
            <h3 className="text-lg font-semibold text-slate-900">{kpi.name}</h3>
            <p className="mt-2 text-slate-600">{kpi.description}</p>
            <div className="mt-4 grid gap-2 text-sm text-slate-700">
              <div>
                <span className="font-semibold">Acceptable:</span> {kpi.acceptable_range}
              </div>
              <div>
                <span className="font-semibold">Critical:</span> {kpi.critical_threshold}
              </div>
              <div>
                <span className="font-semibold">QoE impact:</span> {kpi.qoe_impact}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
