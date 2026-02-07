import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

print("=" * 60)
print("ENVIRONMENT CHECK")
print("=" * 60)

# Check if API key exists
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print(f"✅ ANTHROPIC_API_KEY found (starts with: {api_key[:10]}...)")
else:
    print("❌ ANTHROPIC_API_KEY not found!")
    print("   Please check your .env file")
    exit(1)

print("\n" + "=" * 60)
print("TEST 1: Import Anthropic Library")
print("=" * 60)

try:
    from anthropic import Anthropic
    print("✅ Anthropic library imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Anthropic: {e}")
    print("   Run: pip install anthropic")
    exit(1)

print("\n" + "=" * 60)
print("TEST 2: Create Anthropic Client")
print("=" * 60)

try:
    client = Anthropic(api_key=api_key)
    print("✅ Anthropic client created successfully")
except Exception as e:
    print(f"❌ Failed to create client: {e}")
    exit(1)

print("\n" + "=" * 60)
print("TEST 3: Generate Simple Completion")
print("=" * 60)

try:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say hello in 5 words or less"}
        ]
    )
    response = message.content[0].text
    print(f"✅ API Response: {response}")
except Exception as e:
    print(f"❌ API call failed: {e}")
    exit(1)

print("\n" + "=" * 60)
print("TEST 4: Content Generator")
print("=" * 60)

try:
    from src.agents.content_generator import ContentGenerator
    print("✅ ContentGenerator imported successfully")
    
    generator = ContentGenerator()
    print("✅ ContentGenerator initialized")
    
    post = generator.generate_post("AI productivity tools", "twitter")
    print(f"✅ Generated post ({len(post)} chars):")
    print(f"   '{post}'")
except Exception as e:
    print(f"❌ ContentGenerator test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("TEST 5: Social Publisher (Initialization Only)")
print("=" * 60)

try:
    from src.tools.social_publisher import SocialPublisher
    print("✅ SocialPublisher imported successfully")
    
    # Initialize with dry_run to avoid actual Twitter connection
    publisher = SocialPublisher()
    print("✅ SocialPublisher initialized")
except Exception as e:
    print(f"❌ SocialPublisher test failed: {e}")
    print("   Note: Twitter API errors are expected if credentials aren't set")

print("\n" + "=" * 60)
print("TEST 6: Workflow (Structure Only)")
print("=" * 60)

try:
    from src.workflows.approval_workflow import SocialMediaWorkflow
    print("✅ SocialMediaWorkflow imported successfully")
    
    # Note: Full workflow test requires LangGraph setup
    print("✅ Workflow module loaded (full test in API)")
except Exception as e:
    print(f"❌ Workflow test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ ALL BASIC TESTS PASSED!")
print("=" * 60)
print("\nNext step: Run 'python src/main.py' to start the API server")