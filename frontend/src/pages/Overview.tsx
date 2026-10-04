import React, { useEffect, useState } from 'react';
import { fetchCurrent, fetchAtmosphericRisk, fetchForecastLive } from '../api';
import { FreshnessBadge } from '../components/FreshnessBadge';
import { ArrowRight, Wind, Activity, Thermometer, Droplets, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Overview() {
  const [current, setCurrent] = useState<any>(null);
  const [risk, setRisk] = useState<any>(null);
  const [forecast, setForecast] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetchCurrent('Delhi_Avg'),
      fetchAtmosphericRisk('Delhi_Avg'),
      fetchForecastLive('Delhi_Avg', 24, 'pm25')
    ]).then(([cur, rsk, fc]) => {
      setCurrent(cur);
      setRisk(rsk);
      setForecast(fc);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setError(err.message || 'Unable to connect to Lipro backend.');
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="space-y-6 max-w-7xl mx-auto animate-pulse">
        <div className="h-32 bg-slate-800/50 rounded-2xl"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
           <div className="h-40 bg-slate-800/50 rounded-2xl"></div>
           <div className="h-40 bg-slate-800/50 rounded-2xl"></div>
           <div className="h-40 bg-slate-800/50 rounded-2xl"></div>
           <div className="h-40 bg-slate-800/50 rounded-2xl"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-500/10 text-red-400 p-6 rounded-2xl border border-red-500/20 max-w-3xl flex items-start gap-4">
        <AlertCircle className="w-6 h-6 shrink-0 mt-0.5" />
        <div>
          <h2 className="font-bold text-lg mb-1 text-red-300">Unable to load environmental intelligence</h2>
          <p className="text-sm">{error}</p>
        </div>
      </div>
    );
  }

  const currentPm25 = current?.pm25 ?? 0;
  const currentPm10 = current?.pm10 ?? 0;
  
  // Forecast summaries
  const fcData = forecast?.forecasts || [];
  const next6 = fcData[5]?.prediction ?? currentPm25;
  const next12 = fcData[11]?.prediction ?? currentPm25;
  const next24 = fcData[23]?.prediction ?? currentPm25;

  const getAQIColor = (val: number) => {
    if (val <= 50) return 'text-emerald-400';
    if (val <= 100) return 'text-yellow-400';
    if (val <= 150) return 'text-orange-400';
    if (val <= 200) return 'text-red-400';
    if (val <= 300) return 'text-purple-400';
    return 'text-rose-600';
  };

  const getAQIString = (val: number) => {
    if (val <= 50) return 'Good';
    if (val <= 100) return 'Satisfactory';
    if (val <= 150) return 'Moderate';
    if (val <= 200) return 'Poor';
    if (val <= 300) return 'Very Poor';
    return 'Severe';
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in-up">
      {/* Universal Data Freshness Alert (if degraded) */}
      {current?.status === 'AUTHENTICATION_FAILED' && (
        <div className="bg-amber-500/10 border border-amber-500/20 rounded-2xl p-4 flex items-start gap-3 backdrop-blur-sm">
           <AlertCircle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
           <div>
             <h3 className="text-amber-400 font-semibold text-sm">OpenAQ API Access Suspended</h3>
             <p className="text-amber-200/70 text-xs mt-1">
               True physical sensor data is unavailable. The system has automatically fallen back to the Open-Meteo atmospheric model to sustain live forecasting.
             </p>
           </div>
        </div>
      )}

      {/* Main KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* AQI Card */}
        <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-6 relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-6 opacity-10"><Activity className="w-24 h-24" /></div>
          <div className="relative z-10 flex flex-col h-full justify-between">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-slate-400 text-sm font-semibold tracking-wider">OVERALL AQI</span>
                <FreshnessBadge timestamp={current?.timestamp} status={current?.status} />
              </div>
              <div className={`text-5xl font-black tracking-tighter ${getAQIColor(current?.aqi ?? 150)}`}>
                {Math.round(current?.aqi ?? 150)}
              </div>
              <div className={`text-sm font-bold uppercase mt-1 ${getAQIColor(current?.aqi ?? 150)}`}>
                {getAQIString(current?.aqi ?? 150)}
              </div>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-800/60 flex items-center justify-between text-xs text-slate-500">
               <span>Station: Delhi-NCR Avg</span>
               <span className="bg-slate-800/50 px-2 py-0.5 rounded text-slate-400">
                 {current?.status === 'MODEL_FORECAST' ? 'Proxy Model' : 'Sensor'}
               </span>
            </div>
          </div>
        </div>

        {/* PM2.5 Card */}
        <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-6 relative overflow-hidden group">
          <div className="relative z-10 flex flex-col h-full justify-between">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-slate-400 text-sm font-semibold tracking-wider">PM2.5</span>
                <FreshnessBadge timestamp={current?.timestamp} status={current?.status} />
              </div>
              <div className="flex items-baseline gap-2">
                <div className="text-4xl font-bold text-slate-100">{Math.round(currentPm25)}</div>
                <div className="text-slate-500 text-sm font-medium">µg/m³</div>
              </div>
            </div>
            
            <div className="mt-4 bg-slate-950/50 rounded-xl p-3">
               <div className="text-[10px] text-slate-500 font-bold uppercase mb-2">24H Prediction</div>
               <div className="flex justify-between items-end">
                 <div className="text-xl font-bold text-slate-300">{Math.round(next24)}</div>
                 <Activity className={`w-4 h-4 ${next24 > currentPm25 ? 'text-red-400' : 'text-emerald-400'}`} />
               </div>
            </div>
          </div>
        </div>

        {/* PM10 Card */}
        <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-6 relative overflow-hidden group">
          <div className="relative z-10 flex flex-col h-full justify-between">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-slate-400 text-sm font-semibold tracking-wider">PM10</span>
                <FreshnessBadge timestamp={current?.timestamp} status={current?.status} />
              </div>
              <div className="flex items-baseline gap-2">
                <div className="text-4xl font-bold text-slate-100">{Math.round(currentPm10)}</div>
                <div className="text-slate-500 text-sm font-medium">µg/m³</div>
              </div>
            </div>
            
            <div className="mt-6 pt-4 border-t border-slate-800/60 text-xs text-slate-500">
               Last updated: {new Date(current?.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
            </div>
          </div>
        </div>

        {/* Weather Subsystem */}
        <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-6 relative overflow-hidden group flex flex-col justify-between">
           <div className="flex justify-between items-center mb-4">
             <span className="text-slate-400 text-sm font-semibold tracking-wider">METEOROLOGY</span>
             <FreshnessBadge timestamp={current?.timestamp} status={current?.status} />
           </div>
           
           <div className="space-y-4">
              <div className="flex items-center justify-between">
                 <div className="flex items-center gap-2 text-slate-300">
                    <Thermometer className="w-4 h-4 text-orange-400" />
                    <span className="text-sm font-medium">Temperature</span>
                 </div>
                 <span className="text-slate-100 font-bold">{Math.round(current?.temperature ?? 0)}°C</span>
              </div>
              <div className="flex items-center justify-between">
                 <div className="flex items-center gap-2 text-slate-300">
                    <Droplets className="w-4 h-4 text-blue-400" />
                    <span className="text-sm font-medium">Humidity</span>
                 </div>
                 <span className="text-slate-100 font-bold">{Math.round(current?.humidity ?? 0)}%</span>
              </div>
              <div className="flex items-center justify-between">
                 <div className="flex items-center gap-2 text-slate-300">
                    <Wind className="w-4 h-4 text-teal-400" />
                    <span className="text-sm font-medium">Wind</span>
                 </div>
                 <span className="text-slate-100 font-bold">{Math.round(current?.wind_speed ?? 0)} m/s</span>
              </div>
           </div>
        </div>
      </div>

      {/* Atmospheric Context & CTAs */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
         <div className="lg:col-span-2 bg-gradient-to-r from-blue-900/20 to-indigo-900/10 border border-blue-500/20 rounded-3xl p-6 flex flex-col justify-center relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 to-indigo-500"></div>
            <h3 className="text-xl font-bold text-slate-100 mb-2">Atmospheric Risk Intelligence</h3>
            <p className="text-slate-400 text-sm max-w-xl leading-relaxed">
              {risk?.ventilation?.category === 'POOR' 
                ? "Poor ventilation is currently trapping particulates close to the surface, accelerating pollutant accumulation."
                : "Air dispersion is currently favorable. Meteorological variables suggest lower risk of particulate trapping."
              }
            </p>
            <div className="mt-6 flex gap-4">
               <Link to="/forecast" className="px-4 py-2 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 text-blue-400 text-sm font-semibold rounded-xl transition-colors flex items-center gap-2">
                 Explore 72h Forecast <ArrowRight className="w-4 h-4" />
               </Link>
               <Link to="/atmosphere" className="px-4 py-2 bg-slate-800/50 hover:bg-slate-700/50 border border-slate-700/50 text-slate-300 text-sm font-semibold rounded-xl transition-colors">
                 View Explainable AI
               </Link>
            </div>
         </div>
         
         <div className="bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl p-6 flex flex-col justify-center">
            <h3 className="text-slate-400 text-xs font-bold tracking-widest uppercase mb-4">Upcoming Timeline</h3>
            <div className="space-y-4">
               <div className="flex items-center justify-between">
                 <span className="text-slate-300 text-sm">+6 Hours</span>
                 <div className="flex items-center gap-2">
                   <span className="text-slate-100 font-bold">{Math.round(next6)}</span>
                   <span className="text-[10px] text-slate-500 uppercase font-bold">PM2.5</span>
                 </div>
               </div>
               <div className="h-px w-full bg-slate-800/60"></div>
               <div className="flex items-center justify-between">
                 <span className="text-slate-300 text-sm">+12 Hours</span>
                 <div className="flex items-center gap-2">
                   <span className="text-slate-100 font-bold">{Math.round(next12)}</span>
                   <span className="text-[10px] text-slate-500 uppercase font-bold">PM2.5</span>
                 </div>
               </div>
               <div className="h-px w-full bg-slate-800/60"></div>
               <div className="flex items-center justify-between">
                 <span className="text-slate-300 text-sm">+24 Hours</span>
                 <div className="flex items-center gap-2">
                   <span className="text-slate-100 font-bold">{Math.round(next24)}</span>
                   <span className="text-[10px] text-slate-500 uppercase font-bold">PM2.5</span>
                 </div>
               </div>
            </div>
         </div>
      </div>

    </div>
  );
}
