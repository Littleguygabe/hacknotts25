import os
import finnhub
from datetime import datetime, timedelta


finnhub_client = finnhub.Client(api_key='d3s8p61r01qs1aprm46gd3s8p61r01qs1aprm470')

def get_analyst_sentiment(ticker):
    data = finnhub_client.recommendation_trends(ticker)

    if not data:
        return None, "No analyst data available."

    latest_period = data[0]
    
    buy_count = latest_period.get('buy', 0) + latest_period.get('strongBuy', 0)
    hold_count = latest_period.get('hold', 0)
    sell_count = latest_period.get('sell', 0) + latest_period.get('strongSell', 0)
    
    total_analysts_for_period = buy_count + hold_count + sell_count
    if total_analysts_for_period > 0:
        score = (buy_count * 5 + hold_count * 3 + sell_count * 1) / total_analysts_for_period
        return score * 2, "Analyst sentiment calculated." # Scale 1-5 to 1-10

    return None, "Could not calculate analyst sentiment."

def get_retail_sentiment(ticker, days_history=7):
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days_history)
    
    data = finnhub_client.stock_social_sentiment(ticker, _from=from_date.strftime('%Y-%m-%d'), to=to_date.strftime('%Y-%m-%d'))
    
    if not data or not data.get('reddit'):
        return None, "No retail sentiment data available."

    total_reddit_score = 0
    total_mentions = 0
    
    for entry in data['reddit']:
        total_reddit_score += entry.get('score', 0) * entry.get('mention', 0)
        total_mentions += entry.get('mention', 0)
    
    if total_mentions > 0:
        average_sentiment = total_reddit_score / total_mentions
        return average_sentiment * 10, "Retail sentiment calculated."
    
    return None, "Could not calculate retail sentiment."

if __name__ == "__main__":
    ticker_symbol = "TSLA"

    analyst_score, analyst_msg = get_analyst_sentiment(ticker_symbol)
    if analyst_score is not None:
        print(f"Analyst Sentiment for {ticker_symbol}: {analyst_score:.2f} ({analyst_msg})")
    else:
        print(f"Analyst Sentiment for {ticker_symbol}: {analyst_msg}")

    retail_score, retail_msg = get_retail_sentiment(ticker_symbol, days_history=7)
    if retail_score is not None:
        print(f"Retail Sentiment for {ticker_symbol}: {retail_score:.2f} ({retail_msg})")
    else:
        print(f"Retail Sentiment for {ticker_symbol}: {retail_msg}")
