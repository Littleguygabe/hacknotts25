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

This endpoint is for checking if the backend server is running correctly.

-   **URL:** `/`
-   **Method:** `GET`
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:** 
        ```json
        {
            "message": "Hello! Your fast api backend is running"
        }
        ```

---

### 2. Get Full Sentiment Analysis

Fetches a comprehensive sentiment analysis for a given stock, combining analyst ratings and social media sentiment.

-   **URL:** `/stock/{ticker}`
-   **Method:** `GET`
-   **URL Parameters:**
    -   `ticker` (string, **required**): The stock symbol to look up (e.g., `AAPL`, `TSLA`).

-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:** A JSON object containing the separate analyses for analyst and social sentiment, along with a blended overall score.
        ```json
        {
            "ticker": "TSLA",
            "analystSentiment": {
                "summary": "Analysts are currently bullish on Tesla, citing strong EV delivery growth and market leadership. The average price target suggests a potential upside of 15.20% from the current price.",
                "score": 82.5
            },
            "socialSentiment": {
                "summary": "Social media sentiment is highly positive, driven by significant search interest on Google Trends and a large volume of positive discussion on Reddit regarding upcoming product announcements.",
                "score": 91.7
            },
            "overallScore": 87.1
        }
        ```

-   **Error Response:**
    -   If part of the analysis fails (e.g., for a ticker with no analyst ratings), the `summary` for that section will contain an error message and the `score` may default to a neutral value.
        ```json
        {
            "ticker": "SOMETICKER",
            "analystSentiment": {
                "summary": {
                    "err_msg": "Insufficient Data for Analyst Analysis"
                 },
                "score": 0
            },
            "socialSentiment": { ... },
            "overallScore": ...
        }
        ```

**Example using JavaScript `fetch`:**
```javascript
const ticker = 'TSLA';

fetch(`http://127.0.0.1:8000/stock/${ticker}`)
  .then(response => response.json())
  .then(data => {
    console.log('Full Analysis:', data);
    console.log('Overall Score:', data.overallScore);
  })
  .catch(error => console.error('Fetch Error:', error));
```