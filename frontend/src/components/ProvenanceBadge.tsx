import React from 'react';
import { Database, Clock, BrainCircuit, Activity, TestTube2, AlertCircle } from 'lucide-react';

interface ProvenanceBadgeProps {
  status: string;
}

export const ProvenanceBadge: React.FC<ProvenanceBadgeProps> = ({ status }) => {
  let color = 'bg-slate-100 text-slate-800 border-slate-200';
  let Icon = Database;
  
  const rawStatus = status?.toUpperCase() || 'UNKNOWN';
  let displayText = rawStatus;

  switch (rawStatus) {
    case 'OBSERVED':
    case 'LIVE_DATA_VALID':
      color = 'bg-emerald-50 text-emerald-700 border-emerald-200';
      Icon = Activity;
      displayText = 'Observed Live';
      break;
    case 'HISTORICAL':
    case 'HISTORICAL_FALLBACK':
      color = 'bg-amber-50 text-amber-700 border-amber-200';
      Icon = Clock;
      displayText = 'Historical Data Mode';
      break;
    case 'STALE':
    case 'LIVE_DATA_STALE':
      color = 'bg-rose-50 text-rose-700 border-rose-200';
      Icon = AlertCircle;
      displayText = 'Current Data Unavailable';
      break;
    case 'MODEL_FORECAST':
      color = 'bg-indigo-50 text-indigo-700 border-indigo-200';
      Icon = BrainCircuit;
      displayText = 'Forecast';
      break;
    case 'DERIVED':
    case 'PROXY':
      color = 'bg-indigo-50 text-indigo-700 border-indigo-200';
      Icon = BrainCircuit;
      displayText = 'Model Estimate';
      break;
    case 'SIMPLIFIED ADVECTION PROXY':
      color = 'bg-indigo-50 text-indigo-700 border-indigo-200';
      Icon = BrainCircuit;
      displayText = 'Transport Estimate';
      break;
    case 'SCENARIO':
    case 'SIMULATED':
      color = 'bg-fuchsia-50 text-fuchsia-700 border-fuchsia-200';
      Icon = TestTube2;
      displayText = 'Simulated Scenario';
      break;
  }

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${color}`} title={`Technical Provenance: ${rawStatus}`}>
      <Icon className="w-3 h-3 mr-1" />
      {displayText}
    </span>
  );
};
