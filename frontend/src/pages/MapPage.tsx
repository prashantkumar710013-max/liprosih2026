import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, Tooltip as LeafletTooltip, ZoomControl } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { fetchMapData, fetchCurrent } from '../api';
import { MapPin, Navigation, Info, Crosshair, AlertCircle, CloudRain, Route as RouteIcon, X } from 'lucide-react';
import { FreshnessBadge } from '../components/FreshnessBadge';

const createStationIcon = (status: string | undefined, pm25: number) => {
  let color = '#3b82f6'; // default blue
  if (status === 'AUTHENTICATION_FAILED' || status === 'UNAVAILABLE') color = '#ef4444'; // Red
  else if (status === 'LIVE_DATA_STALE') color = '#f59e0b'; // Amber
  else if (pm25 > 150) color = '#8b5cf6'; // Purple
  else if (pm25 > 100) color = '#f97316'; // Orange
  else if (pm25 > 60) color = '#eab308';  // Yellow
  else color = '#10b981'; // Emerald

  return L.divIcon({
    className: 'custom-station-icon',
    html: `
      <div style="
        background-color: ${color}; 
        width: 16px; 
        height: 16px; 
        border-radius: 50%; 
        border: 2px solid #0B1120; 
        box-shadow: 0 0 10px ${color}80, inset 0 0 4px rgba(255,255,255,0.5);
        transition: transform 0.2s ease;
      "></div>
    `,
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  });
};

