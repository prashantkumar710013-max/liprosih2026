import React, { useState, useEffect } from 'react';
import { postScenario, fetchBiomassFires } from '../api';
import { AlertCircle, Flame, ArrowRight, Activity, Beaker, FlaskConical, Wind, ArrowDown, Droplets } from 'lucide-react';

const SCENARIOS = [
  "BASELINE",
  "LOW_WIND",
  "HIGH_ATMOSPHERIC_TRAPPING",
  "RAIN_SCAVENGING",
  "REGIONAL_POLLUTION_INFLOW",
  "BIOMASS_BURNING_SCENARIO"
];

const SCENARIO_LABELS: Record<string, { label: string, desc: string, icon: any, color: string }> = {
  "BASELINE": { label: "Current Conditions", desc: "No changes to current atmospheric inputs.", icon: Activity, color: "text-blue-400" },
  "LOW_WIND": { label: "Stagnant Wind", desc: "Simulate dropping wind speeds to extreme lows.", icon: Wind, color: "text-amber-400" },
  "HIGH_ATMOSPHERIC_TRAPPING": { label: "Severe Weather Trapping", desc: "Simulate extreme thermal gradients that trap air.", icon: ArrowDown, color: "text-orange-400" },
  "RAIN_SCAVENGING": { label: "Heavy Rain Washout", desc: "Simulate a sudden downpour to clear PM2.5.", icon: Droplets, color: "text-blue-500" },
  "REGIONAL_POLLUTION_INFLOW": { label: "External Pollution Inflow", desc: "Simulate a spike in incoming regional background pollution.", icon: ArrowRight, color: "text-rose-500" },
  "BIOMASS_BURNING_SCENARIO": { label: "Simulate Crop Fires", desc: "Inject synthetic agricultural burning vectors.", icon: Flame, color: "text-red-500" }
};

