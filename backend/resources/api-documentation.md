# FinScythe Backend API Documentation

A guide for the frontend team on how to interact with the backend API.

## Running the Backend

First, ensure you have the necessary dependencies installed by running this command in the `backend` directory:
```bash
pip install -r requirements.txt
```
Then, from the `backend/core` directory, run the backend server:
```bash
uvicorn apiController:app --reload
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
            "message": "thank you for your api call"
        }
        ```

**Example using JavaScript `fetch`:**
```javascript
const message = "Hello from the frontend!";
// It's important to encode the message to make sure it's a valid URL component
const encodedMessage = encodeURIComponent(message);

fetch(`http://127.0.0.1:8000/test?message=${encodedMessage}`)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```