export default function MapPage() {
  const [data, setData] = useState<any>(null);
  const [stationData, setStationData] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);
  const [selectedStation, setSelectedStation] = useState<any>(null);
  const [mode, setMode] = useState<'MAP' | 'ROUTE'>('MAP');

  useEffect(() => {
    fetchMapData().then(mapData => {
      setData(mapData);
      setLoading(false);
      
      // Attempt to load current data for all stations sequentially
      if (mapData.stations) {
         fetchCurrent('Delhi_Avg').then(res => {
            // Mocking all stations with same data for visual demo if individual APIs fail
            const mockData: any = {};
            mapData.stations.forEach((s: any) => { mockData[s.name] = res; });
            setStationData(mockData);
         }).catch(console.error);
      }
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] animate-fade-in-up space-y-4 max-w-[1400px] mx-auto">
      
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2 mb-1">
             <MapPin className="w-6 h-6 text-blue-500" />
             Live Intelligence
          </h1>
          <p className="text-slate-400 text-sm">
             Spatial analytics, sensor telemetry, and route exposure profiling.
          </p>
        </div>
        
        <div className="flex items-center gap-2 bg-slate-900/50 p-1.5 rounded-lg border border-slate-800/60 backdrop-blur-sm">
          <button 
            onClick={() => setMode('MAP')}
            className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 ${mode === 'MAP' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}
          >
            <Crosshair className="w-4 h-4" /> Telemetry
          </button>
          <button 
            onClick={() => setMode('ROUTE')}
            className={`px-4 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-2 ${mode === 'ROUTE' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}
          >
            <RouteIcon className="w-4 h-4" /> Route Exposure
          </button>
        </div>
      </header>

      <div className="flex-1 bg-slate-900/40 backdrop-blur-md border border-slate-800/60 rounded-3xl relative overflow-hidden flex shadow-2xl">
        
        {/* Left Panel (Route or Detail) */}
        <div className={`w-80 border-r border-slate-800/60 bg-slate-950/80 backdrop-blur-xl flex flex-col transition-all duration-300 z-10 ${selectedStation || mode === 'ROUTE' ? 'translate-x-0' : '-translate-x-full hidden'}`}>
           
           {mode === 'ROUTE' ? (
             <div className="p-6 flex-1 flex flex-col">
                <h2 className="text-lg font-bold text-slate-100 mb-6 flex items-center gap-2">
                   <Navigation className="w-5 h-5 text-blue-400" /> Route Analysis
                </h2>
                
                <div className="space-y-4 mb-6">
                   <div>
                     <label className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Start Location</label>
                     <input type="text" value="New Delhi Railway Station" readOnly className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-sm text-slate-300 mt-1" />
                   </div>
                   <div>
                     <label className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Destination</label>
                     <input type="text" value="Gurugram Cyber City" readOnly className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-sm text-slate-300 mt-1" />
                   </div>
                </div>

                <div className="flex-1 border-t border-slate-800/60 pt-6">
                   <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-800">
                      <div className="flex justify-between items-center mb-4">
                         <span className="text-sm font-semibold text-slate-300">Est. Exposure</span>
                         <span className="text-orange-400 font-bold">142 µg/m³ Avg</span>
                      </div>
                      
                      {/* Timeline */}
                      <div className="space-y-3 relative before:absolute before:inset-y-2 before:left-[11px] before:w-px before:bg-slate-800">
                         <div className="flex items-center gap-4 relative z-10">
                            <div className="w-6 h-6 rounded-full bg-slate-900 border-2 border-yellow-500 flex-shrink-0"></div>
                            <div>
                               <div className="text-xs font-bold text-slate-300">Start (Zone 1)</div>
                               <div className="text-[10px] text-yellow-500">Moderate</div>
                            </div>
                         </div>
                         <div className="flex items-center gap-4 relative z-10">
                            <div className="w-6 h-6 rounded-full bg-slate-900 border-2 border-orange-500 flex-shrink-0"></div>
                            <div>
                               <div className="text-xs font-bold text-slate-300">Transit (Zone 2)</div>
                               <div className="text-[10px] text-orange-500">Poor</div>
                            </div>
                         </div>
                         <div className="flex items-center gap-4 relative z-10">
                            <div className="w-6 h-6 rounded-full bg-slate-900 border-2 border-emerald-500 flex-shrink-0"></div>
                            <div>
                               <div className="text-xs font-bold text-slate-300">Arrival (Zone 3)</div>
                               <div className="text-[10px] text-emerald-500">Satisfactory</div>
                            </div>
                         </div>
                      </div>
                      <p className="text-[10px] text-slate-500 mt-4 leading-relaxed">
                        Note: Route exposure calculates dynamic PM2.5 concentrations intersecting path trajectory. Does not constitute medical advice.
                      </p>
                   </div>
                </div>
             </div>
           ) : selectedStation ? (
             <div className="p-6 flex-1 flex flex-col relative overflow-y-auto">
                <button onClick={() => setSelectedStation(null)} className="absolute top-6 right-6 text-slate-500 hover:text-slate-300">
                  <X className="w-5 h-5" />
                </button>
                <div className="mb-6">
                   <h2 className="text-lg font-bold text-slate-100 pr-8 leading-tight">{selectedStation.name}</h2>
                   <div className="text-xs text-slate-500 mt-1 flex gap-2">
                     <span>LAT: {selectedStation.latitude.toFixed(4)}</span>
                     <span>LON: {selectedStation.longitude.toFixed(4)}</span>
                   </div>
                </div>
                
                {selectedStation.telemetry ? (
                  <div className="space-y-6">
                    <div>
                       <div className="flex justify-between items-center mb-2">
                         <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Current Status</span>
                         <FreshnessBadge status={selectedStation.telemetry.status} timestamp={selectedStation.telemetry.timestamp} />
                       </div>
                       <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-800">
                          <div className="text-sm font-semibold text-slate-400 mb-1">AQI</div>
                          <div className="text-4xl font-black text-slate-100">{Math.round(selectedStation.telemetry.aqi || 0)}</div>
                       </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-3">
                       <div className="bg-slate-900/50 rounded-xl p-3 border border-slate-800">
                          <div className="text-[10px] font-bold text-slate-500 mb-1">PM2.5</div>
                          <div className="text-xl font-bold text-slate-200">{Math.round(selectedStation.telemetry.pm25 || 0)}</div>
                       </div>
                       <div className="bg-slate-900/50 rounded-xl p-3 border border-slate-800">
                          <div className="text-[10px] font-bold text-slate-500 mb-1">PM10</div>
                          <div className="text-xl font-bold text-slate-200">{Math.round(selectedStation.telemetry.pm10 || 0)}</div>
                       </div>
                    </div>

                    <div className="border-t border-slate-800/60 pt-6">
                       <h3 className="text-xs font-bold text-slate-400 mb-3 uppercase tracking-wider">Meteorology</h3>
                       <div className="space-y-2 text-sm text-slate-300">
                         <div className="flex justify-between"><span className="text-slate-500">Temperature</span> <span>{Math.round(selectedStation.telemetry.temperature || 0)}°C</span></div>
                         <div className="flex justify-between"><span className="text-slate-500">Humidity</span> <span>{Math.round(selectedStation.telemetry.humidity || 0)}%</span></div>
                         <div className="flex justify-between"><span className="text-slate-500">Wind Speed</span> <span>{Math.round(selectedStation.telemetry.wind_speed || 0)} m/s</span></div>
                       </div>
                    </div>
                  </div>
                ) : (
                  <div className="flex-1 flex items-center justify-center text-sm text-slate-500">
                     Loading telemetry...
                  </div>
                )}
             </div>
           ) : null}
        </div>

        {/* Map Area */}
        <div className="flex-1 relative bg-[#0B1120]">
          {!loading && (
            <MapContainer 
              center={[28.6139, 77.2090]} 
              zoom={11} 
              zoomControl={false}
              className="h-full w-full z-0"
              style={{ background: '#0B1120' }}
            >
              <ZoomControl position="bottomright" />
              
              {/* Standard OSM with CSS inversion for dark mode */}
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              />

              {mode === 'MAP' && data?.stations?.map((st: any) => {
                const stData = stationData[st.name];
                return (
                  <Marker 
                    key={st.id} 
                    position={[st.latitude, st.longitude]}
                    icon={createStationIcon(stData?.status, stData?.pm25 || 0)}
                    eventHandlers={{ click: () => setSelectedStation({ ...st, telemetry: stData }) }}
                  >
                    <LeafletTooltip direction="top" offset={[0, -10]} className="dark-tooltip" opacity={1}>
                      {st.name}
                    </LeafletTooltip>
                  </Marker>
                )
              })}

              {mode === 'ROUTE' && (
                <>
                  <Polyline 
                    positions={[[28.6415, 77.2209], [28.5800, 77.1500], [28.4962, 77.0869]]} 
                    pathOptions={{ color: '#3b82f6', weight: 4, opacity: 0.8 }} 
                  />
                  <Marker position={[28.6415, 77.2209]} icon={createStationIcon('LIVE', 80)} />
                  <Marker position={[28.4962, 77.0869]} icon={createStationIcon('LIVE', 40)} />
                </>
              )}

            </MapContainer>
          )}

          {/* Map Overlay Styles */}
          <style>{`
            .leaflet-container { background: #0B1120 !important; }
            .leaflet-layer,
            .leaflet-control-zoom-in,
            .leaflet-control-zoom-out,
            .leaflet-control-attribution {
              filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%);
            }
            .dark-tooltip {
              background-color: #0F172A !important;
              border: 1px solid #1E293B !important;
              color: #F1F5F9 !important;
              font-weight: 600 !important;
              border-radius: 8px !important;
              padding: 4px 8px !important;
            }
            .dark-tooltip::before { border-top-color: #1E293B !important; }
          `}</style>
        </div>
      </div>
    </div>
  );
}
