import yfinance as yf
import services.finnHubController as finnHubController
from models.geminiController import getGeminiNL

class AnalystSentiment:
    """
    A class to fetch, analyze, and summarize analyst sentiment for a given stock ticker.
    """
    def __init__(self, ticker_sym):
        """
        Initializes the AnalystSentiment class for a specific stock ticker.
        Args:
            ticker_sym (str): The stock ticker symbol (e.g., 'AAPL').
        """
        self.ticker = ticker_sym
        self.raw_data = None
        self.analysis_summary = None
        self.sentiment_score = None

    def _fetch_raw_data(self):
        """
        Private method to fetch raw analyst and news data from yfinance and Finnhub.
        """
        print(f"Fetching analyst data for {self.ticker}...")
        try:
            ticker_obj = yf.Ticker(self.ticker)
            info = ticker_obj.info
            news_summary = finnHubController.getNews(self.ticker)

            self.raw_data = {
                "ticker": self.ticker,
                "recommendationMean": info.get('recommendationMean', None),
                "recommendationKey": info.get('recommendationKey', 'n/a'),
                "numberOfAnalystOpinions": info.get('numberOfAnalystOpinions', 0),
                "targetMeanPrice": info.get('targetMeanPrice', 0),
                "currentPrice": info.get('regularMarketPrice', info.get('currentPrice', 0)),
                "corporateActions": info.get('corporateActions'),
                "news_summary": news_summary
            }

            if self.raw_data['currentPrice'] is None or self.raw_data['currentPrice'] == 0:
                print(f"Warning: Could not fetch current price for {self.ticker}. Upside calculation will be skewed.")
                self.raw_data['currentPrice'] = self.raw_data.get('targetMeanPrice', 0)

        except Exception as e:
            print(f"Error fetching raw data for {self.ticker}: {e}")
            self.raw_data = None

    def _perform_analysis(self):
        """
        Private method to analyze fetched data, calculate sentiment, and get a Gemini summary.
        """
        if not self.raw_data or self.raw_data.get('recommendationMean') is None:
            self.analysis_summary = {'err_msg': 'Insufficient Data for Analysis'}
            return

        score = self.raw_data['recommendationMean']
        sentiment_text = 'N/A'

        if score is not None:
            if score < 1.5: sentiment_text = 'Strong Buy'
            elif score < 2.5: sentiment_text = 'Buy'
            elif score < 3.5: sentiment_text = 'Hold'
            elif score < 4.5: sentiment_text = 'Sell'
            else: sentiment_text = 'Strong Sell'

        potential_upside_pct = 0.0
        if self.raw_data.get('currentPrice', 0) > 0 and self.raw_data.get('targetMeanPrice', 0) > 0:
            potential_upside_pct = ((self.raw_data['targetMeanPrice'] / self.raw_data['currentPrice']) - 1) * 100

        self.sentiment_score = (5 - score) * 25 if score is not None else 0

        analysis_for_gemini = {
            "ticker": self.raw_data['ticker'],
            "sentimentScore": self.sentiment_score,
            "sentimentText": sentiment_text,
            "analystCount": self.raw_data['numberOfAnalystOpinions'],
            "currentPrice": f"${self.raw_data.get('currentPrice', 0):.2f}",
            "targetMeanPrice": f"${self.raw_data.get('targetMeanPrice', 0):.2f}",
            "potentialUpside": f"{potential_upside_pct:.2f}%",
            "corporateActions": [a.get('headline') for a in self.raw_data.get('corporateActions', []) if a],
            "news_summary": self.raw_data.get('news_summary')
        }
        
        self.analysis_summary = getGeminiNL(analysis_for_gemini)

    def getFullAnalysis(self):
        """
        Public method to run the full fetch and analysis pipeline.
        Returns the natural language summary and the calculated sentiment score.
        """
        self._fetch_raw_data()
        self._perform_analysis()
        return self.analysis_summary, self.sentiment_score

def getSentimentAnalysis(ticker):
    analyst_obj = AnalystSentiment(ticker)
    analyst_summary,analyst_sentiment_score = analyst_obj.getFullAnalysis()
    print(analyst_summary,analyst_sentiment_score)