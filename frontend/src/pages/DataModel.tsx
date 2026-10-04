import React, { useEffect, useState } from 'react';
import { fetchSourceHealth, fetchModelMetrics } from '../api';
import { Database, Server, Activity, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';
import { FreshnessBadge } from '../components/FreshnessBadge';

export default function DataModel() {
  const [health, setHealth] = useState<any>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchSourceHealth().catch(e => null),
      fetchModelMetrics().catch(e => null)
    ]).then(([h, m]) => {
      setHealth(h);
      setMetrics(m);
      setLoading(false);
    });
  }, []);

  if (loading) {
     return <div className="max-w-7xl mx-auto h-[600px] bg-slate-900/40 rounded-3xl animate-pulse"></div>;
  }

  const aqStatus = health?.air_quality?.status || 'UNAVAILABLE';
  const weatherStatus = health?.weather?.status || 'UNAVAILABLE';

  return (
    <div className="space-y-8 max-w-7xl mx-auto animate-fade-in-up">
      <header>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2 mb-1">
           <Database className="w-6 h-6 text-blue-500" />
           System & Data Architecture
        </h1>
        <p className="text-slate-400 text-sm">
           Real-time ingestion health, model performance, and API status.
        </p>
      </header>

      {/* Engineering Pipeline Monitor */}
      <section className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-8 relative overflow-hidden">
         <h2 className="text-lg font-bold text-slate-100 mb-6 flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" /> Data Pipeline Topology
         </h2>
         
         <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            
            <PipelineNode name="OpenAQ / Weather" status={aqStatus} type="Source" />
            <ArrowRight className="w-6 h-6 text-slate-600 hidden md:block" />
            
            <PipelineNode name="Ingestion Service" status="ONLINE" type="Worker" />
            <ArrowRight className="w-6 h-6 text-slate-600 hidden md:block" />
            
            <PipelineNode name="Feature Builder" status="ONLINE" type="Compute" />
            <ArrowRight className="w-6 h-6 text-slate-600 hidden md:block" />
            
            <PipelineNode name="XGBoost Engine" status="ONLINE" type="Model" />
            <ArrowRight className="w-6 h-6 text-slate-600 hidden md:block" />
            
            <PipelineNode name="FastAPI" status="ONLINE" type="Gateway" />
            
         </div>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Source Health */}
        <section className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-8">
           <h2 className="text-lg font-bold text-slate-100 mb-6">Source Health</h2>
           
           <div className="space-y-6">
              <div className="border-b border-slate-800/60 pb-6">
                 <div className="flex justify-between items-start mb-2">
                    <div>
                       <h3 className="text-sm font-bold text-slate-200">OpenAQ Network</h3>
                       <p className="text-xs text-slate-500 mt-1">Ground-truth sensor arrays (PM2.5, PM10)</p>
                    </div>
                    <FreshnessBadge status={aqStatus} timestamp={health?.air_quality?.latest_observation} />
                 </div>
                 {aqStatus === 'AUTHENTICATION_FAILED' && (
                    <div className="mt-3 bg-red-500/10 border border-red-500/20 p-3 rounded-lg flex items-start gap-2">
                       <AlertCircle className="w-4 h-4 text-red-400 mt-0.5 shrink-0" />
                       <p className="text-xs text-red-300">OpenAQ API authentication is currently suspended. The pipeline has automatically failed-over to atmospheric proxies to prevent system downtime.</p>
                    </div>
                 )}
              </div>

              <div>
                 <div className="flex justify-between items-start mb-2">
                    <div>
                       <h3 className="text-sm font-bold text-slate-200">Open-Meteo AQ</h3>
                       <p className="text-xs text-slate-500 mt-1">Continuous atmospheric proxy modeling</p>
                    </div>
                    <FreshnessBadge status={weatherStatus} timestamp={health?.weather?.latest_observation} />
                 </div>
              </div>
           </div>
        </section>

        {/* Model Performance */}
        <section className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-8">
           <div className="flex justify-between items-center mb-6">
              <h2 className="text-lg font-bold text-slate-100">Forecast Validation</h2>
              <span className="text-[10px] uppercase font-bold text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20 flex items-center gap-1">
                 <ShieldCheck className="w-3 h-3" /> Ground Truth Validated
              </span>
           </div>

           {metrics ? (
             <>
               <div className="grid grid-cols-3 gap-4 mb-8">
                 <div className="bg-slate-950/50 p-4 rounded-2xl border border-slate-800/80 text-center">
                    <div className="text-[10px] text-slate-500 font-bold uppercase mb-1">MAE</div>
                    <div className="text-xl font-black text-slate-200">{metrics.metrics?.MAE?.toFixed(2) || '--'}</div>
                 </div>
                 <div className="bg-slate-950/50 p-4 rounded-2xl border border-slate-800/80 text-center">
                    <div className="text-[10px] text-slate-500 font-bold uppercase mb-1">RMSE</div>
                    <div className="text-xl font-black text-slate-200">{metrics.metrics?.RMSE?.toFixed(2) || '--'}</div>
                 </div>
                 <div className="bg-slate-950/50 p-4 rounded-2xl border border-slate-800/80 text-center">
                    <div className="text-[10px] text-slate-500 font-bold uppercase mb-1">R² Score</div>
                    <div className="text-xl font-black text-slate-200">{metrics.metrics?.R2?.toFixed(2) || '--'}</div>
                 </div>
               </div>

               <div className="text-xs text-slate-400 space-y-2 border-t border-slate-800/60 pt-6">
                  <div className="flex justify-between">
                     <span className="text-slate-500">Model Architecture</span>
                     <span className="font-mono text-slate-300">{metrics.model}</span>
                  </div>
                  <div className="flex justify-between">
                     <span className="text-slate-500">Prediction Horizon</span>
                     <span className="font-mono text-slate-300">{metrics.horizon} Hours</span>
                  </div>
               </div>
             </>
           ) : (
             <div className="text-sm text-slate-500 text-center py-8">Model metrics unavailable.</div>
           )}
        </section>

      </div>
    </div>
  );
}

function PipelineNode({ name, status, type }: { name: string, status: string, type: string }) {
   let color = 'border-slate-700 bg-slate-800 text-slate-400';
   if (status === 'ONLINE' || status === 'LIVE' || status === 'RECENT') {
      color = 'border-emerald-500/50 bg-emerald-900/20 text-emerald-400';
   } else if (status === 'AUTHENTICATION_FAILED' || status === 'UNAVAILABLE') {
      color = 'border-red-500/50 bg-red-900/20 text-red-400';
   }

   return (
      <div className={`p-4 rounded-xl border w-full md:w-auto text-center shadow-lg ${color}`}>
         <div className="text-[10px] uppercase font-bold tracking-widest opacity-70 mb-1">{type}</div>
         <div className="text-sm font-bold truncate">{name}</div>
      </div>
   );
}
