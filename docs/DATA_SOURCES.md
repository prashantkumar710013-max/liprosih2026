# Live Data Sources

1. **Air Quality:** OpenAQ API v3. 
   - Utilizes standard standard endpoints.
   - Pollutants queried: PM2.5, PM10, NO2, SO2, O3, CO.
   
2. **Weather:** Open-Meteo.
   - Provides free access to current meteorological data (Temperature, Humidity, Wind).
   - Note: Open-Meteo is explicitly utilized as a reliable global weather proxy, as IMD live automated scraping often violates TOS or lacks a stable public developer JSON REST API.


**Note on OpenAQ Status:** OpenAQ integration is implemented, but the currently configured OpenAQ account is suspended and therefore current external air-quality observations cannot presently be retrieved through that account. The platform degrades gracefully to Historical Fallback.
