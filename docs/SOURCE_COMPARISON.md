# Source Comparison

## Comparison of Source Project 1 and Source Project 2

### Overlapping Datasets
- Both projects contain historical PM2.5, PM10, NO2, and SO2 data for Delhi.
- Both projects contain weather variables: Temperature, Wind Speed, Humidity, and Precipitation/Pressure.

### Unique Datasets
- **Project 1**: Contains CO (Carbon Monoxide), traffic congestion data, and station-specific files (Anand Vihar, Punjabi Bagh).
- **Project 2**: Contains Ozone data (`ozone`) and future-looking or expanded multiyear data up to 2025. It also explicitly includes predefined lag and rolling features.

### Common Pollutants
- PM2.5, PM10, NO2, SO2.

### Unique Pollutants
- **Project 1**: CO.
- **Project 2**: Ozone.

### Common Weather Variables
- Temperature, Relative Humidity, Wind Speed.

### Different Date Ranges
- **Project 1**: ~Nov 2017 to Nov 2021.
- **Project 2**: Jan 2023 to Dec 2025.

### Different Sampling Frequencies
- **Project 1**: Mixed. Contains both hourly and daily aggregated files.
- **Project 2**: Contains distinct hourly raw datasets and daily aggregated processed datasets.

### Different Targets
- **Project 1**: PM2.5 or PM10 for the current timestamp (or next step depending on sequence modeling).
- **Project 2**: Explicitly targets `target_pm2_5_next_day` and `risk_category_next_day`.

### Compatible Datasets
- The underlying daily aggregated pollutants (PM2.5, PM10, NO2, SO2) and standard weather features (Temp, RH, Wind Speed) can be combined conceptually if column names and units are standardized.

### Incompatible Datasets
- The date ranges are entirely disjoint (2017-2021 vs. 2023-2025). Direct concatenation would leave a full year gap (2022).
- Station-specific vs. City-wide: Project 1 focuses on specific stations for some data, while Project 2 seems to be city-wide or single-point aggregated.
- Traffic data from Project 1 cannot easily be projected to Project 2's 2023-2025 timeframe without a new data source.

## How They Can Safely Be Combined
1. **Pipeline Reuse**: Project 1's Transformer model architecture and FastAPI deployment can be reused and trained on Project 2's newer, engineered dataset (which includes lags and rolling stats).
2. **Data Standardization**: If a continuous dataset is desired, a new scraper (repurposing Project 1's scraping code) needs to fetch 2022 data, and then merge with Project 1 and Project 2 schemas.
3. **Feature Union**: Combine the feature engineering approach of Project 2 (lags, rolling averages, target next day) with the deep learning model of Project 1 (Transformer).
4. **Isolated usage**: Keep Project 2 data for modern model training, while keeping Project 1 for structural reference (API, Firebase integration, PowerBI).
