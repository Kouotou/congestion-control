import Head from 'next/head'

export default function Home() {
  return (
    <>
      <Head>
        <title>AI Traffic Control Dashboard</title>
        <meta name="description" content="Decision support dashboard for flash crowd traffic control" />
      </Head>
      <main className="min-h-screen bg-slate-100 text-slate-900">
        <div className="mx-auto max-w-6xl py-16 px-6">
          <h1 className="text-4xl font-semibold">AI-Driven Traffic Control Dashboard</h1>
          <p className="mt-4 text-lg text-slate-700">
            A prototype interface for traffic forecasting, congestion detection, QoE prediction, and QoS recommendations.
          </p>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
            {[
              'Dataset Explorer',
              'KPI Monitoring',
              'Traffic Forecasting',
              'Congestion Detection',
              'Resource Allocation',
              'QoE Prediction',
              'QoS Recommendation',
              'What-If Simulator',
              'Model Comparison',
            ].map((card) => (
              <div key={card} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-slate-900">{card}</h2>
                <p className="mt-3 text-slate-600">Interactive module under development.</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </>
  )
}
