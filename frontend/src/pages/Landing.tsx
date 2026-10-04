import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, Wind, Activity, Zap } from 'lucide-react';

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 flex flex-col relative overflow-hidden">
      {/* Background atmospheric effect */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-900/20 rounded-full blur-[128px] mix-blend-screen"></div>
        <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-emerald-900/10 rounded-full blur-[128px] mix-blend-screen"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-slate-900/50 rounded-full blur-[120px] mix-blend-screen"></div>
      </div>

      {/* Navbar */}
      <nav className="relative z-10 px-8 py-6 flex justify-between items-center border-b border-slate-800/50 bg-slate-950/50 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
            <Wind className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight text-slate-100">
            Lipro <span className="text-blue-500">Delhi</span>
          </span>
        </div>
        <div className="hidden md:flex gap-6 text-sm font-medium text-slate-400">
          <button onClick={() => navigate('/overview')} className="hover:text-blue-400 transition-colors">Platform</button>
          <button onClick={() => navigate('/data')} className="hover:text-blue-400 transition-colors">Methodology</button>
        </div>
      </nav>

      {/* Hero Content */}
      <main className="relative z-10 flex-1 flex flex-col items-center justify-center px-6 text-center max-w-5xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-900/30 border border-blue-800/50 text-blue-400 text-xs font-semibold tracking-wide uppercase mb-8 animate-fade-in-up">
          <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
          Environmental Intelligence Platform
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-br from-slate-100 via-slate-300 to-slate-500 mb-6">
          Delhi's Air.<br />
          <span className="text-blue-400">Understood Before It Happens.</span>
        </h1>
        
        <p className="text-lg md:text-xl text-slate-400 max-w-2xl mb-12 leading-relaxed">
          Lipro combines air-quality observations, weather conditions, machine learning, and explainable AI to understand and forecast pollution across Delhi-NCR.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <button 
            onClick={() => navigate('/overview')}
            className="group px-8 py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-semibold transition-all shadow-[0_0_40px_-10px_rgba(37,99,235,0.5)] hover:shadow-[0_0_60px_-15px_rgba(37,99,235,0.7)] flex items-center justify-center gap-2"
          >
            Explore Live Intelligence
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
          <button 
            onClick={() => navigate('/forecast')}
            className="px-8 py-4 bg-slate-800/50 hover:bg-slate-800 text-slate-200 border border-slate-700 rounded-xl font-semibold transition-all backdrop-blur-sm flex items-center justify-center gap-2"
          >
            <Activity className="w-4 h-4 text-slate-400" />
            View Forecast
          </button>
        </div>

        {/* Feature Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-24 text-left w-full border-t border-slate-800/50 pt-12">
          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/50 backdrop-blur-sm">
            <Activity className="w-6 h-6 text-blue-400 mb-4" />
            <h3 className="text-slate-200 font-semibold mb-2">72-Hour Forecasting</h3>
            <p className="text-sm text-slate-500">XGBoost MultiOutputRegressor predicting PM2.5, PM10, and AQI up to 3 days ahead.</p>
          </div>
          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/50 backdrop-blur-sm">
            <Zap className="w-6 h-6 text-emerald-400 mb-4" />
            <h3 className="text-slate-200 font-semibold mb-2">Explainable AI (SHAP)</h3>
            <p className="text-sm text-slate-500">Transparent AI that explains exactly which meteorological factors are driving pollution changes.</p>
          </div>
          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/50 backdrop-blur-sm">
            <Wind className="w-6 h-6 text-indigo-400 mb-4" />
            <h3 className="text-slate-200 font-semibold mb-2">Multi-Source Ingestion</h3>
            <p className="text-sm text-slate-500">Fuses real-time sensor data with continuous atmospheric proxy models for ultimate reliability.</p>
          </div>
        </div>
      </main>
    </div>
  );
}
