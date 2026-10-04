# Frontend Architecture

## Stack Overview
The AeroSense Delhi dashboard is built using:
- **React 19**
- **TypeScript**
- **Vite**
- **Tailwind CSS v4**
- **React Router** for declarative navigation.
- **Recharts** for timeseries data visualization.
- **Leaflet & React-Leaflet** for spatial mapping.

## Component Structure
The UI uses a modular structure anchored by a persistent sidebar (`App.tsx` router).
All data fetch operations are centralized in `src/api.ts` which provides typed abstractions wrapping Axios.

## API Integration Strategy
The frontend acts strictly as a presentation layer. It does not contain domain logic for air quality forecasting.
- It interfaces with the FastAPI backend exposed at `http://localhost:8000/api`.
- It implements defensive rendering for `NaN`, `null`, and `undefined` responses.
- It leverages a universal `DataStatusBanner` component that parses the `mode` and `status` flags returned by `LiveFeatureBuilder` endpoints to warn users if underlying data is stale.
