import React, { useEffect, useState } from 'react';
import { fetchEvents } from '../api';
import { FreshnessBadge } from '../components/FreshnessBadge';
import { Activity, AlertTriangle, Terminal } from 'lucide-react';

export default function PollutionEvents() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchEvents()
      .then(res => {
        setData(res);
        setLoading(false);
      })
      .catch(err => { 
         console.error(err);
         setError('Failed to load event detector feed.');
         setLoading(false); 
      });
  }, []);

  if (loading) {
     return <div className="h-48 bg-slate-900/40 animate-pulse rounded-3xl"></div>;
  }
  
  if (error) {
     return <div className="text-red-500 text-sm font-mono">{error}</div>;
  }

  const events = data?.events || [];

  return (
    <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-8 relative overflow-hidden">
      <div className="absolute top-0 right-0 p-8 opacity-[0.03]"><Terminal className="w-32 h-32" /></div>
      
      <div className="relative z-10 flex justify-between items-start mb-8">
        <div>
           <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-1">
              <Terminal className="w-5 h-5 text-blue-500" /> Event Detection Engine
           </h2>
           <p className="text-sm text-slate-400">Autonomous multi-pollutant deterioration anomalies.</p>
        </div>
        <FreshnessBadge status={data?.status || "DERIVED"} timestamp={new Date().toISOString()} />
      </div>

      <div className="relative z-10">
         {events.length === 0 ? (
           <div className="flex flex-col items-center justify-center p-8 bg-slate-950/50 rounded-2xl border border-slate-800/80 border-dashed">
              <Activity className="w-8 h-8 text-emerald-600 mb-3" />
              <p className="text-sm font-mono text-emerald-400">SYSTEM.LOG: No multi-pollutant deterioration anomalies detected in the active window.</p>
           </div>
         ) : (
           <div className="space-y-4">
             {events.map((e: any, i: number) => (
               <div key={i} className="bg-slate-950/50 p-6 rounded-2xl border border-rose-500/30 shadow-[inset_0_0_20px_rgba(225,29,72,0.05)] font-mono text-sm">
                 <div className="flex justify-between items-start mb-4 border-b border-slate-800/80 pb-4">
                   <div className="flex items-center gap-2 text-rose-400">
                      <AlertTriangle className="w-5 h-5" />
                      <h3 className="font-bold uppercase tracking-widest">{e.event_type}</h3>
                   </div>
                   <FreshnessBadge status={e.data_status} timestamp={new Date().toISOString()} />
                 </div>
                 
                 <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                   <div>
                     <span className="block text-slate-500 uppercase text-[10px] tracking-widest mb-2">Start Time</span>
                     <span className="text-slate-300">{e.start_time}</span>
                   </div>
                   <div>
                     <span className="block text-slate-500 uppercase text-[10px] tracking-widest mb-2">Severity</span>
                     <span className="text-rose-300 font-bold bg-rose-500/10 px-2 py-1 rounded border border-rose-500/20">{e.severity || 'HIGH'}</span>
                   </div>
                   <div className="col-span-2">
                     <span className="block text-slate-500 uppercase text-[10px] tracking-widest mb-2">Details</span>
                     <span className="text-slate-400 leading-relaxed">{e.details || 'Conditions met for autonomous anomaly detection.'}</span>
                   </div>
                 </div>
               </div>
             ))}
           </div>
         )}
      </div>
    </div>
  );
}
