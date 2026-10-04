# AeroSense Delhi - SIH Demo Script

**Total Time:** 5-7 Minutes
**Objective:** Present AeroSense Delhi as a deeply integrated environmental intelligence platform that goes beyond standard statistical charts.

## 1. The Problem (0:00 - 1:00)
*Action: Display the main Overview dashboard.*
**Script:** 
"Air quality platforms traditionally operate in silos—showing either current pollution, generic weather, or basic linear charts. They fail to explain *why* pollution accumulates. AeroSense Delhi solves this by coupling atmospheric chemistry with meteorological stability in real-time."

## 2. 72-Hour Forecast & Predictability (1:00 - 2:00)
*Action: Navigate to '72-Hour Forecast'. Switch between stations.*
**Script:** 
"This is our 72-hour projection engine. Unlike recurrent models that compound errors by predicting one hour at a time, AeroSense leverages an XGBoost MultiOutputRegressor to forecast the entire 72-hour vector simultaneously, preserving long-term accuracy. The shaded area represents our empirical confidence interval, giving policymakers a reliable worst-case boundary."

## 3. Atmospheric Trapping (2:00 - 3:00)
*Action: Navigate to 'Atmospheric Intel'. Highlight the Trapping Index.*
**Script:** 
"We built a completely novel 'Atmospheric Trapping Index'. Instead of requiring expensive vertical radiosonde balloons to detect inversions, our mathematical proxy analyzes aggressive diurnal temperature drops and absolute wind stagnation to accurately estimate when the atmosphere is locking pollutants near the surface."

## 4. Early Warnings & Events (3:00 - 4:00)
*Action: Open 'Alert Center' and 'Pollution Events'.*
**Script:** 
"The engine continuously scans both the current state and the 72-hour forecast sequence. It autonomously detects structural breakdowns—like concurrent PM2.5 and NO2 spikes—and issues programmatic warnings, entirely replacing hardcoded thresholds with dynamic intelligence."

## 5. Scenario Lab (4:00 - 5:00)
*Action: Open 'Scenario Lab'. Run 'BIOMASS-BURNING SCENARIO'.*
**Script:** 
"To help with actionable policy, we created the Scenario Lab. Watch as we trigger a simulated agricultural biomass burning event in Punjab. The advection-dispersion engine instantly renders the trajectory of the smoke plume, estimating its impact tail and arrival window in Delhi-NCR without requiring heavy supercomputer WRF-Chem runs."

## 6. Transparency (5:00 - 6:00)
*Action: Open 'Explainable AI'.*
**Script:** 
"Finally, policymakers cannot act on a black box. Our integrated SHAP engine deconstructs every forecast on the fly, explicitly ranking which exact meteorological or lagged pollution factors are driving the prediction up or down, proving exactly *why* the forecast was made."
