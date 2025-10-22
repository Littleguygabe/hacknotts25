import pandas as pd
from newsapi import NewsApiClient
import os
import argparse


API_KEY = '26b2a74685ca4920b8b05b47b057e1f1'

def getQuery(searchArgs,constructor):
    sq = f' {constructor.upper()} '.join(searchArgs)
    return sq




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search_query','-sq',nargs='+',required=True,type=str)
    parser.add_argument('--constructor','-c',required=True,type=str)
    args = parser.parse_args()

    print('Running newsAPI testing')

    newsapi = NewsApiClient(api_key=API_KEY)

    search_query = getQuery(args.search_query,args.constructor)    

    try:
        print(f"Fetching news for query: {search_query}...")
        
        # Use get_everything() to search
        all_articles = newsapi.get_everything(
            q=search_query,
            language='en',
            sort_by='publishedAt',  # Get the newest articles first
            page_size=100             # Max 100 on free plan
        )
        
        # --- 4. Process into a DataFrame ---
        articles_list = []
        for article in all_articles['articles']:
            articles_list.append({
                'timestamp': article['publishedAt'],
                'headline': article['title'],
                'source': article['source']['name']
            })

        # Create the DataFrame
        df = pd.DataFrame(articles_list)
        
        # Convert timestamp column to datetime objects (for resampling later)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # --- 5. Save the Data ---
        # This is the file your Streamlit app will read
        df.to_csv('news_headlines.csv', index=False)

        print(f"Success! Fetched {len(df)} articles.")
        print(df.head(35))

    except Exception as e:
        print(f"An error occurred: {e}")
        print("\n--- ERROR DETAILS ---")
        print(e)
        print("\nCheck if your API key is correct or if you've hit your rate limit.")
