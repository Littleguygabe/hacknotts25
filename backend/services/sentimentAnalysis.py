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


def analyseSentiment(data):
    #take in sentiment in the format of the output from analyst sentiment    

    if not data or data.get('recommendationMean') is None:
        return {
            'ticker': data.get('ticker','N/A'),
            'err_msg':'Insufficient Data for Analysis'
        }
    
    score = data['recommendationMean']
    sentiment_text = 'N/A'

    if score is not None:
        if score<1.5:
            sentiment_text='Strong Buy'
        
        elif score<2.5:
            sentiment_text='Buy'
        
        elif score<3.5:
            sentiment_text='Hold'

        elif score<4.5:
            sentiment_text='Sell'

        else:
            sentiment_text = 'Strong Sell'
        
    
    potential_upside_pct = 0.0
    if data['currentPrice'] and data['currentPrice'] > 0 and data['targetMeanPrice'] and data['targetMeanPrice'] > 0:
        potential_upside_pct = ((data['targetMeanPrice'] / data['currentPrice']) - 1) * 100
    
    adjusted_sentiment_score = (5-score)*25 #scales the sentiment score 0-100 with 100 being strong buy
    
    analysis = {
        "ticker": data['ticker'],
        "sentimentScore": adjusted_sentiment_score,
        "sentimentText": sentiment_text,
        "analystCount": data['numberOfAnalystOpinions'],
        "currentPrice": f"${data['currentPrice']:.2f}",
        "targetMeanPrice": f"${data['targetMeanPrice']:.2f}",
        "potentialUpside": f"{potential_upside_pct:.2f}%"
    }
    
    return analysis

def getSentimentAnalysis(ticker,time_period):
    analyst_info = getAnalystSentiment(ticker)
    analyst_sentiment = analyseSentiment(analyst_info)
    print(analyst_sentiment)



