from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Correctly import the function from the services package
from services.handleTickerData import getTickerAttributes
from services.sentimentAnalysis import getSentimentAnalysis

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

    #take a time period as a number of days of previous data wanted

    ticker_data = getTickerAttributes(ticker.upper(),time_period)
    sentiment_analysis = getSentimentAnalysis(ticker,time_period)

    #get the sentiment


    return ticker_data


if __name__ == '__main__':
    # To make the imports work correctly, you should now run uvicorn
    # from the parent 'backend' directory like this:
    # uvicorn core.apiController:app --reload
    uvicorn.run(app,host="127.0.0.1",port=8000)


