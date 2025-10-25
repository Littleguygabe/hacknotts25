from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time

# Correctly import the function from the services package
from services.handleTickerData import getTickerAttributes
from services.sentimentAnalysis import getSentimentAnalysis
from services.priceForecast import forecastPrices

app = FastAPI()


origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods = ['*'],    
    allow_headers = ['*']
)

@app.get('/')
def read_root():
    return {"message":"Hello! Your fast api backend is running"}

@app.get("/test")
def test_api_call(message: str):
    print(f'received api request with message > {message}')

    ### fastAPI auto converts python dictionaries into json data
    return {'message':f'Call Received with message > {message}'}

@app.get("/stock/{ticker}")
def get_stock_data(ticker: str,time_period: int):
    ticker_data = getTickerAttributes(ticker.strip('$').upper(),time_period)
    return ticker_data

@app.get("/sentiment/{ticker}")
def get_sentiment(ticker:str):
    # start = time.time()
    sentiment = getSentimentAnalysis(ticker)
    # print(f'Runtime: {time.time()-start}s')
    
    return sentiment

@app.get("/stock/{ticker}")
def getPriceActionPredictions(ticker: str,forecast_horizon: str):
    forecasts = forecastPrices(ticker,forecast_horizon)



@app.get("/sentiment/synthetic/{ticker}")
def get_synthetic_sentiment(ticker: str):
    """
    Returns a synthetic (mock) data response for frontend development.
    This avoids calling the Gemini API and other external services.
    The data structure is identical to the real /stock/{ticker} endpoint.
    """
    print(f"--- Serving synthetic data for ticker: {ticker} ---")
    
    synthetic_data = {
        'analyst_score': 83,
        'analyst_summary': "[SYNTHETIC] Analysts are cautiously optimistic, citing strong market position but noting concerns about upcoming regulatory changes.",
        'social_score': 75,
        'social_summary': "[SYNTHETIC] Social media buzz is moderate. While there is positive discussion on Reddit, Google search trends have been flat recently.",
        'combined_score': 79.0,
        'combined_sentiment': "[SYNTHETIC] Overall sentiment is positive but measured. The solid analyst ratings are balanced by a more neutral social media landscape, indicating a 'wait-and-see' approach from the public.",
    }
    
    return synthetic_data


if __name__ == '__main__':
    # To make the imports work correctly, you should now run uvicorn
    # from the parent 'backend' directory like this:
    # uvicorn core.apiController:app --reload
    uvicorn.run(app,host="127.0.0.1",port=8000)


