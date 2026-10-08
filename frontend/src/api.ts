import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchCurrent = async (station = 'Delhi_Avg') => {
  const res = await api.get(`/current?station=${station}`);
  return res.data;
};

export const fetchForecastLive = async (station = 'Delhi_Avg', hours = 72, pollutant = 'pm25') => {
  const res = await api.get(`/forecast/live?station=${station}&hours=${hours}&pollutant=${pollutant}`);
  return res.data;
};

export const fetchAtmosphericRisk = async (station = 'Delhi_Avg') => {
  const res = await api.get(`/atmospheric-risk?station=${station}`);
  return res.data;
};

export const fetchInversionProxy = async (station = 'Delhi_Avg') => {
  const res = await api.get(`/inversion-proxy?station=${station}`);
  return res.data;
};

export const fetchEvents = async (station = 'Delhi_Avg') => {
  const res = await api.get(`/events?station=${station}`);
  return res.data;
};

export const fetchAlerts = async (station = 'Delhi_Avg') => {
  const res = await api.get(`/alerts?station=${station}`);
  return res.data;
};

export const fetchExplain = async (station = 'Delhi_Avg') => {
  const res = await api.get(`/forecast/explanation?station=${station}`);
  return res.data;
};

export const fetchMapData = async () => {
  const res = await api.get('/map-data');
  return res.data;
};

export const fetchTransport = async (station = 'Delhi_Avg', lat = 28.6, lon = 77.2, duration = 12) => {
  const res = await api.get(`/transport?station=${station}&lat=${lat}&lon=${lon}&duration_hours=${duration}`);
  return res.data;
};

export const postScenario = async (station = 'Delhi_Avg', scenario_name: string) => {
  const res = await api.post('/scenario', { station, scenario_name, hours: 72 });
  return res.data;
};

export const postWhatIf = async (station = 'Delhi_Avg', modifications: Record<string, number>) => {
  const res = await api.post('/what-if', { station, hours: 72, modifications });
  return res.data;
};

export const fetchBiomassFires = async () => {
  const res = await api.get('/biomass-fires');
  return res.data;
};

export const fetchSourceHealth = async () => {
  const res = await api.get('/source-health');
  return res.data;
};

export const fetchModelMetrics = async () => {
  const res = await api.get('/model-metrics');
  return res.data;
};

