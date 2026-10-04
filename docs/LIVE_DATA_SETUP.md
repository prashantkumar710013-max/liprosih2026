# Live Data Setup

1. Copy `.env.example` to `.env`.
2. Retrieve a free API Key from `https://openaq.org/developers/`.
3. Paste the key into `OPENAQ_API_KEY`.
4. Ensure `OPENAQ_BASE_URL=https://api.openaq.org/v3`.
5. Start the backend (`uvicorn app.main:app`). The ingestion endpoints are now accessible.

*Note: If no API key is provided, the ingestion service fails gracefully without crashing the app.*
