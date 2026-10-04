import React from 'react';

export function FreshnessBadge({ timestamp, status }: { timestamp?: string, status?: string }) {
  if (!timestamp) {
    return (
      <div className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-slate-500">
        <span className="w-1.5 h-1.5 rounded-full bg-slate-500"></span>
        Unavailable
      </div>
    );
  }

  const ageMs = Date.now() - new Date(timestamp).getTime();
  const ageMinutes = Math.floor(ageMs / 60000);

  // If status comes from OpenAQ as AUTHENTICATION_FAILED or STALE
  if (status === 'AUTHENTICATION_FAILED') {
    return (
      <div className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-red-400">
        <span className="w-1.5 h-1.5 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)]"></span>
        Unavailable
      </div>
    );
  }
  
  if (status === 'LIVE_DATA_STALE') {
    return (
      <div className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-amber-400">
        <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.8)]"></span>
        Stale ({ageMinutes}m)
      </div>
    );
  }

  if (ageMinutes < 60) {
    return (
      <div className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-emerald-400">
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span>
        Fresh ({ageMinutes}m)
      </div>
    );
  } else if (ageMinutes < 180) {
    return (
      <div className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-yellow-400">
        <span className="w-1.5 h-1.5 rounded-full bg-yellow-500 shadow-[0_0_8px_rgba(234,179,8,0.8)]"></span>
        Delayed ({Math.floor(ageMinutes/60)}h)
      </div>
    );
  } else {
    return (
      <div className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-orange-400">
        <span className="w-1.5 h-1.5 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.8)]"></span>
        Stale ({Math.floor(ageMinutes/60)}h)
      </div>
    );
  }
}
