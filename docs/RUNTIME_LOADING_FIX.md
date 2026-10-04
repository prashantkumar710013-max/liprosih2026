# Post-Mortem: Overview Infinite Loading Bug Fix

## Issue Summary
The `Overview` dashboard page and subsequent pages exhibited a critical runtime bug where they became permanently stuck in a "Loading AeroSense Data..." state when deployed/previewed in certain environments, despite the FastAPI backend running successfully on `127.0.0.1:8000`.

## Root Cause Analysis
The failure was the compounding result of two specific misconfigurations:

### 1. IPv6 vs IPv4 `localhost` resolution (`ERR_CONNECTION_REFUSED`)
In modern operating systems and browsers, the hostname `localhost` aggressively attempts to resolve to the IPv6 loopback `[::1]`. However, the FastAPI `uvicorn` instance was instantiated explicitly bound to the IPv4 loopback `127.0.0.1`. When the frontend's Axios client made requests to `http://localhost:8000/api/...`, the browser routed them to `[::1]:8000`, which was rejected (Connection Refused) because the backend was not listening on IPv6.

### 2. Silent Asynchronous Promise Failures
The React frontend executed its initial API fetch operations (such as `fetchCurrent`, `fetchAtmosphericRisk`, and `fetchForecastLive`) within a `Promise.all` block. The `.catch()` block for this promise was implemented as `.catch(console.error)`. Because `setLoading(false)` was only called inside the `.then()` fulfillment block, the rejected promise caused the execution path to skip disabling the loading state. Consequently, the UI was completely bricked in the loading skeleton with no user-facing indication of a network failure.

## Affected Files
1. `frontend/src/api.ts` (API Base URL configuration)
2. `frontend/src/pages/Overview.tsx` (Loading state mismanagement)
3. `frontend/src/pages/AtmosphericIntelligence.tsx`
4. `frontend/src/pages/ExplainableAI.tsx`
5. `frontend/src/pages/Forecast.tsx`
6. `frontend/src/pages/MapPage.tsx`
7. `frontend/src/pages/PollutionEvents.tsx`
8. `frontend/src/pages/ScenarioLab.tsx`

## The Fix

### Step 1: Explicit IPv4 Binding
I updated the Axios client configuration in `frontend/src/api.ts` to strictly route traffic to the IPv4 loopback interface:
```typescript
// Before
const API_BASE_URL = 'http://localhost:8000/api';
// After
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

### Step 2: Robust Error State Handling
I implemented proper React error boundaries for the loading states. Across all pages, the `.catch` blocks were refactored to disable the loading spinner and populate a human-readable error state. For example, in `Overview.tsx`:
```typescript
.catch(err => {
  console.error(err);
  setError(err.message || 'Unknown error');
  setLoading(false);
});
```
This forces the UI to render a clear fallback box (`Error loading data. Please ensure the FastAPI backend is running at http://127.0.0.1:8000.`) instead of hanging indefinitely if the backend is genuinely offline.

## Validation & Verification
- **Backend Integrity:** `pytest` executed successfully (78/78 passing), confirming the backend routes (`/api/current`, `/api/forecast/live`, `/api/atmospheric-risk`) were fully intact.
- **Frontend Compilation:** `npm run build` completed with zero TypeScript warnings or Vite bundle errors.
- **Runtime Test:** Tested the `/` endpoint. The `fetchCurrent` data correctly propagates. Historical Data Mode logic properly handles the UI visualization without hanging.
