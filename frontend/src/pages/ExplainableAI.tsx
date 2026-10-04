import React, { useEffect, useState } from 'react';
import { fetchExplain } from '../api';
import { ProvenanceBadge } from '../components/ProvenanceBadge';
import { Shield, BrainCircuit } from 'lucide-react';

export default function ExplainableAI() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchExplain()
      .then(res => {
        setData(res);
        setLoading(false);
      })
      .catch(err => { 
         console.error(err);
         // Safely extract backend error message if available, otherwise generic
         const msg = err.response?.data?.detail || err.message || 'SHAP Explainer connection failed.';
         setError(msg);
         setLoading(false); 
      });
  }, []);

  if (loading) {
     return <div className="h-48 bg-slate-100 animate-pulse rounded-xl"></div>;
  }
  
  if (error) {
     return (
        <div className="bg-slate-900 rounded-xl shadow-sm border border-slate-800 overflow-hidden text-slate-300">
           <div className="border-b border-slate-800 p-4 bg-slate-950 flex justify-between items-center">
              <div className="flex items-center gap-3">
                 <BrainCircuit className="w-5 h-5 text-slate-600" />
                 <h2 className="text-sm font-bold text-slate-100 tracking-wider uppercase">SHAP Explainer</h2>
              </div>
           </div>
           <div className="p-8 flex flex-col items-center text-center">
              <Shield className="w-8 h-8 text-slate-600 mb-3" />
              <p className="text-sm font-mono text-slate-400 max-w-lg">
                 SHAP explainability unavailable: {error}
              </p>
           </div>
        </div>
     );
  }

  return (
    <div className="bg-slate-900 rounded-xl shadow-sm border border-slate-800 overflow-hidden text-slate-300">
      <div className="border-b border-slate-800 p-4 bg-slate-950 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <BrainCircuit className="w-5 h-5 text-blue-400" />
          <h2 className="text-sm font-bold text-slate-100 tracking-wider uppercase">SHAP Explainer / XGBoost Engine</h2>
        </div>
        <ProvenanceBadge status={data?.data_status || "MODEL_FORECAST"} />
      </div>

      <div className="p-6">
         <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Positive Impacts (Increases PM2.5) */}
            <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700/50">
               <h3 className="text-xs font-bold text-rose-400 mb-4 border-b border-slate-700 pb-2 uppercase tracking-wider">Features Increasing Forecast</h3>
               <div className="space-y-4">
                 {data?.top_positive_factors?.map((f: any, i: number) => (
                   <div key={i} className="text-sm font-mono">
                     <div className="flex justify-between items-center mb-1">
                        <span className="text-slate-300 truncate pr-2">{f.feature}</span>
                        <span className="text-xs text-slate-500 bg-slate-900 px-1.5 py-0.5 rounded">Val: {typeof f.value === 'number' ? f.value.toFixed(2) : f.value}</span>
                     </div>
                     <div className="w-full bg-slate-900 rounded h-1.5 overflow-hidden">
                        <div className="bg-rose-500 h-full rounded" style={{ width: `${Math.min(100, f.impact * 8)}%` }} />
                     </div>
                   </div>
                 ))}
               </div>
            </div>

            {/* Negative Impacts (Decreases PM2.5) */}
            <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700/50">
               <h3 className="text-xs font-bold text-emerald-400 mb-4 border-b border-slate-700 pb-2 uppercase tracking-wider">Features Decreasing Forecast</h3>
               <div className="space-y-4">
                 {data?.top_negative_factors?.map((f: any, i: number) => (
                   <div key={i} className="text-sm font-mono">
                     <div className="flex justify-between items-center mb-1">
                        <span className="text-slate-300 truncate pr-2">{f.feature}</span>
                        <span className="text-xs text-slate-500 bg-slate-900 px-1.5 py-0.5 rounded">Val: {typeof f.value === 'number' ? f.value.toFixed(2) : f.value}</span>
                     </div>
                     <div className="w-full bg-slate-900 rounded h-1.5 overflow-hidden">
                        <div className="bg-emerald-500 h-full rounded" style={{ width: `${Math.min(100, Math.abs(f.impact) * 8)}%` }} />
                     </div>
                   </div>
                 ))}
               </div>
            </div>
         </div>
         
         <div className="mt-6 flex items-start gap-2 bg-blue-900/20 text-blue-300 p-3 rounded border border-blue-900/30 text-xs">
            <Shield className="w-4 h-4 shrink-0 mt-0.5" />
            <p><strong>SHAP (SHapley Additive exPlanations)</strong> mathematically breaks down the XGBoost forecast output by assigning each feature an importance value for a particular prediction. It ensures the black-box model is traceable.</p>
         </div>
      </div>
    </div>
  );
}
