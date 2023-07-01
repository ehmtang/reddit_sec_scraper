import praw
from datetime import datetime

class WallStreetBetsPraw:
    
    # Initialize a praw.Reddit instance with the provided credentials and user agent
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id = client_id,
            client_secret = client_secret,
            user_agent = user_agent
            )
    
    # Scrape top 100 daily posts from wallstreetbets subreddit forum
    def scrape_top_dailies_posts(self, subreddit='wallstreetbets', limit=100, time_filter='day'):
        headlines = [
            {
                "title": str(post.title).encode('ascii', 'ignore').decode(),
                "flair_text": str(post.link_flair_text),
                "id": str(post.id),
                "author": str(post.author),
                "created_utc": str(datetime.utcfromtimestamp(post.created_utc)),
                "score": str(post.score),
                "upvote_ratio": str(post.upvote_ratio),
                "url": str(post.url)
            }
            for post in self.reddit.subreddit(subreddit).top(limit=limit, time_filter=time_filter)
        ]
        return headlines