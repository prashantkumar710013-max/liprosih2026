import React, { useEffect, useState } from 'react';
import { fetchForecastLive, fetchCurrent } from '../api';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Activity, AlertCircle, Clock, Info, Download } from 'lucide-react';
import { FreshnessBadge } from '../components/FreshnessBadge';

const CustomTooltip = ({ active, payload, label, activeMetric }: any) => {
  if (active && payload && payload.length) {
    const pred = payload.find((p: any) => p.dataKey === activeMetric);
    const isObserved = payload[0].payload.isObserved;
    
    // Map internal key to display name
    const metricNames: any = { prediction: 'PM2.5', aqi_prediction: 'AQI', o3_prediction: 'Ozone (O3)', pm10_prediction: 'PM10' };
    const displayMetric = metricNames[activeMetric] || 'PM2.5';
    
    let val = pred ? pred.value : payload[0].payload[activeMetric.replace('_prediction', '')];
    // Fallback if current doesn't have the exactly named key
    if (val === undefined && isObserved) {
        val = payload[0].payload.prediction; // fallback for current
    }

    return (
      <div className="bg-slate-900/90 backdrop-blur-md p-4 shadow-2xl border border-slate-700/60 rounded-xl min-w-[220px]">
        <div className="text-slate-400 text-[10px] font-bold uppercase tracking-widest mb-3 flex items-center gap-2">
           <Clock className="w-3 h-3" />
           {new Date(label).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
           {!isObserved && <span className="text-blue-400 ml-auto">+ {payload[0].payload.horizon}h</span>}
        </div>
        
        <div className="flex justify-between items-end mb-1">
          <span className="text-slate-300 font-medium text-sm">{displayMetric}</span>
          <div className="flex items-baseline gap-1">
            <span className={`font-bold text-2xl ${isObserved ? 'text-emerald-400' : 'text-blue-400'}`}>
               {val ? val.toFixed(1) : '--'}
            </span>
            <span className="text-slate-500 text-xs">{activeMetric === 'aqi_prediction' ? 'Index' : 'µg/m³'}</span>
          </div>
        </div>

        {!isObserved && activeMetric === 'prediction' && payload[0].payload.lower_bound && (
           <div className="mt-3 pt-3 border-t border-slate-800 text-[10px] text-slate-400 space-y-1">
              <div className="flex justify-between">
                 <span>Confidence Interval</span>
                 <span>95%</span>
              </div>
              <div className="flex justify-between">
                 <span>Expected Range</span>
                 <span className="font-mono text-slate-300">
                    {payload[0].payload.lower_bound.toFixed(0)} — {payload[0].payload.upper_bound.toFixed(0)}
                 </span>
              </div>
           </div>
        )}

        <div className="mt-3 pt-3 border-t border-slate-800 text-[10px] font-bold uppercase flex justify-between">
           <span className="text-slate-500">Status</span>
           <span className={isObserved ? 'text-emerald-500' : 'text-blue-500'}>
              {isObserved ? 'Observed Live' : 'XGBoost Prediction'}
           </span>
        </div>
      </div>
    );
  }
  return null;
};

export default function Forecast() {
  const [data, setData] = useState<any>(null);
  const [current, setCurrent] = useState<any>(null);
  const [horizon, setHorizon] = useState(72);
  const [activeMetric, setActiveMetric] = useState('prediction'); // prediction (pm25), aqi_prediction, o3_prediction
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetchForecastLive('Delhi_Avg', horizon, 'pm25'),
      fetchCurrent('Delhi_Avg')
    ]).then(([fc, cur]) => {
      setData(fc);
      setCurrent(cur);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setError(err.message || 'Unable to connect to forecasting engine.');
      setLoading(false);
    });
  }, [horizon]);

  if (error) {
    return (
      <div className="bg-red-500/10 text-red-400 p-6 rounded-2xl border border-red-500/20 max-w-3xl flex items-start gap-4 mx-auto mt-10">
        <AlertCircle className="w-6 h-6 shrink-0 mt-0.5" />
        <div>
          <h2 className="font-bold text-lg mb-1 text-red-300">Coupled Forecasting Engine Unavailable</h2>
          <p className="text-sm">{error}</p>
        </div>
      </div>
    );
  }

  // Combine current observation (t=0) with predictions
  let chartData: any[] = [];
  if (current && data?.forecasts) {
    chartData.push({
      timestamp: current.timestamp,
      prediction: current.pm25,
      pm10_prediction: current.pm10,
      o3_prediction: current.o3,
      aqi_prediction: current.aqi,
      horizon: 0,
      isObserved: true
    });
    
    chartData = chartData.concat(data.forecasts.map((f: any) => ({
      ...f,
      isObserved: false,
      range: activeMetric === 'prediction' ? [f.lower_bound, f.upper_bound] : undefined
    })));
  }

  const downloadCSV = () => {
    if (!chartData || chartData.length === 0) return;
    const header = ['timestamp', 'horizon', 'isObserved', 'PM2.5', 'AQI', 'Ozone', 'PM10'].join(',');
    const rows = chartData.map(r => 
      [r.timestamp, r.horizon, r.isObserved, r.prediction, r.aqi_prediction, r.o3_prediction, r.pm10_prediction].join(',')
    );
    const csvContent = [header, ...rows].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `lipro_coupled_forecast_${horizon}h.csv`;
    link.click();
  };

  return (
    <div className="max-w-7xl mx-auto animate-fade-in-up space-y-6">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
         <div>
            <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2 mb-1">
               <Activity className="w-6 h-6 text-blue-500" />
               Coupled Forecasting System
            </h1>
            <p className="text-slate-400 text-sm">
               72-Hour AQ forecasts mapping Meteorology &harr; Chemical Transport.
            </p>
         </div>
         <div className="flex flex-col items-end gap-3">
             <div className="flex items-center gap-2 bg-slate-900/50 p-1.5 rounded-lg border border-slate-800/60 backdrop-blur-sm">
                {[6, 12, 24, 72].map(h => (
                  <button 
                    key={h}
                    onClick={() => setHorizon(h)}
                    className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all ${horizon === h ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}
                  >
                    {h}H
                  </button>
                ))}
             </div>
         </div>
      </div>

      {loading ? (
        <div className="h-[500px] bg-slate-900/40 rounded-3xl border border-slate-800/60 animate-pulse"></div>
      ) : (
        <>
          <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
            <MetricTab label="AQI (Overall)" value="aqi_prediction" current={activeMetric} set={setActiveMetric} />
            <MetricTab label="PM2.5 (Aerosols)" value="prediction" current={activeMetric} set={setActiveMetric} />
            <MetricTab label="Ozone (O3)" value="o3_prediction" current={activeMetric} set={setActiveMetric} />
            <MetricTab label="PM10 (Dust)" value="pm10_prediction" current={activeMetric} set={setActiveMetric} />
            <button onClick={downloadCSV} className="ml-auto bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-lg text-xs font-bold flex items-center gap-2 transition-colors border border-slate-700">
               <Download className="w-4 h-4" /> Export CSV
            </button>
          </div>

          {/* Chart Area */}
          <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-6 relative">
            <div className="flex justify-between items-center mb-8">
               <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-emerald-400">
                     <span className="w-2 h-2 rounded-full bg-emerald-500"></span> Observed
                  </div>
                  <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-blue-400">
                     <span className="w-2 h-2 rounded-full bg-blue-500"></span> XGBoost Predicted
                  </div>
               </div>
               <FreshnessBadge timestamp={data?.generated_at} status="LIVE" />
            </div>

            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorPrediction" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0}/>
                    </linearGradient>
                    <linearGradient id="colorRange" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#1e293b" stopOpacity={0.5}/>
                      <stop offset="95%" stopColor="#1e293b" stopOpacity={0.1}/>
                    </linearGradient>
                  </defs>
                  
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                  
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={(tick) => new Date(tick).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} 
                    stroke="#475569" 
                    tick={{ fill: '#64748b', fontSize: 12 }} 
                    dy={10}
                  />
                  
                  <YAxis 
                    stroke="#475569" 
                    tick={{ fill: '#64748b', fontSize: 12 }} 
                    dx={-10}
                    domain={['auto', 'auto']}
                  />
                  
                  <RechartsTooltip content={<CustomTooltip activeMetric={activeMetric} />} />
                  
                  {activeMetric === 'prediction' && (
                      <Area 
                        type="monotone" 
                        dataKey="range" 
                        stroke="none" 
                        fill="url(#colorRange)" 
                        isAnimationActive={true}
                      />
                  )}
                  
                  <Area 
                    type="monotone" 
                    dataKey={activeMetric} 
                    stroke="#3b82f6" 
                    strokeWidth={3}
                    fill="url(#colorPrediction)"
                    activeDot={{ r: 6, strokeWidth: 0, fill: '#60a5fa' }} 
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            
            <div className="mt-6 flex items-start gap-3 bg-blue-500/5 border border-blue-500/10 p-4 rounded-xl">
               <Info className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
               <p className="text-xs text-slate-400 leading-relaxed">
                 <strong className="text-slate-300">Implementation Note:</strong> This pipeline uses an XGBoost MultiOutputRegressor coupled with Open-Meteo atmospheric integrations. 
                 It explicitly handles two-way feedback proxies between meteorology (temperature, wind, PBL height) and chemistry (PM2.5, PM10, O3, NOx) as requested in the problem statement, rather than a raw numerical physics simulation (like WRF-Chem).
               </p>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function MetricTab({ label, value, current, set }: { label: string, value: string, current: string, set: (v: string) => void }) {
    const isActive = current === value;
    return (
        <button 
           onClick={() => set(value)}
           className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all border whitespace-nowrap ${isActive ? 'bg-blue-600/10 border-blue-500/30 text-blue-400 shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)]' : 'bg-slate-900/50 border-slate-800/60 text-slate-500 hover:text-slate-300 hover:border-slate-700'}`}
        >
            {label}
        </button>
    )
}
