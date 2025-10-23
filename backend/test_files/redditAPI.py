import praw
import os
import dotenv
import time

class RedditPost:
    def __init__(self,post,sub) -> None:
        self.post = post
        self.sub = sub
        self.title = None
        self.upvotes = None
        self.comments = []

        self.readValues()

    def readValues(self):
        print('reading post data')
        self.title = self.post.title
        self.upvotes = self.post.score
        self.post.comments.replace_more(limit=0)
        for comment in self.post.comments[:5]:
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

posts = []

# 3. Fetch the top 5 'hot' posts
for post in subreddit.hot(limit=5):
    posts.append(RedditPost(post,'wallstreetbets'))

for post in posts:
    post.displayPost()

print(f'Took {round(time.time()-start_time)}s to run')