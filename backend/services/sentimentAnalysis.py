import yfinance as yf


def getAnalystSentiment(ticker_sym):
    print('getting analyst sentiment')
    try:
        ticker = yf.Ticker(ticker_sym)
        info = ticker.info
        # recommendationMean: A 1-5 scale (1=Strong Buy, 5=Strong Sell)
        # recommendationKey: The text (e.g., 'buy', 'hold')
        # targetMeanPrice: The average price target from analysts
        # regularMarketPrice: The last traded price
        # numberOfAnalystOpinions: How many analysts contribute to the consensus

        data = {
            "ticker": ticker_sym,
            "recommendationMean": info.get('recommendationMean', None),
            "recommendationKey": info.get('recommendationKey', 'n/a'),
            "numberOfAnalystOpinions": info.get('numberOfAnalystOpinions', 0),
            "targetMeanPrice": info.get('targetMeanPrice', 0),
            "currentPrice": info.get('regularMarketPrice', info.get('currentPrice', 0))
        }

        if data['currentPrice'] is None or data['currentPrice'] == 0:
            print(f"Warning: Could not fetch current price for {ticker_sym}. Upside calculation will be skewed.")
            data['currentPrice'] = data['targetMeanPrice'] # Avoid division by zero, though this makes upside 0

        return data
        
    except Exception as e:
        print(f"Error fetching data for {ticker_sym}: {e}")
        return None


def createSentimentAnalysis(data):
    pass

def getSentimentAnalysis(ticker,time_period):
    analyst_sentiment = getAnalystSentiment(ticker)
    