import yfinance as yf
import services.finnHubController as finnHubController
from models.geminiController import getGeminiNL
import os
import dotenv
from pytrends.request import TrendReq
import pandas as pd
from services.redditController import RedditController
import warnings


dotenv.load_dotenv()

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    module="pytrends.request"
)

class AnalystSentiment:
    """
    A class to fetch, analyze, and summarize analyst sentiment for a given stock ticker.
    """
    def __init__(self, ticker_sym):
        self.ticker = ticker_sym
        self.raw_data = None
        self.analysis_summary = None
        self.sentiment_score = None

    def _fetch_raw_data(self):
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
                self.raw_data['currentPrice'] = self.raw_data.get('targetMeanPrice', 0)
        except Exception as e:
            print(f"Error fetching raw analyst data for {self.ticker}: {e}")
            self.raw_data = None

    def _perform_analysis(self):
        if not self.raw_data or self.raw_data.get('recommendationMean') is None:
            self.analysis_summary = {'err_msg': 'Insufficient Data for Analyst Analysis'}
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
            "analysis_type": "Analyst Sentiment",
            "ticker": self.raw_data['ticker'],
            "sentimentScore": self.sentiment_score,
            "sentimentText": sentiment_text,
            "analystCount": self.raw_data['numberOfAnalystOpinions'],
            "potentialUpside": f"{potential_upside_pct:.2f}%",
            "news_summary": self.raw_data.get('news_summary')
        }
        self.analysis_summary = getGeminiNL(analysis_for_gemini)

    def getFullAnalysis(self):
        self._fetch_raw_data()
        self._perform_analysis()
        return self.analysis_summary, round(self.sentiment_score)

class SocialSentiment:
    """
    Analyzes public sentiment for a stock using Reddit and Google Trends.
    """
    def __init__(self, ticker):
        self.ticker = ticker
        ticker_obj = yf.Ticker(ticker)
        l_name = ticker_obj.info.get('longName', ticker)
        self.search_terms = [f'${ticker}', ticker, l_name.split()[0]]
        self.sentiment_score = 50.0
        self.analysis_summary = None
        try:
            self.reddit_controller = RedditController()
            self.pytrends = TrendReq(hl='en-US', tz=360)
        except Exception as e:
            print(f"Error initializing clients in SocialSentiment: {e}")

    def _fetch_reddit_data(self):
        return self.reddit_controller.get_reddit_sentiment(self.search_terms)

    def _fetch_gtrends_data(self):
        try:
            self.pytrends.build_payload(self.search_terms, cat=0, timeframe='today 1-m', geo='', gprop='')
            df = self.pytrends.interest_over_time()
            if df.empty:
                print(f"No Google Trends data found for {self.ticker}.")
                return 50.0, 50.0, 50.0
            
            df['average'] = df[self.search_terms].mean(axis=1)
            gtrends_avg = df['average'].mean()
            gtrends_last = df['average'].iloc[-1]
            gtrends_score = (gtrends_avg + gtrends_last) / 2
            return gtrends_score, gtrends_avg, gtrends_last
        except Exception as e:
            print(f"Error fetching Google Trends data: {e}")
            return 50.0, 50.0, 50.0

    def _perform_analysis(self):
        reddit_headlines, post_count, reddit_score = self._fetch_reddit_data()
        gtrends_score, gtrends_avg, gtrends_last = self._fetch_gtrends_data()

        self.sentiment_score = (reddit_score * 0.6) + (gtrends_score * 0.4)

        analysis_for_gemini = {
            "analysis_type": "Social Media Sentiment",
            "ticker": self.ticker,
            "blendedScore": self.sentiment_score,
            "qualitativeSignal (Reddit)": f"{reddit_score:.2f}/100 based on {post_count} posts.",
            "quantitativeSignal (Google Trends)": f"{gtrends_score:.2f}/100 buzz score.",
            "gtrends_average_interest": f"{gtrends_avg:.2f}",
            "gtrends_latest_interest": f"{gtrends_last:.2f}",
            "top_5_headlines": reddit_headlines[:5]
        }

        self.analysis_summary = getGeminiNL(analysis_for_gemini)

    def getFullAnalysis(self):
        self._perform_analysis()
        return self.analysis_summary, round(self.sentiment_score)

def getSentimentAnalysis(ticker):
    analyst_analyser = AnalystSentiment(ticker)
    analyst_summary, analyst_score = analyst_analyser.getFullAnalysis()

    social_analyser = SocialSentiment(ticker)
    social_summary, social_score = social_analyser.getFullAnalysis()

    output_dict = {
        'analyst_score':analyst_score,
        'analyst_summary':analyst_summary,
        'social_score':social_score,
        'social_summary':social_summary
    }

    return output_dict
