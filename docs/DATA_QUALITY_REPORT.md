# AeroSense Delhi - Data Quality Report

## Overview
This report summarizes the data quality for the historical (2015-2021) and recent (2023-2025) datasets.
Note the gap in data for the year 2022.

### Dataset: AQI_Anand_Vihar_Nov2017-Nov2021.xlsx
- **Records**: 31684
- **Columns**: 9
- **Date Range**: 2017-11-01 01:00:00 to 2021-11-30 23:00:00
- **Missing Percentage**: 13.79%
- **Duplicate Count**: 0
- **Station Count**: 1
- **Pollutant Availability**: pm25, pm10, no2, so2, co
- **Weather Availability**: None

**Quality Flags:**
- Found 1386 potential gaps in timeline

### Dataset: AQI_Punjabi_Bagh_Jun2015-Nov2021_hourly.xlsx
- **Records**: 48764
- **Columns**: 9
- **Date Range**: 2015-04-10 00:00:00 to 2021-11-27 23:00:00
- **Missing Percentage**: 13.89%
- **Duplicate Count**: 0
- **Station Count**: 1
- **Pollutant Availability**: pm25, pm10, no2, so2, co
- **Weather Availability**: None

**Quality Flags:**
- Found 2037 potential gaps in timeline

### Dataset: Delhi_Weather_report_June2015-November2021_hourly.xlsx
- **Records**: 97137
- **Columns**: 11
- **Missing Percentage**: 36.36%
- **Duplicate Count**: 0
- **Station Count**: 1
- **Pollutant Availability**: None
- **Weather Availability**: temperature, wind_speed, wind_direction

**Quality Flags:**
- Time column timestamp not found

### Dataset: delhi_air_quality_hourly_2023_2025.csv
- **Records**: 26304
- **Columns**: 7
- **Date Range**: 2023-01-01 00:00:00 to 2025-12-31 23:00:00
- **Missing Percentage**: 0.00%
- **Duplicate Count**: 0
- **Station Count**: 1
- **Pollutant Availability**: pm10
- **Weather Availability**: None

### Dataset: delhi_weather_daily_2023_2025.csv
- **Records**: 1096
- **Columns**: 5
- **Date Range**: 2023-01-01 00:00:00 to 2025-12-31 00:00:00
- **Missing Percentage**: 0.00%
- **Duplicate Count**: 0
- **Station Count**: 1
- **Pollutant Availability**: None
- **Weather Availability**: None

**Quality Flags:**
- Found 1095 potential gaps in timeline
