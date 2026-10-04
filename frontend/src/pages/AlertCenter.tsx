import React, { useEffect, useState } from 'react';
import { fetchAlerts } from '../api';
import { AlertTriangle, Clock } from 'lucide-react';

export default function AlertCenter() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetchAlerts().then(setData);
  }, []);

  if (!data) return <div>Loading Alerts...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-800">Alert Center</h1>
      <p className="text-slate-500">Predictive warnings generated from the 72-hour forecast trajectory.</p>
      
      <div className="bg-white p-6 rounded-xl border border-slate-100 shadow-sm">
        {data.alerts.length === 0 ? (
          <div className="text-slate-500 italic">No forecast alerts at this time.</div>
        ) : (
          <div className="space-y-4">
            {data.alerts.map((a: any, i: number) => (
              <div key={i} className={`border-l-4 p-4 rounded-r-md ${
                a.severity === 'CRITICAL' || a.severity === 'HAZARDOUS' || a.severity === 'VERY UNHEALTHY'
                  ? 'border-red-600 bg-red-50' 
                  : 'border-orange-500 bg-orange-50'
              }`}>
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-slate-800 text-lg flex items-center">
                      <AlertTriangle className="w-5 h-5 mr-2 text-red-500" />
                      {a.alert_type.replace(/_/g, ' ')}
                    </h3>
                    <p className="text-slate-700 mt-2">{a.message}</p>
                    <div className="text-xs text-slate-500 flex items-center mt-2 font-semibold">
                      <Clock className="w-3 h-3 mr-1" /> Expected Horizon: +{a.horizon}h
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`px-3 py-1 text-xs font-bold rounded-full ${
                      a.severity === 'CRITICAL' ? 'bg-red-200 text-red-900' : 'bg-orange-200 text-orange-900'
                    }`}>
                      SEVERITY: {a.severity}
                    </span>
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
