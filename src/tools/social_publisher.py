import tweepy
import os
from typing import Dict

class SocialPublisher:
    def __init__(self):
        # Twitter/X Setup
        auth = tweepy.OAuthHandler(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET")
        )
        auth.set_access_token(
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        )
        self.twitter_client = tweepy.API(auth)
    
    def publish_to_twitter(self, content: str) -> Dict:
        """Publish content to Twitter"""
        try:
            tweet = self.twitter_client.update_status(content)
            return {
                "success": True,
                "platform": "twitter",
                "post_id": tweet.id_str,
                "url": f"https://twitter.com/user/status/{tweet.id_str}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }