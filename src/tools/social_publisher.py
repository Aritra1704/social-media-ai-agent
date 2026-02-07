import tweepy
import os
from typing import Dict

class SocialPublisher:
    def __init__(self, dry_run=True):
        """
        Initialize social media publisher
        
        Args:
            dry_run: If True, simulate posting without actually publishing
        """
        self.dry_run = dry_run
        
        if not dry_run:
            # Only initialize Twitter client if not in dry run mode
            try:
                auth = tweepy.OAuthHandler(
                    os.getenv("TWITTER_API_KEY"),
                    os.getenv("TWITTER_API_SECRET")
                )
                auth.set_access_token(
                    os.getenv("TWITTER_ACCESS_TOKEN"),
                    os.getenv("TWITTER_ACCESS_SECRET")
                )
                self.twitter_client = tweepy.API(auth)
            except Exception as e:
                print(f"Warning: Twitter client initialization failed: {e}")
                self.dry_run = True  # Fall back to dry run
    
    def publish_to_twitter(self, content: str) -> Dict:
        """Publish content to Twitter"""
        if self.dry_run:
            print(f"[DRY RUN] Would publish to Twitter: {content[:50]}...")
            return {
                "success": True,
                "platform": "twitter",
                "post_id": "dry_run_12345",
                "url": "https://twitter.com/user/status/dry_run_12345",
                "dry_run": True
            }
        
        try:
            tweet = self.twitter_client.update_status(content)
            return {
                "success": True,
                "platform": "twitter",
                "post_id": tweet.id_str,
                "url": f"https://twitter.com/user/status/{tweet.id_str}",
                "dry_run": False
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "platform": "twitter"
            }