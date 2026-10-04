# UI Data Provenance

## Provenance Enforcement
Because air quality datasets blend real observations, legacy data, simulated predictions, and derived proxies, the UI employs a strict Data Provenance taxonomy. This taxonomy guarantees scientific transparency and prevents hallucinated data claims.

## Provenance Types

1. **OBSERVED / LIVE_DATA_VALID**
   - **Color:** Emerald
   - **Meaning:** Data represents actual, verified real-time telemetry from an external source (e.g., OpenAQ).

2. **HISTORICAL / HISTORICAL_FALLBACK**
   - **Color:** Amber
   - **Meaning:** Due to stale upstream APIs, the system has reverted to a historical reference dataset to allow the application to function in demonstration mode.

3. **STALE / LIVE_DATA_STALE**
   - **Color:** Rose/Red
   - **Meaning:** The cached live observation is older than the `LIVE_DATA_MAX_AGE_MINUTES` threshold.

4. **MODEL_FORECAST / PROXY / SIMPLIFIED ADVECTION PROXY**
   - **Color:** Indigo
   - **Meaning:** Output is the direct product of the XGBoost ML model or a meteorological approximation. It is a prediction, not an observation.

5. **SCENARIO / SIMULATED**
   - **Color:** Fuchsia
   - **Meaning:** Data is the product of a "What-If" intervention in the Scenario Lab. It does not represent actual reality.

## Reusable Component
The `ProvenanceBadge` React component accepts a `status` prop and automatically routes it to the corresponding color palette and Lucide icon.
