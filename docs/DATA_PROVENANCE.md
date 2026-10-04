# Data Provenance

The provenance tracker ensures we maintain an unbroken chain of custody for all datasets used in model training. This guarantees reproducibility and transparency.

## Tracked Attributes
Each processed dataset creates a provenance record containing:

- **source_dataset**: High-level origin (e.g., "Project 1", "Project 2").
- **source_file**: Exact filename of the original raw file (e.g., `delhi_air_quality_hourly_2023_2025.csv`).
- **source_period**: The timeline range covered (e.g., "2023-2025").
- **station**: Specific station (e.g., "Anand Vihar") or "All".
- **processing_version**: Pipeline version used to clean the data.
- **processing_timestamp**: UTC timestamp of when the data was processed.

By tracking these attributes, any anomaly found during model evaluation can be traced back to the exact version of the processing script and the original raw file.