export default function ScenarioLab() {
  const [activeScenario, setActiveScenario] = useState('BASELINE');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [biomassStatus, setBiomassStatus] = useState<any>(null);

  useEffect(() => {
    fetchBiomassFires().then(setBiomassStatus).catch(err => { console.error(err); });
    runScenario('BASELINE');
  }, []);

  const runScenario = async (scenario: string) => {
    setLoading(true);
    setError(null);
    setActiveScenario(scenario);
    try {
      const res = await postScenario('Delhi_Avg', scenario);
      setResult(res);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed to execute the scenario simulation.');
    }
    setLoading(false);
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto animate-fade-in-up">
      <header>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2 mb-1">
           <Beaker className="w-6 h-6 text-fuchsia-500" />
           Environmental Scenario Lab
        </h1>
        <p className="text-slate-400 text-sm">
           Execute hypothetical "What-If" simulations against the XGBoost engine.
        </p>
      </header>

      {biomassStatus?.status === 'BIOMASS_BURNING_DATA_UNAVAILABLE' && (
        <div className="bg-amber-500/10 border border-amber-500/20 p-4 rounded-2xl flex items-start gap-3 backdrop-blur-sm">
          <Flame className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <h3 className="text-sm font-bold text-amber-400 uppercase tracking-wide">Real Crop Fire Data Unavailable</h3>
            <p className="text-xs text-amber-200/70 mt-1">Live thermal anomaly data cannot be verified. Use the button below to execute a synthetic "Simulated Crop Fires" scenario instead.</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Scenarios List */}
        <div className="col-span-1 space-y-3 bg-slate-900/40 p-6 rounded-3xl border border-slate-800/60 backdrop-blur-md">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Simulation Models</h2>
          {SCENARIOS.map(s => {
             const isActive = activeScenario === s;
             const Icon = SCENARIO_LABELS[s].icon;
             return (
              <button
                key={s}
                onClick={() => runScenario(s)}
                className={`w-full text-left p-4 rounded-2xl border transition-all flex items-start gap-3 ${
                  isActive 
                  ? 'bg-blue-600/10 border-blue-500/30 shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)] text-slate-100' 
                  : 'bg-slate-950/50 border-slate-800/60 text-slate-400 hover:border-slate-600 hover:bg-slate-900'
                }`}
              >
                <Icon className={`w-5 h-5 shrink-0 mt-0.5 ${isActive ? SCENARIO_LABELS[s].color : 'text-slate-500'}`} />
                <div>
                  <div className={`font-bold text-sm ${isActive ? 'text-slate-200' : 'text-slate-300'}`}>
                     {SCENARIO_LABELS[s].label}
                  </div>
                  <div className={`text-xs mt-1 leading-relaxed ${isActive ? 'text-slate-400' : 'text-slate-500'}`}>
                     {SCENARIO_LABELS[s].desc}
                  </div>
                </div>
              </button>
             );
          })}
        </div>

        {/* Results Panel */}
        <div className="col-span-1 lg:col-span-2">
          {error ? (
            <div className="bg-red-500/10 text-red-400 p-6 rounded-3xl border border-red-500/20 flex items-start gap-4">
              <AlertCircle className="w-6 h-6 shrink-0 mt-0.5" />
              <div>
                <h2 className="font-bold text-lg mb-1 text-red-300">Simulation Failed</h2>
                <p className="text-sm">{error}</p>
              </div>
            </div>
          ) : loading ? (
            <div className="bg-slate-900/40 border border-slate-800/60 rounded-3xl p-12 flex flex-col items-center justify-center text-center backdrop-blur-md">
               <FlaskConical className="w-12 h-12 text-blue-500 animate-pulse mb-4" />
               <h3 className="text-lg font-bold text-slate-200">Executing XGBoost Scenario</h3>
               <p className="text-sm text-slate-400 mt-2 max-w-sm">Applying synthetic atmospheric modifications to the feature vector and running inference...</p>
            </div>
          ) : result && (
            <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
               <div className="absolute top-0 right-0 p-8 opacity-[0.03]"><FlaskConical className="w-64 h-64" /></div>
               
               <div className="relative z-10 flex justify-between items-start mb-8">
                  <div>
                    <h2 className="text-2xl font-bold text-slate-100 mb-1">{SCENARIO_LABELS[activeScenario].label}</h2>
                    <p className="text-sm text-slate-400">Simulation completed successfully.</p>
                  </div>
                  <div className="text-[10px] uppercase font-bold text-fuchsia-400 bg-fuchsia-500/10 px-2 py-1 rounded border border-fuchsia-500/20">
                     SYNTHETIC MODEL
                  </div>
               </div>

               {(() => {
                 const baseline = result.forecast_effect?.baseline_t1_pm25 || 1;
                 const scenVal = result.forecast_effect?.scenario_t1_pm25 || baseline;
                 const delta = result.forecast_effect?.delta_pm25 || 0;
                 const impact_percentage = (delta / baseline) * 100;
                 
                 return (
                   <>
                     <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 relative z-10">
                        <div className="bg-slate-950/80 rounded-2xl p-6 border border-slate-800/80">
                           <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Original Baseline (+24h)</div>
                           <div className="flex items-baseline gap-2">
                              <div className="text-4xl font-black text-slate-300">{baseline.toFixed(1)}</div>
                              <div className="text-slate-500 text-sm">µg/m³</div>
                           </div>
                        </div>
                        <div className="bg-blue-900/10 rounded-2xl p-6 border border-blue-500/30 shadow-[inset_0_0_20px_rgba(59,130,246,0.05)]">
                           <div className="text-[10px] font-bold text-blue-400 uppercase tracking-widest mb-2">Scenario Forecast (+24h)</div>
                           <div className="flex items-baseline gap-2">
                              <div className="text-4xl font-black text-blue-100">{scenVal.toFixed(1)}</div>
                              <div className="text-blue-400/60 text-sm">µg/m³</div>
                           </div>
                        </div>
                     </div>
      
                     <div className="bg-slate-950/50 rounded-2xl p-6 border border-slate-800/80 relative z-10">
                        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Impact Analysis</h3>
                        <div className="flex items-center gap-4">
                           <div className="flex-1 bg-slate-900 rounded-full h-3 overflow-hidden border border-slate-800">
                              {/* Render simple bar based on magnitude */}
                              <div 
                                className={`h-full rounded-full ${impact_percentage > 0 ? 'bg-gradient-to-r from-rose-600 to-rose-400' : 'bg-gradient-to-r from-emerald-600 to-emerald-400'}`} 
                                style={{ width: `${Math.min(100, Math.abs(impact_percentage || 0) * 2)}%` }}
                              ></div>
                           </div>
                           <div className={`font-mono font-bold text-lg ${impact_percentage > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                              {impact_percentage > 0 ? '+' : ''}{impact_percentage.toFixed(1)}%
                           </div>
                        </div>
                        <p className="text-xs text-slate-500 mt-4 leading-relaxed">
                           The applied hypothetical environmental conditions resulted in a {Math.abs(impact_percentage).toFixed(1)}% {impact_percentage > 0 ? 'increase' : 'decrease'} in expected PM2.5 concentrations compared to the baseline forecast model.
                        </p>
                     </div>
                   </>
                 );
               })()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
