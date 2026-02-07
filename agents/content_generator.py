import random

class ContentGenerator:
    def __init__(self):
        """Mock content generator - no API needed"""
        pass
    
    def generate_post(self, topic: str, platform: str = "twitter") -> str:
        """Generate a mock post for testing"""
        templates = [
            f"🚀 Excited about {topic}! This is transforming how we work. #AI #Tech #Innovation",
            f"💡 Hot take: {topic} is the future. Here's why it matters... #Technology",
            f"📊 Just discovered {topic}. The implications are huge! #TechNews #AI",
            f"🔥 {topic} is going to change everything. Thread 🧵 #Innovation",
            f"⚡ Breaking down {topic} in simple terms. #TechTrends"
        ]
        
        post = random.choice(templates)
        
        # Keep under 280 chars
        if len(post) > 280:
            post = post[:277] + "..."
        
        return post