# Backend Implementation Plan: FinScythe

This document outlines a detailed plan for building the backend of the FinScythe project, based on the main project specification.

## 1. Directory Structure

The backend will be organized into the following structure to ensure a clear separation of concerns:

```
backend/
├── main.py                 # FastAPI app, main endpoint logic
├── requirements.txt        # Python dependencies
├── .env                    # API keys and environment variables (gitignored)
├── core/
│   ├── config.py           # Loads variables from .env
│   └── cache.py            # Simple in-memory caching for API calls
├── services/
│   ├── financial_data.py   # Fetches data from Alpha Vantage & Finnhub
│   ├── quant_model.py      # GARCH, Monte Carlo, and sentiment modeling
│   └── ai_synthesis.py     # Handles interaction with the Google Gemini API
└── models/
    └── schemas.py          # Pydantic models for data validation & response structure
```

## 2. Component Breakdown

### `main.py` (The Orchestrator)
This file will contain the primary FastAPI application and the main `GET /api/stock-data` endpoint.

**Endpoint Logic Flow:**
1.  **Receive Request:** Accept a `ticker` string as a query parameter.
2.  **Check Cache:** Query the in-memory cache (`core/cache.py`) using the ticker. If valid, recent data exists, return it immediately.
3.  **Fetch Data:** If not cached, execute parallel API calls to `services/financial_data.py` to retrieve:
    *   Historical price data (Alpha Vantage).
    *   Analyst news sentiment (Finnhub).
    *   Retail Reddit sentiment (Finnhub).
4.  **Quantitative Analysis:**
    *   Pass the historical price data to `services/quant_model.py` to calculate GARCH volatility and baseline historical drift.
    *   Use the current sentiment scores to calculate the "Overall Market Bias" and adjust the drift accordingly.
5.  **Prediction:**
    *   Execute the Monte Carlo simulation via `services/quant_model.py` using the sentiment-adjusted drift and GARCH volatility to generate the quantitative price prediction.
    *   Determine the general direction of the prediction (e.g., "upward", "downward", "stable").
6.  **AI Synthesis:**
    *   Call the `services/ai_synthesis.py` module, providing it with the sentiment scores, news headlines, and the quantitative prediction's direction to generate the dissonance analysis.
7.  **Assemble & Respond:**
    *   Combine all generated data (prices, sentiments, predictions, AI summary) into the Pydantic response model defined in `models/schemas.py`.
    *   Store the complete response object in the cache with a timestamp.
    *   Return the final JSON object to the client.

### `models/schemas.py`
-   Will contain Pydantic models that strictly define the structure of the final JSON response sent to the frontend. This enforces the API contract agreed upon with the frontend developer.

### `core/`
-   **`config.py`**: Uses `python-dotenv` to load API keys (`ALPHA_VANTAGE_API_KEY`, `FINNHUB_API_KEY`, `GOOGLE_API_KEY`) from the `.env` file into a centralized configuration object.
-   **`cache.py`**: Implements a simple dictionary-based, time-aware cache to store results for tickers. This is critical for mitigating API rate-limit risks during development and the demo.

### `services/`
-   **`financial_data.py`**:
    -   Contains distinct functions like `get_price_history(ticker)`, `get_analyst_sentiment(ticker)`, etc.
    -   Each function will be responsible for making a `requests` call to a single external API endpoint and performing basic error handling and data extraction.
-   **`quant_model.py`**:
    -   **`calculate_garch_volatility(returns)`**: Uses the `arch` library to model volatility from historical price returns.
    -   **`determine_market_bias(analyst_score, retail_score)`**: Implements the logic to convert the two sentiment scores into a single "Market Bias" factor.
    -   **`run_monte_carlo(...)`**: The core simulation engine. It will use `numpy` to generate random walks based on the GARCH volatility and sentiment-adjusted drift.
-   **`ai_synthesis.py`**:
    -   Contains a primary function, `get_ai_summary(...)`, that constructs a detailed, structured prompt for the Google Gemini API.
    -   This function will handle the API call and parse the returned JSON to fit the required output structure.

## 3. Setup and Dependencies

-   **`requirements.txt`**: Will be populated with `fastapi`, `uvicorn`, `requests`, `pandas`, `numpy`, `arch`, `google-generativeai`, and `python-dotenv`.
-   **`.env`**: Will be created locally to manage API keys securely.
