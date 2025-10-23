import time
import praw
import os
import dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

class RedditPost:
    def __init__(self,post,sub) -> None:
        self.post = post
        self.sub = sub
        self.title = None
        self.upvotes = None
        self.comments = []

    def readValues(self):
        print('reading post data')
        self.title = self.post.title
        self.upvotes = self.post.score
        self.post.comments.replace_more(limit=0)
        for comment in self.post.comments[1:6]:
            if hasattr(comment,'body'):
                self.comments.append(comment.body)


    def displayPost(self):
        print("-" * 30)
        print(f"Title: {self.title}")
        print(f"Upvotes: {self.upvotes}")
        print("Comments:")
        if self.comments:
            for comment in self.comments:
                print(f"  - {comment}")
        else:
            print("  No comments available.")
        print("-" * 30)

start_time = time.time()

dotenv.load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get('REDDIT_CLIENT_ID'),
    client_secret = os.environ.get('REDDIT_SECRET'),
    user_agent = 'hacknotts proto v1.0'
)

subreddit = reddit.subreddit("wallstreetbets")

print(f"--- Top 5 Posts in r/{subreddit.display_name} ---")

def fetch_and_process_post(raw_post, subreddit_name):
    reddit_post = RedditPost(raw_post, subreddit_name)
    reddit_post.readValues()
    return reddit_post

posts = []
raw_posts_iterator = subreddit.hot(limit=5)

with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_post = {executor.submit(fetch_and_process_post, raw_post, subreddit.display_name): raw_post for raw_post in raw_posts_iterator}

    for future in as_completed(future_to_post):
        try:
            reddit_post_obj = future.result()
            posts.append(reddit_post_obj)
        except Exception as exc:
            print(f'A post generated an exception: {exc}')

for post in posts:
    post.displayPost()

print(f'Took {round(time.time()-start_time)}s to run')