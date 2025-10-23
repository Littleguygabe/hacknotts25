import os
from dotenv import load_dotenv

load_dotenv()
reddit_key = os.environ.get('REDDIT_API_KEY')
if reddit_key:
    print(reddit_key)



