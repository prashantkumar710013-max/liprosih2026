import React, { useEffect, useState } from 'react';
import { fetchSourceHealth, fetchModelMetrics } from '../api';

export default function Methodology() {
  const [health, setHealth] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetchSourceHealth(),
      fetchModelMetrics()
    ])
      .then(([healthData, metricsData]) => {
        setHealth(healthData);
        setMetrics(metricsData);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setError(err.message || 'Failed to load system health');
        setLoading(false);
      });
  }, []);

  return (
    <div className="space-y-6 max-w-4xl">
      <header>
        <h1 className="text-3xl font-bold text-slate-800">Data & Method</h1>
        <p className="text-slate-500 mt-2">Transparency report on data sources, forecasting methodology, and system status.</p>
      </header>

      {error && (
        <div className="bg-red-50 text-red-600 rounded-xl border border-red-200 p-4">
          <p>{error}</p>
        </div>
      )}

      {loading ? (
        <div className="bg-white rounded-xl border border-slate-200 h-32 flex items-center justify-center text-slate-500">
          Loading system metrics...
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <h2 className="text-lg font-bold text-slate-800 mb-4">Data Freshness & Source Health</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center pb-3 border-b border-slate-100">
                  <div>
                    <span className="text-sm font-semibold text-slate-700 block">Air Quality (OpenAQ)</span>
                    <span className="text-xs text-slate-500 block">Station count: {health?.air_quality?.station_count || 0}</span>
                  </div>
                  <div className="text-right">
                    <StatusBadge status={health?.air_quality?.status || 'UNAVAILABLE'} />
                    <span className="text-xs text-slate-400 block mt-1">
                      {health?.air_quality?.latest_observation ? new Date(health.air_quality.latest_observation).toLocaleString() : 'No data'}
                    </span>
                  </div>
                </div>
                <div className="flex justify-between items-center pb-3 border-b border-slate-100">
                  <div>
                    <span className="text-sm font-semibold text-slate-700 block">Weather (Open-Meteo)</span>
                    <span className="text-xs text-slate-500 block">Location count: {health?.weather?.station_count || 0}</span>
                  </div>
                  <div className="text-right">
                    <StatusBadge status={health?.weather?.status || 'UNAVAILABLE'} />
                    <span className="text-xs text-slate-400 block mt-1">
                      {health?.weather?.latest_observation ? new Date(health.weather.latest_observation).toLocaleString() : 'No data'}
                    </span>
                  </div>
                </div>
                <div>
                   <p className="text-xs text-slate-500 mt-2">
                     * Status is automatically determined from observation timestamps, strictly enforcing a 120-minute freshness gate.
                   </p>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <h2 className="text-lg font-bold text-slate-800 mb-4">Model Performance (Evaluation Data)</h2>
              <div className="grid grid-cols-3 gap-4">
                <MetricBox label="MAE" value={metrics?.metrics?.MAE} />
                <MetricBox label="RMSE" value={metrics?.metrics?.RMSE} />
                <MetricBox label="R²" value={metrics?.metrics?.R2} />
              </div>
              <div className="mt-4 text-sm text-slate-600">
                <p><strong>Architecture:</strong> {metrics?.model}</p>
                <p><strong>Horizon:</strong> {metrics?.horizon} hours</p>
                <p className="text-xs text-slate-500 mt-2">
                  * Metrics are derived from the strict holdout evaluation phase during model training. Never fabricated.
                </p>
              </div>
            </div>
          </div>
        </>
      )}

      <div className="bg-slate-50 rounded-xl border border-slate-200 p-6 space-y-6">
        <h2 className="text-xl font-bold text-slate-800">Provenance Definitions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Def term="Observed" desc="Real-time, verified measurements from live external sources." />
          <Def term="Historical Data Mode" desc="System fallback to verified historical database when live data is stale." />
          <Def term="Current Data Unavailable" desc="Live API connection works, but the sensor observations are too old." />
          <Def term="Forecast" desc="Machine learning output spanning 0-72 hours into the future." />
          <Def term="Derived Indicator" desc="A mathematically computed condition (e.g., Air Dispersion) based on meteorological proxy combinations." />
          <Def term="Model Estimate" desc="Used for features like Atmospheric Trapping where direct vertical profile data is absent." />
          <Def term="Simulated Scenario" desc="A hypothetical modeling run (e.g., What-if we reduced wind by 2.0 m/s? or Simulated Biomass)." />
        </div>
      </div>

      <div className="space-y-6">
        <h2 className="text-xl font-bold text-slate-800">Technical Details & Limitations</h2>
        <div className="space-y-4">
          <Section title="Data Pipeline & Forecasting Method" content="Lipro uses an XGBoost MultiOutputRegressor to forecast a direct 72-hour vector, eliminating compounding autoregressive loop errors. A strict chronological 80/20 split was used to prevent data leakage during training." />
          <Section title="Atmospheric Intelligence" content="Because vertical atmospheric profiles (PBL) are typically unavailable in open datasets, the system mathematically derives Trapping and Air Dispersion (Ventilation Index) proxies using extreme diurnal cooling and nocturnal wind stagnation indicators." />
          <Section title="Transport Approximation" content="The pollution transport module is a Simplified Advection Proxy. It is an estimation of wind-driven transport vectors, NOT a rigorous WRF-Chem or CFD physical simulation." />
          <Section title="Limitations" content="1. Daily historical weather was forward-filled to hourly, flattening intra-day thermodynamics in the historical dataset. 2. Spatial interpolation is a mathematical estimation (IDW), not a high-resolution CFD grid. 3. Vehicular traffic flow data is excluded due to API limitations." />
        </div>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const isGood = status === 'LIVE' || status === 'RECENT';
  return (
    <span className={`px-2 py-1 text-xs font-bold rounded-md ${
      isGood ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
    }`}>
      {status}
    </span>
  );
}

function MetricBox({ label, value }: { label: string, value: number }) {
  return (
    <div className="bg-slate-50 p-3 rounded-lg border border-slate-100 text-center">
      <div className="text-xs text-slate-500 mb-1">{label}</div>
      <div className="text-lg font-bold text-slate-800">{value}</div>
    </div>
  );
}

function Def({ term, desc }: { term: string, desc: string }) {
  return (
    <div>
      <span className="font-bold text-slate-700">{term}:</span> <span className="text-slate-600 text-sm">{desc}</span>
    </div>
  );
}

function Section({ title, content }: { title: string, content: string }) {
  return (
    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
      <h3 className="font-bold text-slate-800 mb-2">{title}</h3>
      <p className="text-sm text-slate-600 leading-relaxed">{content}</p>
    </div>
  );
}
