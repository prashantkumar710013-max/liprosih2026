import React, { useEffect, useState } from 'react';
import { fetchAtmosphericRisk, fetchExplain } from '../api';
import { CloudRain, ArrowDown, ArrowUp, Activity, BrainCircuit, Shield, AlertCircle, Wind } from 'lucide-react';
import { FreshnessBadge } from '../components/FreshnessBadge';

export default function AtmosphericIntelligence() {
  const [data, setData] = useState<any>(null);
  const [shap, setShap] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetchAtmosphericRisk('Delhi_Avg').catch(e => null),
      fetchExplain('Delhi_Avg').catch(e => null)
    ]).then(([rsk, exp]) => {
      setData(rsk);
      setShap(exp);
      setLoading(false);
    }).catch(err => {
      setError(err.message || 'Unable to connect to intelligence backend.');
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="space-y-6 max-w-7xl mx-auto animate-pulse">
        <div className="h-24 bg-slate-800/50 rounded-2xl"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
           <div className="h-64 bg-slate-800/50 rounded-2xl"></div>
           <div className="h-64 bg-slate-800/50 rounded-2xl"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-500/10 text-red-400 p-6 rounded-2xl border border-red-500/20 max-w-3xl flex items-start gap-4">
         <AlertCircle className="w-6 h-6 shrink-0 mt-0.5" />
         <div>
           <h2 className="font-bold text-lg mb-1 text-red-300">Error loading AI Insights</h2>
           <p className="text-sm">{error}</p>
         </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto animate-fade-in-up">
      <header>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2 mb-1">
           <BrainCircuit className="w-6 h-6 text-indigo-400" />
           AI Insights
        </h1>
        <p className="text-slate-400 text-sm">
           Explainable AI (SHAP) and atmospheric correlations for Delhi-NCR.
        </p>
      </header>

      {/* SHAP Explainer (Why is pollution changing?) */}
      {shap ? (
        <section className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-6 lg:p-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-8 opacity-[0.03]"><BrainCircuit className="w-64 h-64" /></div>
          
          <div className="relative z-10">
            <div className="flex justify-between items-start mb-8">
              <div>
                <h2 className="text-xl font-bold text-slate-100 mb-1">Why does Lipro expect this prediction?</h2>
                <p className="text-sm text-slate-400">SHAP (SHapley Additive exPlanations) mathematically isolates the impact of individual features on the XGBoost prediction.</p>
              </div>
              <FreshnessBadge status={shap.data_status || "MODEL_FORECAST"} timestamp={new Date().toISOString()} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
               {/* Positive Impacts */}
               <div className="bg-slate-950/50 p-6 rounded-2xl border border-slate-800/80">
                  <h3 className="text-xs font-bold text-rose-400 mb-6 border-b border-slate-800 pb-3 uppercase tracking-widest flex items-center gap-2">
                    <ArrowUp className="w-4 h-4" /> Driving Pollution Up
                  </h3>
                  <div className="space-y-5">
                    {shap?.top_positive_factors?.slice(0, 5).map((f: any, i: number) => (
                      <div key={i} className="text-sm">
                        <div className="flex justify-between items-end mb-2">
                           <span className="text-slate-200 font-medium">{f.feature}</span>
                           <span className="text-xs text-slate-500 font-mono">Value: {typeof f.value === 'number' ? f.value.toFixed(2) : f.value}</span>
                        </div>
                        <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden shadow-inner">
                           <div className="bg-gradient-to-r from-rose-600 to-rose-400 h-full rounded-full" style={{ width: `${Math.min(100, f.impact * 12)}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
               </div>

               {/* Negative Impacts */}
               <div className="bg-slate-950/50 p-6 rounded-2xl border border-slate-800/80">
                  <h3 className="text-xs font-bold text-emerald-400 mb-6 border-b border-slate-800 pb-3 uppercase tracking-widest flex items-center gap-2">
                    <ArrowDown className="w-4 h-4" /> Driving Pollution Down
                  </h3>
                  <div className="space-y-5">
                    {shap?.top_negative_factors?.slice(0, 5).map((f: any, i: number) => (
                      <div key={i} className="text-sm">
                        <div className="flex justify-between items-end mb-2">
                           <span className="text-slate-200 font-medium">{f.feature}</span>
                           <span className="text-xs text-slate-500 font-mono">Value: {typeof f.value === 'number' ? f.value.toFixed(2) : f.value}</span>
                        </div>
                        <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden shadow-inner">
                           <div className="bg-gradient-to-r from-emerald-600 to-emerald-400 h-full rounded-full" style={{ width: `${Math.min(100, Math.abs(f.impact) * 12)}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
               </div>
            </div>
          </div>
        </section>
      ) : (
        <div className="bg-slate-900/40 border border-slate-800/60 p-8 rounded-3xl text-center">
           <Shield className="w-8 h-8 text-slate-600 mx-auto mb-3" />
           <p className="text-sm text-slate-400">SHAP Explainability currently unavailable. Models may be initializing.</p>
        </div>
      )}

      {/* Meteorological Correlators */}
      {data && (
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-6 relative overflow-hidden group">
            <div className="flex justify-between items-start mb-6 relative z-10">
              <div className="flex items-center gap-3">
                <div className="bg-orange-500/10 p-2.5 rounded-xl text-orange-400 border border-orange-500/20">
                  <ArrowDown className="w-5 h-5" />
                </div>
                <h2 className="text-lg font-bold text-slate-100">Atmospheric Trapping</h2>
              </div>
              <FreshnessBadge status={data.status} timestamp={data.timestamp} />
            </div>
            
            <div className="mb-6 relative z-10">
              <div className="text-4xl font-black text-slate-100 mb-1 tracking-tight">
                {data.trapping?.category || 'UNKNOWN'}
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="text-slate-500 font-medium uppercase tracking-widest text-xs">Index Score</span>
                <span className="text-orange-400 font-bold">{data.trapping?.score ?? '--'} / 100</span>
              </div>
            </div>
            
            <div className="bg-slate-950/50 p-4 rounded-2xl border border-slate-800/60 text-sm text-slate-400 relative z-10">
              <p className="leading-relaxed">Derived from surface meteorological conditions (cooling gradients). Indicates the likelihood of pollution being mechanically trapped near the surface rather than dispersing.</p>
            </div>
          </div>

          <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-6 relative overflow-hidden group">
            <div className="flex justify-between items-start mb-6 relative z-10">
              <div className="flex items-center gap-3">
                <div className="bg-emerald-500/10 p-2.5 rounded-xl text-emerald-400 border border-emerald-500/20">
                  <Wind className="w-5 h-5" />
                </div>
                <h2 className="text-lg font-bold text-slate-100">Ventilation Proxy</h2>
              </div>
              <FreshnessBadge status={data.status} timestamp={data.timestamp} />
            </div>
            
            <div className="mb-6 relative z-10">
              <div className="text-4xl font-black text-slate-100 mb-1 tracking-tight">
                {data.ventilation?.category || 'UNKNOWN'}
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="text-slate-500 font-medium uppercase tracking-widest text-xs">Index Score</span>
                <span className="text-emerald-400 font-bold">{data.ventilation?.score ?? '--'} / 100</span>
              </div>
            </div>
            
            <div className="bg-slate-950/50 p-4 rounded-2xl border border-slate-800/60 text-sm text-slate-400 relative z-10">
              <p className="leading-relaxed">Estimates the atmosphere's capability to dilute pollutants horizontally. High ventilation suggests rapid clearing of newly emitted particulates.</p>
            </div>
          </div>

        </section>
      )}

    </div>
  );
}
