# Data Pipeline

The data pipeline for AeroSense Delhi handles two distinct datasets:

1. **Historical Data (2015-2021)**: Sourced from Project 1.
2. **Recent Data (2023-2025)**: Sourced from Project 2.

*Note: There is a logical gap for the year 2022. We do not fabricate or interpolate across this year.*

## Ingestion
- `DataLoader` reads from CSV or Excel.
- Detects encoding using `chardet` (primarily to handle legacy CSV formats).
- Parses timestamps using common time column names (`date`, `time`, `timestamp`, `datetime`, `From Date`).

## Normalization
The `DataNormalizer` addresses schema inconsistencies between Project 1 and Project 2.
- Examples of unification:
  - `PM2.5`, `PM 2.5`, `PM2.5 (ug/m3)` -> `pm25`
  - `Temp`, `Temperature` -> `temperature`
  - `From Date`, `date` -> `timestamp`
- Standardizes all features to numeric types using `pd.to_numeric()`.

## Validation
The `DataValidator` scans the normalized datasets to identify quality issues without automatically destroying data. It generates flags for:
- Missing timestamps.
- Timeline gaps > 1 hour.
- Negative pollutant values (e.g., PM2.5 < 0).
- Extreme values (e.g., Temp > 55C, PM2.5 > 1000).

## Output
Validated outputs and metadata reports are saved or persisted into the database for model consumption.
