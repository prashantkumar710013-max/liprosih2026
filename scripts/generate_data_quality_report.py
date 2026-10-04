import os
import sys

# Add backend to path so we can import from app
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.data.loaders import DataLoader
from app.data.normalizer import DataNormalizer
from app.data.validator import DataValidator
import pandas as pd

def generate_report():
    loader = DataLoader()
    normalizer = DataNormalizer()
    validator = DataValidator()
    
    datasets = [
        "data/source/project_1/AQI_Anand_Vihar_Nov2017-Nov2021.xlsx",
        "data/source/project_1/AQI_Punjabi_Bagh_Jun2015-Nov2021_hourly.xlsx",
        "data/source/project_1/Delhi_Weather_report_June2015-November2021_hourly.xlsx",
        "data/source/project_2/delhi_air_quality_hourly_2023_2025.csv",
        "data/source/project_2/delhi_weather_daily_2023_2025.csv"
    ]
    
    report_lines = [
        "# AeroSense Delhi - Data Quality Report",
        "",
        "## Overview",
        "This report summarizes the data quality for the historical (2015-2021) and recent (2023-2025) datasets.",
        "Note the gap in data for the year 2022.",
        ""
    ]
    
    for filepath in datasets:
        full_path = os.path.join(os.path.dirname(__file__), '..', filepath)
        if not os.path.exists(full_path):
            report_lines.append(f"### Dataset: {os.path.basename(filepath)}")
            report_lines.append("File not found.")
            report_lines.append("")
            continue
            
        try:
            df, metadata = loader.load_dataset(full_path)
            df_norm = normalizer.normalize(df)
            val_report = validator.validate(df_norm)
            
            report_lines.append(f"### Dataset: {metadata['source_file']}")
            report_lines.append(f"- **Records**: {len(df)}")
            report_lines.append(f"- **Columns**: {len(df.columns)}")
            
            if 'timestamp' in df_norm.columns:
                date_min = df_norm['timestamp'].min()
                date_max = df_norm['timestamp'].max()
                report_lines.append(f"- **Date Range**: {date_min} to {date_max}")
            
            # Missing percentage
            total_cells = df_norm.size
            total_missing = df_norm.isna().sum().sum()
            missing_pct = (total_missing / total_cells) * 100 if total_cells > 0 else 0
            report_lines.append(f"- **Missing Percentage**: {missing_pct:.2f}%")
            
            # Duplicate count
            dup_count = df_norm.duplicated().sum()
            report_lines.append(f"- **Duplicate Count**: {dup_count}")
            
            # Stations
            station_count = 1
            if 'station' in df_norm.columns:
                station_count = df_norm['station'].nunique()
            report_lines.append(f"- **Station Count**: {station_count}")
            
            # Pollutant availability
            pollutants = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'aqi']
            available_pols = [p for p in pollutants if p in df_norm.columns]
            report_lines.append(f"- **Pollutant Availability**: {', '.join(available_pols) if available_pols else 'None'}")
            
            # Weather availability
            weather = ['temperature', 'humidity', 'wind_speed', 'wind_direction', 'pressure', 'precipitation']
            available_wx = [w for w in weather if w in df_norm.columns]
            report_lines.append(f"- **Weather Availability**: {', '.join(available_wx) if available_wx else 'None'}")
            
            if val_report['flags']:
                report_lines.append("\n**Quality Flags:**")
                for flag in val_report['flags']:
                    report_lines.append(f"- {flag}")
            
            report_lines.append("")
            
        except Exception as e:
            report_lines.append(f"### Dataset: {os.path.basename(filepath)}")
            report_lines.append(f"Error processing: {str(e)}")
            report_lines.append("")

    out_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'DATA_QUALITY_REPORT.md')
    with open(out_path, 'w') as f:
        f.write('\n'.join(report_lines))
        
    print(f"Report generated at {out_path}")

if __name__ == "__main__":
    generate_report()
