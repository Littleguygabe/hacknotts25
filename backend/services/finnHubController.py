import finnhub
import json
import os
import dotenv
from datetime import datetime,timedelta
from models.geminiController import getNewsSummary

dotenv.load_dotenv()
api_key = os.environ.get('FINNHUB_KEY')
finnhub_client = finnhub.Client(api_key=api_key)

def getNews(ticker_sym):
    try:

        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        company_news = finnhub_client.company_news(ticker_sym,_from=from_date,to=to_date)
        relevant_news = company_news[:20]
        
        headlines = {}

        for element in relevant_news:
            headline = element['headline']
            summary = element['summary']
            timestamp = element['datetime']

            date_object = datetime.fromtimestamp(timestamp)
            formatted_date = date_object.strftime("%d/%m/%Y")
            
            headlines[headline] = (formatted_date,summary)

        news_summary = getNewsSummary(headlines,ticker_sym) 

        return news_summary

    except Exception as e:
        print(f'ERROR > {e}')
        return []