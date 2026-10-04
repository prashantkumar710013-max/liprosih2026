# SIH Dashboard Guide

## Overview for Evaluators
This guide explains how to navigate the AeroSense Delhi dashboard during the Smart India Hackathon presentation.

## Key Demonstration Points
1. **Historical Fallback State:** Because the OpenAQ telemetry for Delhi NCR is currently halted (latest data Feb 2025), the dashboard explicitly alerts you that it is running in `HISTORICAL_FALLBACK` mode. This is a *feature*, proving the system's robustness against data hallucination.
2. **Atmospheric Intelligence (Proxies):** Instead of making impossible claims about measuring Planetary Boundary Layer (PBL) heights, navigate to the Atmospheric Intelligence tab to demonstrate our Model-Derived Proxies (Trapping Score and Ventilation Index).
3. **Forecast Explainability:** Navigate to the Explainable AI tab. This shows the SHAP driver values explaining exactly *why* the XGBoost model made its current prediction, maximizing trust.
4. **Scenario Lab:** Use the Scenario Lab to prove the model's dynamic capability. Select "BIOMASS_BURNING_SCENARIO" or "RAIN_SCAVENGING" to show how the model instantaneously adjusts its 72-hour forecast based on theoretical interventions.
5. **Pollution Events Engine:** Show how the system autonomously scans historical trajectories to label anomalies without relying on hardcoded static thresholds.
