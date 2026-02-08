from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents.content_generator import ContentGenerator
from tools.social_publisher import SocialPublisher
import uuid
import os
from typing import Dict

app = FastAPI(title="Social Media AI Agent")

generator = ContentGenerator()
publisher = SocialPublisher()
pending_posts: Dict[str, dict] = {}

class PostRequest(BaseModel):
    topic: str

class ApprovalRequest(BaseModel):
    workflow_id: str
    approved: bool

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the UI"""
    try:
        with open("index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback to API info if index.html not found
        return {
            "message": "Social Media AI Agent - Running!",
            "status": "healthy",
            "endpoints": {
                "ui": "GET / (this page)",
                "health": "GET /health",
                "api_docs": "GET /docs",
                "generate": "POST /generate",
                "approve": "POST /approve",
                "status": "GET /status/{id}",
                "pending": "GET /pending"
            }
        }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/generate")
async def generate_post(request: PostRequest):
    """Generate a new post"""
    workflow_id = str(uuid.uuid4())
    content = generator.generate_post(request.topic)
    
    pending_posts[workflow_id] = {
        "topic": request.topic,
        "content": content,
        "status": "pending_approval"
    }
    
    return {
        "workflow_id": workflow_id,
        "content": content,
        "chars": len(content),
        "status": "pending_approval"
    }

@app.post("/approve")
async def approve_post(request: ApprovalRequest):
    """Approve or reject"""
    if request.workflow_id not in pending_posts:
        raise HTTPException(404, "Not found")
    
    post = pending_posts[request.workflow_id]
    
    if request.approved:
        result = publisher.publish_to_twitter(post["content"])
        post["status"] = "published"
        post["result"] = result
        return {"status": "published", "result": result}
    else:
        post["status"] = "rejected"
        return {"status": "rejected"}

@app.get("/status/{workflow_id}")
async def get_status(workflow_id: str):
    """Get status"""
    if workflow_id not in pending_posts:
        raise HTTPException(404, "Not found")
    return pending_posts[workflow_id]

@app.get("/pending")
async def list_pending():
    """List pending"""
    pending = {k: v for k, v in pending_posts.items() 
               if v["status"] == "pending_approval"}
    return {"count": len(pending), "posts": pending}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)