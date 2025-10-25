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
-   **Query Parameters:** None
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:** 
        ```json
        {
            "message": "Hello! Your fast api backend is running"
        }
        ```

**Example using JavaScript `fetch`:**
```javascript
fetch('http://127.0.0.1:8000/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

---

### 2. Test API Call

A simple endpoint to test sending a string to the backend and getting a response.

-   **URL:** `/test`
-   **Method:** `GET`
-   **Query Parameters:**
    -   `message` (string, **required**): The message you want to send to the backend.
-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:** 
        ```json
        {
            "message": "Call Received with message > your_message_here"
        }
        ```

**Example using JavaScript `fetch`:**
```javascript
const message = "Hello from the frontend!";
const encodedMessage = encodeURIComponent(message);

fetch(`http://127.0.0.1:8000/test?message=${encodedMessage}`)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

---

### 3. Get Stock Data by Ticker

Fetches recent historical price data for a given stock ticker.

-   **URL:** `/stock/{ticker}`
-   **Method:** `GET`
-   **URL Parameters:**
    -   `ticker` (string, **required**): The stock symbol to look up (e.g., `AAPL`, `TSLA`).
-   **Query Parameters:**
    -   `time_period` (integer, **required**): The number of days to look back. This affects the *granularity* (interval) of the data points returned within a 7-day period.
        -   `time_period <= 7`: returns `1m` intervals.
        -   `time_period <= 60`: returns `15m` intervals.
        -   `time_period > 60`: returns `1d` intervals.

-   **Success Response:**
    -   **Code:** `200 OK`
    -   **Content:** A JSON object containing the ticker and an array of its recent closing prices.
        ```json
        {
            "ticker": "AAPL",
            "ticker_history": [
                {
                    "Datetime": "2025-10-24 09:30:00",
                    "Close": 150.12
                },
                {
                    "Datetime": "2025-10-24 09:31:00",
                    "Close": 150.15
                }
            ]
        }
        ```

-   **Error Response:**
    -   **Code:** `200 OK` (Note: The API currently returns a 200 status even for invalid tickers. The frontend should check the response body for an `err_msg` key to handle errors.)
    -   **Content:**
        ```json
        {
            "err_msg": "'INVALIDTICKER' ticker Does not exist OR has no retrievable data"
        }
        ```

**Example using JavaScript `fetch`:**
```javascript
const ticker = 'AAPL';
const timePeriod = 7; // Number of days

fetch(`http://127.0.0.1:8000/stock/${ticker}?time_period=${timePeriod}`)
  .then(response => response.json())
  .then(data => {
    if (data.err_msg) {
      console.error('API Error:', data.err_msg);
    } else {
      console.log('Stock Data:', data);
    }
  })
  .catch(error => console.error('Fetch Error:', error));
```
