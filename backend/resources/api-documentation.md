# FinScythe Backend API Documentation

A guide for the frontend team on how to interact with the backend API.

## Running the Backend

First, ensure you have the necessary dependencies installed by running this command in the `backend` directory:
```bash
pip install -r requirements.txt
```
Then, from the **`backend`** directory, run the backend server:
```bash
uvicorn core.apiController:app --reload
```
The API will then be available at `http://127.0.0.1:8000`.

---

## Endpoints

The base URL for all API calls is `http://127.0.0.1:8000`.

### 1. Health Check

-   **URL:** `/`
-   **Method:** `GET`
-   **Purpose:** To check if the backend server is running correctly.

---

### 2. Get Historical Price Data

-   **URL:** `/stock/{ticker}`
-   **Method:** `GET`
-   **Purpose:** Fetches recent historical price data for a given stock ticker.
-   **URL Parameters:**
    -   `ticker` (string, **required**): The stock symbol (e.g., `AAPL`).
-   **Query Parameters:**
    -   `time_period` (integer, **required**): The number of days of history to fetch.
-   **Success Response:**
    ```json
    {
        "ticker": "AAPL",
        "ticker_history": [
            {
                "Datetime": "2025-10-24 09:30:00",
                "Close": 150.12
            }
        ]
    }
    ```

---

### 3. Get Full Sentiment Analysis

-   **URL:** `/sentiment/{ticker}`
-   **Method:** `GET`
-   **Purpose:** Fetches a comprehensive sentiment analysis, combining analyst ratings, social media discussion, and a final confidence-weighted score.
-   **URL Parameters:**
    -   `ticker` (string, **required**): The stock symbol (e.g., `TSLA`).
-   **Success Response:**
    ```json
    {
        "analyst_score": 83,
        "analyst_summary": "Analysts are currently bullish on Tesla, citing strong EV delivery growth...",
        "social_score": 92,
        "social_summary": "Social media sentiment is highly positive, driven by significant search interest...",
        "combined_score": 87.8,
        "combined_sentiment": "Overall sentiment is strongly positive, driven by high social media buzz..."
    }
    ```

---

### 4. Get Synthetic Sentiment Analysis (for Development)

-   **URL:** `/sentiment/synthetic/{ticker}`
-   **Method:** `GET`
-   **Purpose:** Returns a hardcoded, synthetic (mock) sentiment analysis response. Use this for frontend development to avoid using your API quotas for external services like Gemini.
-   **URL Parameters:**
    -   `ticker` (string, **required**): The stock symbol. The data returned is always the same, but the ticker is required in the path.
-   **Success Response:**
    -   The response has the **exact same structure** as the real `/sentiment/{ticker}` endpoint, but the values are synthetic.
        ```json
        {
            "analyst_score": 83,
            "analyst_summary": "[SYNTHETIC] Analysts are cautiously optimistic...",
            "social_score": 75,
            "social_summary": "[SYNTHETIC] Social media buzz is moderate...",
            "combined_score": 79.0,
            "combined_sentiment": "[SYNTHETIC] Overall sentiment is positive but measured..."
        }
        ```