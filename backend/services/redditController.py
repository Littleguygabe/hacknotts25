import os
import dotenv
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load environment variables from .env file
dotenv.load_dotenv()

class RedditController:
    def __init__(self):
        try:
            self.reddit = praw.Reddit(
                client_id=os.environ.get("REDDIT_CLIENT_ID"),
                client_secret=os.environ.get("REDDIT_SECRET"),
                user_agent=os.environ.get("REDDIT_USER_AGENT", "SocialSentimentAnalysis v1.0 by FinScythe")
            )
            self.analyzer = SentimentIntensityAnalyzer()
        except Exception as e:
            print(f"Error initializing RedditController: {e}")
            self.reddit = None
            self.analyzer = None

    def get_reddit_sentiment(self, search_terms):
        if not self.reddit or not self.analyzer:
            print("RedditController not initialized. Returning neutral sentiment.")
            return [], 0, 50.0
        subreddits = "stocks+investing+wallstreetbets"
        query = ' OR '.join(search_terms)
        headlines = []
        compound_scores = []

        try:
            # Search the multi-reddit for hot posts in the last week
            posts = self.reddit.subreddit(subreddits).search(query, sort='hot', time_filter='week', limit=50)
            for post in posts:
                headlines.append(post.title)
                compound_scores.append(self.analyzer.polarity_scores(post.title)['compound'])

            # Handle case where no posts are found
            if not compound_scores:
                print(f"No Reddit posts found for the given terms.")
                return [], 0, 50.0

            # Average the compound scores and scale to 0-100
            average_compound = sum(compound_scores) / len(compound_scores)
            reddit_score = (average_compound + 1) * 50
            return headlines, len(headlines), reddit_score

        except Exception as e:
            print(f"An error occurred while fetching Reddit data: {e}")
            return [], 0, 50.0
