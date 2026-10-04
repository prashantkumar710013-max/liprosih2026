# Transport Approximation Methodology

## Overview
The `AeroSenseRapidTransportModel` provides a fast, simplified advection proxy for estimating regional pollution plume trajectories.

## Capabilities & Implementation
- Estimates the 2D advection of a point-source plume over a specified duration (hours).
- Travels in the opposite direction of the meteorological wind direction vector (i.e. if wind is 270/West, plume travels to 90/East).
- Returns a GeoJSON LineString (centerline) and point properties estimating lateral Gaussian dispersion.

## Limitations & Assumptions
- **NOT WRF-Chem:** This is *not* a numerical weather prediction or advanced chemical transport model.
- **Constant Wind Field:** Assumes the current surface wind vector remains constant over the duration of the transport.
- **No Terrain:** Does not account for topographical barriers, building-level CFD, or boundary layer fluctuations.
- **Uncertainty:** High uncertainty beyond 6 hours of transport.
- **Status:** Labeled explicitly as `SIMPLIFIED ADVECTION PROXY`.
