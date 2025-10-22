import os
import requests

FMP_API_KEY = 'tXbUoWgagYPE4RGbi7hcoYSvIUcbkzX1'

BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_fmp_analyst_sentiment(ticker):
    url = f"{BASE_URL}/analyst-stock-recommendations/{ticker}?apikey={FMP_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if not data:
        return None, "No FMP analyst data available."

    latest_recommendation = data[0]
    
    rating_details = latest_recommendation.get("ratingDetails", {})
    
    buy_count = rating_details.get("ratingBuy", 0) + rating_details.get("ratingStrongBuy", 0)
    hold_count = rating_details.get("ratingHold", 0)
    sell_count = rating_details.get("ratingSell", 0) + rating_details.get("ratingStrongSell", 0)
    
    total_analysts = buy_count + hold_count + sell_count
    
    if total_analysts > 0:
        score = (buy_count * 5 + hold_count * 3 + sell_count * 1) / total_analysts
        return score * 2, "FMP Analyst sentiment calculated." # Scale 1-5 to 1-10

    return None, "Could not calculate FMP analyst sentiment."

if __name__ == "__main__":
    ticker_symbol = "AAPL"

    url = f'https://financialmodelingprep.com/stable/search-symbol?query=AAPL&apikey=tXbUoWgagYPE4RGbi7hcoYSvIUcbkzX1'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(data[0])
   
