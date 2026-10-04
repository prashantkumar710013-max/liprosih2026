import datetime
from typing import Dict, Any

class ProvenanceTracker:
    def __init__(self):
        self.records = []

    def track(
        self,
        source_dataset: str,
        source_file: str,
        source_period: str,
        station: str,
        processing_version: str
    ) -> Dict[str, Any]:
        """
        Creates a provenance record for a processed dataset.
        """
        record = {
            "source_dataset": source_dataset,
            "source_file": source_file,
            "source_period": source_period,
            "station": station,
            "processing_version": processing_version,
            "processing_timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
        self.records.append(record)
        return record
