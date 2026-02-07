from typing import Dict

class SocialPublisher:
    def __init__(self):
        """Mock publisher - simulates posting"""
        pass
    
    def publish_to_twitter(self, content: str) -> Dict:
        """Simulate publishing to Twitter"""
        print(f"[MOCK] Would publish: {content[:50]}...")
        return {
            "success": True,
            "platform": "twitter",
            "post_id": "mock_12345",
            "url": "https://twitter.com/user/status/mock_12345",
            "mock": True
        }