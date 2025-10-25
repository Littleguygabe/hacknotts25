import yfinance as yf
import services.finnHubController as finnHubController
from models.geminiController import getGeminiNL
import dotenv
from pytrends.request import TrendReq
import pandas as pd
from services.redditController import RedditController
import warnings

#imports for caching
import redis
import json
try:
    redis_client = redis.Redis(host='127.0.0.1',port=6379,db=0,decode_responses=True)
    redis_client.ping()
    print('Connected to Redis')
except Exception as e:
    print(f'ERROR > {e}')
    print('Caching will be disabled')
    redis_client = None


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
        self.analysis_for_gemini = {
            "analysis_type": "Analyst Sentiment",
            "ticker": self.raw_data['ticker'],
            "sentimentScore": self.sentiment_score,
            "sentimentText": sentiment_text,
            "analystCount": self.raw_data['numberOfAnalystOpinions'],
            "potentialUpside": f"{potential_upside_pct:.2f}%",
            "news_summary": self.raw_data.get('news_summary')
        }
        self.analysis_summary = getGeminiNL(self.analysis_for_gemini)

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
        reddit_headlines, self.post_count, self.reddit_score = self._fetch_reddit_data()
        self.gtrends_score, gtrends_avg, gtrends_last = self._fetch_gtrends_data()

        self.sentiment_score = (self.reddit_score * 0.6) + (self.gtrends_score * 0.4)

        self.analysis_for_gemini = {
            "analysis_type": "Social Media Sentiment",
            "ticker": self.ticker,
            "blendedScore": self.sentiment_score,
            "qualitativeSignal (Reddit)": f"{self.reddit_score:.2f}/100 based on {self.post_count} posts.",
            "quantitativeSignal (Google Trends)": f"{self.gtrends_score:.2f}/100 buzz score.",
            "gtrends_average_interest": f"{gtrends_avg:.2f}",
            "gtrends_latest_interest": f"{gtrends_last:.2f}",
            "top_5_headlines": reddit_headlines[:5]
        }

        self.analysis_summary = getGeminiNL(self.analysis_for_gemini)

    def getFullAnalysis(self):
        self._perform_analysis()
        return self.analysis_summary, round(self.sentiment_score)


class CustomSentiment:
    def __init__(self,analyst_sentiment,social_sentiment,ticker) -> None:
        self.analyst_sentiment = analyst_sentiment
        self.social_sentiment = social_sentiment
        self.sentiment_score = 50
    

    def _calculateSentimentScore(self):
        #get the analyst and social score
        analyst_sentiment_score = self.analyst_sentiment.sentiment_score
        social_sentiment_score = self.social_sentiment.reddit_score

        #get the per analyst confidence score and the social buzz value

        analyst_count = self.analyst_sentiment.raw_data['numberOfAnalystOpinions']
        analyst_conf = min((analyst_count/40.0),1.0) #caps the number of analyst opinions at 40

        post_count = self.social_sentiment.post_count
        gtrends_score = self.social_sentiment.gtrends_score

        reddit_conf = min((post_count/50.0),1.0)
        gtrends_conf = gtrends_score/100
        social_conf_norm = (gtrends_conf*0.6)+(reddit_conf*0.4)

        #convert the acs and sbv into probs
        total_conf = analyst_conf+social_conf_norm

        if total_conf == 0:
            analyst_weight = 0.5
            social_weight = 0.5
        else:
            analyst_weight = analyst_conf / total_conf
            social_weight = social_conf_norm / total_conf
        
        # Store them so getFullAnalysis can use them for the Gemini prompt
        self.analyst_weight = analyst_weight
        self.social_weight = social_weight


        # --- 4. Calculate the Final "Expected Value" Score ---
        self.sentiment_score = (analyst_sentiment_score * self.analyst_weight) + \
                               (social_sentiment_score * self.social_weight)

        #calculate the weighted average of the sentiment score
        

    def getSummary(self):
        #combine the analyst and social gemini inputs
        # give it our sentiment score and calculate a summary
        analyst_data = self.analyst_sentiment.analysis_for_gemini
        social_data = self.social_sentiment.analysis_for_gemini

        combined_sentiment_score = self.sentiment_score

        final_context_for_gemini = {
            "analysis_type": "Final Unifying Prediction",
            "final_blended_score_0_100": combined_sentiment_score,
            
            # Nest the original dictionaries to provide clear context for the LLM
            "analyst_module_data": analyst_data,
            "social_module_data": social_data,
            
            # Also pass the weights you calculated
            "analyst_weight": self.analyst_weight, 
            "social_weight": self.social_weight
        }

        self.summary = getGeminiNL(final_context_for_gemini)

    def getFullAnalysis(self):
        #first get the weighted sentiment score
        self._calculateSentimentScore()        
        self.getSummary()

        return self.summary,self.sentiment_score

def getSentimentAnalysis(ticker):
    #check if the data is already cached as no point re-calculating
    if redis_client:
        try:
            cached_result = redis_client.get(f'sentiment_cache:{ticker}')
            if cached_result:
                print(f'Found cached data for {ticker}')
                return json.loads(cached_result)

        except Exception as e:
            print(f'Error Reading data from cache > {e}')

    print(f'Cache MISS for > {ticker}')

    analyst_analyser = AnalystSentiment(ticker)
    analyst_summary, analyst_score = analyst_analyser.getFullAnalysis()

    social_analyser = SocialSentiment(ticker)
    social_summary, social_score = social_analyser.getFullAnalysis()

    combined_analyser = CustomSentiment(analyst_analyser,social_analyser,ticker)
    combined_summary,combined_score = combined_analyser.getFullAnalysis()

    output_dict = {
        'analyst_score':analyst_score,
        'analyst_summary':analyst_summary,
        'social_score':social_score,
        'social_summary':social_summary,
        'combined_score':combined_score,
        'combined_sentiment':combined_summary,
        'current_price':analyst_analyser.raw_data.get('currentPrice'),
        'analyst_targetMeanPrice': analyst_analyser.raw_data.get('targetMeanPrice')
    }

    if redis_client:
        try:
            cache_key = f'sentiment_cache:{ticker}'
            json_out = json.dumps(output_dict)
            redis_client.set(cache_key,json_out,ex=1800) #gives ttl 30 minutes
            print(f'Sentiment for {ticker} cached')

        except Exception as e:
            print(f'ERROR > Could not Cache Data > {e}')

    return output_dict
