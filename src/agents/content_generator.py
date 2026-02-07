from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class ContentGenerator:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=api_key)
    
    def generate_post(self, topic: str, platform: str = "twitter") -> str:
        """Generate a social media post based on topic"""
        
        prompt = f"""Create a {platform} post about: {topic}

Requirements:
- Engaging and authentic
- Include relevant hashtags
- Keep it concise (280 chars for Twitter)
- Professional yet friendly tone

Return ONLY the post text, nothing else."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            print(f"Error generating content: {e}")
            raise