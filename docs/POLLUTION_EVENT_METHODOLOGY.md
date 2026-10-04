# Pollution Event Methodology

## Overview
The Pollution Event Engine autonomously tags developing environmental anomalies without requiring manual thresholding from human operators.

## Detection Rules
- **rapid PM2.5 increase:** Triggered when PM2.5 grows by >25% in a single hour and exceeds 100 µg/m³.
- **sustained PM2.5 elevation:** Triggered when PM2.5 remains >150 µg/m³ for 24 consecutive hours.
- **multi-pollutant increase:** Triggered when PM2.5 > 100, PM10 > 150, and NO2 > 50 simultaneously.
- **stagnation-associated buildup:** Triggered when PM2.5 > 150 AND the Atmospheric Trapping Score > 75.
- **rainfall-associated reduction:** Triggered when precipitation > 2.0 mm AND PM2.5 declines by >10%.

## Provenance
Every event strictly tags its `data_status`. If the underlying data relies on the Stale Data gate, it is tagged as `HISTORICAL_FALLBACK` to prevent false confidence.
