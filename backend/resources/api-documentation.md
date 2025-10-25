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

Fetches a comprehensive sentiment analysis for a given stock. This combines three distinct analyses:
1.  **Analyst Sentiment:** Based on professional analyst ratings.
2.  **Social Sentiment:** Based on Reddit discussions and Google Trends data.
3.  **Combined Sentiment:** A final, confidence-weighted score that blends the analyst and social signals.

-   **URL:** `/stock/{ticker}`
-   **Method:** `GET`
-   **URL Parameters:**
    -   `ticker` (string, **required**): The stock symbol to look up (e.g., `AAPL`, `TSLA`).

-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:** A JSON object containing the scores and summaries for all three analysis types.
        ```json
        {
            "analyst_score": 83,
            "analyst_summary": "Analysts are currently bullish on Tesla, citing strong EV delivery growth and market leadership. The average price target suggests a potential upside of 15.20% from the current price.",
            "social_score": 92,
            "social_summary": "Social media sentiment is highly positive, driven by significant search interest on Google Trends and a large volume of positive discussion on Reddit regarding upcoming product announcements.",
            "combined_score": 87.8,
            "combined_sentiment": "Overall sentiment is strongly positive. This is primarily driven by high social media buzz and positive Reddit conversations, further supported by a solid 'Buy' consensus from market analysts, whose opinions are given moderate weight due to a significant number of reviews."
        }
        ```

-   **Error Response:**
    -   If part of the analysis fails (e.g., for a ticker with no analyst ratings), the `summary` for that section will contain an error message and the `score` may default to a neutral value.

**Example using JavaScript `fetch`:**
```javascript
const ticker = 'TSLA';

fetch(`http://127.0.0.1:8000/stock/${ticker}`)
  .then(response => response.json())
  .then(data => {
    console.log('Full Analysis:', data);
    console.log('--- Combined Analysis ---');
    console.log('Score:', data.combined_score);
    console.log('Summary:', data.combined_sentiment);
  })
  .catch(error => console.error('Fetch Error:', error));
```
