# OpenAQ Access Status

## Current Status
**AUTHENTICATION_FAILED / ACCOUNT SUSPENDED**

## Observed HTTP/Authentication Behavior
The configured OPENAQ_API_KEY (kept securely in .env) returns a strict HTTP 401 Unauthorized with the payload {"detail":"Invalid credentials"}. An independent validation confirmed that the associated OpenAQ account is currently displaying: *"API usage for this account has been temporarily suspended due to violation of the platform Terms of Use."*

## Effect on AeroSense
Live Delhi NCR pollutant ingestion via ackend/app/services/ingestion.py is currently blocked. No new observations can be pulled from the https://api.openaq.org/v3/locations endpoints. 

## Fallback Behavior
AeroSense's architecture gracefully degraded into its scientific failsafe:
- **NO_CURRENT_DATA_AFTER_DYNAMIC_AUDIT** was correctly detected.
- The system automatically rolled over into **HISTORICAL_FALLBACK** mode. 
- The UI actively restricts the usage of the term "Live" and explicitly labels all charts as HISTORICAL_FALLBACK and MODEL_FORECAST.

## Recovery Procedure
The OpenAQ architecture (OpenAQAdapter) was intentionally preserved. Once the account suspension is resolved or a new API key is provided and saved inside .env, the system will automatically re-engage live dynamic bounding-box polling. No code rewrites are required for restoration.

## Security Precautions
The compromised OPENAQ_API_KEY was audited and confirmed to ONLY exist within the local untracked .env file. It does not exist in .env.example, .gitignore, rontend/, or any system logs.
