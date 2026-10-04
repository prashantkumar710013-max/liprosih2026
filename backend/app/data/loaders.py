import os
import pandas as pd
import chardet
from typing import Optional, Dict, Any, Tuple

class DataLoader:
    def __init__(self):
        pass

    def _detect_encoding(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding'] or 'utf-8'

    def load_dataset(self, file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Loads a CSV or Excel dataset, returns DataFrame and metadata.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        metadata = {
            "source_file": os.path.basename(file_path),
            "file_type": ext,
            "malformed_records": 0
        }

        try:
            if ext == '.csv':
                encoding = self._detect_encoding(file_path)
                # Read without parsing dates initially to handle malformed records if needed
                df = pd.read_csv(file_path, encoding=encoding, on_bad_lines='skip')
                # Count total lines vs dataframe size could be a way to find malformed, but skip does it automatically
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif ext == '.json':
                df = pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file extension: {ext}")
                
            # basic clean column names
            df.columns = [str(c).strip() for c in df.columns]
            
            # parse timestamps if obvious columns exist
            time_cols = ['date', 'time', 'timestamp', 'datetime', 'From Date', 'To Date']
            for c in df.columns:
                if str(c).lower() in time_cols:
                    df[c] = pd.to_datetime(df[c], errors='coerce')
                    
            return df, metadata

        except Exception as e:
            raise ValueError(f"Error loading {file_path}: {str(e)}")
