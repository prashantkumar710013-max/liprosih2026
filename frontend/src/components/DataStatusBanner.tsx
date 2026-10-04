import React from 'react';
import { AlertTriangle, Activity } from 'lucide-react';

interface DataStatusBannerProps {
  mode: string;
  status: string;
  timestamp?: string;
}

export const DataStatusBanner: React.FC<DataStatusBannerProps> = ({ mode, status, timestamp }) => {
  if (status === 'LIVE_DATA_STALE' || mode === 'HISTORICAL_FALLBACK') {
    return (
      <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl shadow-sm">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <AlertTriangle className="h-5 w-5 text-amber-600 mt-0.5" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-bold text-amber-800">
              Historical Data Mode
            </h3>
            <div className="mt-1 text-sm text-amber-700">
              <p>
                Current Delhi observations from the configured external source are unavailable. Lipro is using validated historical data for demonstration and forecasting.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  } else if (status === 'LIVE_DATA_VALID' || status === 'LIVE') {
    let timeText = 'recently';
    if (timestamp) {
       const obs = new Date(timestamp);
       const now = new Date();
       const diffMins = Math.max(0, Math.round((now.getTime() - obs.getTime()) / 60000));
       timeText = `${diffMins} minutes ago`;
    }
    return (
      <div className="bg-emerald-50 border border-emerald-200 p-4 rounded-xl shadow-sm">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <Activity className="h-5 w-5 text-emerald-600 mt-0.5" />
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-bold text-emerald-800">
              LIVE DATA
            </h3>
            <div className="mt-1 text-sm text-emerald-700">
              <p>
                Latest observations received {timeText}.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }
  return null;
};
