import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, Map as MapIcon, CloudRain, Activity, 
  Database, Settings, AlertTriangle, Route as RouteIcon, 
  Bell, MapPin, Clock, Server, CheckCircle2, AlertCircle 
} from 'lucide-react';
import { fetchSourceHealth } from './api';

import Landing from './pages/Landing';
import Overview from './pages/Overview';
import Forecast from './pages/Forecast';
import MapPage from './pages/MapPage';
import AtmosphericIntelligence from './pages/AtmosphericIntelligence';
import ScenarioLab from './pages/ScenarioLab';
import DataModel from './pages/DataModel';
import TechnicalMode from './pages/TechnicalMode';

const navItems = [
  { path: '/overview', label: 'Overview', icon: LayoutDashboard },
  { path: '/map', label: 'Live Intelligence', icon: MapIcon },
  { path: '/forecast', label: 'Forecast', icon: Activity },
  { path: '/atmosphere', label: 'AI Insights', icon: CloudRain },
  { path: '/scenario', label: 'Scenario Lab', icon: RouteIcon },
  { path: '/data', label: 'Data & System', icon: Database },
];

function DashboardShell({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  const [health, setHealth] = useState<any>(null);
  const [time, setTime] = useState(new Date());
  
  useEffect(() => {
    fetchSourceHealth().then(setHealth).catch(console.error);
    const timer = setInterval(() => setTime(new Date()), 60000);
    return () => clearInterval(timer);
  }, [location.pathname]);

  const currentPage = navItems.find(i => i.path === location.pathname)?.label || 
                      (location.pathname === '/technical' ? 'Technical Mode' : 'Lipro');

  const aqStatus = health?.air_quality?.status;
  const isLive = aqStatus === 'LIVE' || aqStatus === 'RECENT';

  return (
    <div className="flex h-screen bg-[#0B1120] text-slate-300 font-sans selection:bg-blue-500/30">
      {/* Left Sidebar */}
      <aside className="w-64 bg-slate-950/50 backdrop-blur-xl border-r border-slate-800/60 flex flex-col shrink-0 hidden md:flex">
        <div className="p-6 border-b border-slate-800/60">
          <h1 className="text-2xl font-bold tracking-tight text-slate-100 flex items-center gap-2">
            Li<span className="text-blue-500">pro</span>
          </h1>
          <p className="text-[10px] text-slate-400 mt-1 uppercase tracking-widest font-semibold">Delhi NCR</p>
        </div>
        
        <nav className="flex-1 overflow-y-auto py-6 px-4 flex flex-col gap-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600/10 text-blue-400 border border-blue-500/20 shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)]'
                    : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200 border border-transparent'
                }`
              }
            >
              <item.icon className="w-4 h-4 mr-3 opacity-80" />
              {item.label}
            </NavLink>
          ))}
        </nav>

        {/* Bottom Sidebar */}
        <div className="p-4 border-t border-slate-800/60 bg-slate-950/30">
          <div className="flex items-center justify-between mb-4">
             <div className="flex items-center gap-2">
               {isLive ? (
                 <CheckCircle2 className="w-4 h-4 text-emerald-500" />
               ) : (
                 <AlertCircle className="w-4 h-4 text-amber-500" />
               )}
               <span className="text-xs font-semibold text-slate-400">System Status</span>
             </div>
             <span className={`text-[10px] uppercase font-bold px-1.5 py-0.5 rounded ${isLive ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'}`}>
                {isLive ? 'ONLINE' : 'DEGRADED'}
             </span>
          </div>

          <NavLink
            to="/technical"
            className={({ isActive }) =>
              `flex items-center px-3 py-2 rounded-xl text-xs font-medium transition-all border ${
                isActive
                  ? 'bg-slate-800 border-slate-600 text-slate-200'
                  : 'bg-slate-900 border-slate-800 text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`
            }
          >
            <Settings className="w-3.5 h-3.5 mr-2 opacity-80" />
            Technical Mode
          </NavLink>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        {/* Top Bar */}
        <header className="bg-slate-950/30 backdrop-blur-md border-b border-slate-800/60 px-6 py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center z-20">
          <div className="flex items-center gap-4">
            <h2 className="text-lg font-semibold text-slate-100">{currentPage}</h2>
          </div>
          
          <div className="mt-3 sm:mt-0 flex items-center gap-6 text-sm">
             <div className="flex items-center gap-2 text-slate-400">
                <MapPin className="w-4 h-4 text-blue-500" />
                <span className="text-xs font-medium">Delhi-NCR</span>
             </div>
             
             <div className="flex items-center gap-2 text-slate-400">
                <Clock className="w-4 h-4 text-slate-500" />
                <span className="text-xs font-medium">{time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
             </div>

             <div className="flex items-center gap-3 pl-4 border-l border-slate-800">
                <button className="relative text-slate-400 hover:text-slate-200 transition-colors">
                  <Bell className="w-4 h-4" />
                  <span className="absolute -top-1 -right-1 w-2 h-2 bg-blue-500 rounded-full"></span>
                </button>
             </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-4 md:p-8 bg-gradient-to-br from-[#0B1120] to-[#0F172A]">
          {children}
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/*" element={
          <DashboardShell>
            <Routes>
              <Route path="/overview" element={<Overview />} />
              <Route path="/forecast" element={<Forecast />} />
              <Route path="/atmosphere" element={<AtmosphericIntelligence />} />
              <Route path="/map" element={<MapPage />} />
              <Route path="/scenario" element={<ScenarioLab />} />
              <Route path="/data" element={<DataModel />} />
              <Route path="/technical" element={<TechnicalMode />} />
            </Routes>
          </DashboardShell>
        } />
      </Routes>
    </Router>
  );
}

export default App;
