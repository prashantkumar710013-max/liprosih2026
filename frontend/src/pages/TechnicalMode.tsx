import React from 'react';
import PollutionEvents from './PollutionEvents';
import { Settings, Server, Database } from 'lucide-react';

export default function TechnicalMode() {
  return (
    <div className="space-y-8 max-w-7xl mx-auto animate-fade-in-up">
      <header>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2 mb-1">
           <Settings className="w-6 h-6 text-slate-400" />
           Technical Mode
        </h1>
        <p className="text-slate-400 text-sm">
           Advanced evaluator metrics and autonomous event methodologies.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
         <div className="bg-slate-900/40 border border-slate-800/60 rounded-2xl p-6 flex items-center gap-4">
            <div className="p-3 bg-emerald-500/10 rounded-xl text-emerald-400 border border-emerald-500/20">
               <Server className="w-6 h-6" />
            </div>
            <div>
               <div className="text-sm font-bold text-slate-300">FastAPI Backend</div>
               <div className="text-xs text-slate-500 mt-1">Uvicorn / Python 3.11</div>
            </div>
         </div>
         <div className="bg-slate-900/40 border border-slate-800/60 rounded-2xl p-6 flex items-center gap-4">
            <div className="p-3 bg-blue-500/10 rounded-xl text-blue-400 border border-blue-500/20">
               <Database className="w-6 h-6" />
            </div>
            <div>
               <div className="text-sm font-bold text-slate-300">SQLite Timeseries</div>
               <div className="text-xs text-slate-500 mt-1">Local Edge Database</div>
            </div>
         </div>
         <div className="bg-slate-900/40 border border-slate-800/60 rounded-2xl p-6 flex items-center gap-4">
            <div className="p-3 bg-purple-500/10 rounded-xl text-purple-400 border border-purple-500/20">
               <Settings className="w-6 h-6" />
            </div>
            <div>
               <div className="text-sm font-bold text-slate-300">XGBoost Engine</div>
               <div className="text-xs text-slate-500 mt-1">MultiOutputRegressor (72h)</div>
            </div>
         </div>
      </div>

      <section>
        <PollutionEvents />
      </section>
    </div>
  );
}
