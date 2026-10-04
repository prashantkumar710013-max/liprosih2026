from typing import List, Dict, Any

class AlertEngine:
    """
    Generates dynamic alerts based on the forecasted trajectory of pollutants.
    Does NOT use hard-coded alert messages. It dynamically constructs them based on severity and triggers.
    """
    
    def generate_alerts(self, forecast_sequence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of forecasts (e.g. from predictor.py)
        Format expected: [{'horizon': 1, 'prediction': 150, 'risk': 'Moderate', ...}, ...]
        """
        alerts = []
        if not forecast_sequence:
            return alerts
            
        # Detect threshold crossings
        thresholds = [
            {"level": 150, "risk_category": "Unhealthy"},
            {"level": 250, "risk_category": "Very Unhealthy"},
            {"level": 350, "risk_category": "Hazardous"}
        ]
        
        # Track when thresholds are breached
        for threshold in thresholds:
            breach_horizon = None
            for f in forecast_sequence:
                if f.get('prediction', 0) >= threshold['level']:
                    breach_horizon = f
                    break
                    
            if breach_horizon:
                horizon = breach_horizon['horizon']
                target = breach_horizon.get('timestamp', f"+{horizon}h")
                pred = breach_horizon['prediction']
                
                alerts.append({
                    "alert_type": "THRESHOLD_BREACH_WARNING",
                    "severity": threshold['risk_category'].upper(),
                    "message": f"Forecast indicates PM2.5 will exceed {threshold['level']} µg/m³ around {target} (projected {pred} µg/m³).",
                    "horizon": horizon
                })
                
        # Detect prolonged severe events
        # E.g., if PM2.5 stays above 250 for > 12 hours
        severe_count = 0
        for f in forecast_sequence:
            if f.get('prediction', 0) >= 250:
                severe_count += 1
            else:
                severe_count = 0
                
            if severe_count == 12:
                alerts.append({
                    "alert_type": "PROLONGED_SEVERE_POLLUTION",
                    "severity": "CRITICAL",
                    "message": f"High risk of PM2.5 remaining above 250 µg/m³ for at least 12 consecutive hours starting around +{f['horizon'] - 12}h.",
                    "horizon": f['horizon']
                })
                break # Just alert once for the sequence
                
        return alerts
