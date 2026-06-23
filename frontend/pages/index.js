import Head from 'next/head'
import { useState, useEffect } from 'react'
import DatasetExplorer from '../components/DatasetExplorer'
import KpiPanel from '../components/KpiPanel'
import ForecastPanel from '../components/ForecastPanel'
import CongestionPanel from '../components/CongestionPanel'
import QoEPanel from '../components/QoEPanel'
import QoSPanel from '../components/QoSPanel'
import ResourceAllocationPanel from '../components/ResourceAllocationPanel'
import WhatIfPanel from '../components/WhatIfPanel'

export default function Home() {
  const [kpis, setKpis] = useState([])
  const [loadingKpis, setLoadingKpis] = useState(true)
  const [kpiError, setKpiError] = useState(null)

  useEffect(() => {
    async function fetchKpis() {
      try {
        const res = await fetch('/api/kpis')
        if (!res.ok) {
          throw new Error(`Failed to load KPIs: ${res.status}`)
        }
        setKpis(await res.json())
      } catch (err) {
        setKpiError(err.message)
      } finally {
        setLoadingKpis(false)
      }
    }
    fetchKpis()
  }, [])

  return (
    <>
      <Head>
        <title>AI Traffic Control Dashboard</title>
        <meta name="description" content="Decision support dashboard for flash crowd traffic control" />
      </Head>
      <main className="min-h-screen bg-slate-100 text-slate-900">
        <div className="mx-auto max-w-7xl py-16 px-6">
          <div className="mb-10">
            <h1 className="text-4xl font-semibold">AI-Driven Traffic Control Dashboard</h1>
            <p className="mt-4 max-w-2xl text-lg text-slate-700">
              A working interface for dataset exploration, KPI monitoring, traffic forecasting, congestion detection, QoE prediction, QoS recommendation, and scenario simulation.
            </p>
          </div>

          <div className="grid gap-6 xl:grid-cols-[640px_1fr]">
            <div className="space-y-6">
              <DatasetExplorer />
              {loadingKpis ? (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                  <p className="text-slate-700">Loading KPI definitions...</p>
                </div>
              ) : kpiError ? (
                <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm text-red-600">
                  {kpiError}
                </div>
              ) : (
                <KpiPanel kpis={kpis} />
              )}
            </div>

            <div className="space-y-6">
              <ForecastPanel />
              <CongestionPanel />
              <QoEPanel />
              <QoSPanel />
              <ResourceAllocationPanel />
              <WhatIfPanel />
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
