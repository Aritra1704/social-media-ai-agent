from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.content_generator import ContentGenerator
from src.tools.social_publisher import SocialPublisher
import uuid
from typing import Dict

app = FastAPI()

# Initialize components
generator = ContentGenerator(use_mock=True)  # Use mock for testing
publisher = SocialPublisher(dry_run=True)     # Dry run for testing

# In-memory storage for pending posts
pending_posts: Dict[str, dict] = {}

class PostRequest(BaseModel):
    topic: str

class ApprovalRequest(BaseModel):
    workflow_id: str
    approved: bool

@app.get("/")
async def root():
    return {
        "message": "Social Media AI Agent API",
        "status": "running",
        "endpoints": {
            "generate": "POST /generate",
            "approve": "POST /approve",
            "status": "GET /status/{workflow_id}"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/generate")
async def generate_post(request: PostRequest):
    """Generate a new post"""
    try:
        workflow_id = str(uuid.uuid4())
        
        # Generate content
        content = generator.generate_post(request.topic)
        
        # Store in memory
        pending_posts[workflow_id] = {
            "topic": request.topic,
            "content": content,
            "status": "pending_approval",
            "publish_result": None
        }
        
        return {
            "workflow_id": workflow_id,
            "generated_content": content,
            "status": "pending_approval",
            "message": "Post generated. Call /approve to publish."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/approve")
async def approve_post(request: ApprovalRequest):
    """Approve or reject a post"""
    if request.workflow_id not in pending_posts:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    post_data = pending_posts[request.workflow_id]
    
    if request.approved:
        # Publish the post
        result = publisher.publish_to_twitter(post_data["content"])
        post_data["publish_result"] = result
        post_data["status"] = "published" if result["success"] else "failed"
        
        return {
            "status": post_data["status"],
            "result": result,
            "message": "Post published successfully!" if result["success"] else "Publishing failed"
        }
    else:
        post_data["status"] = "rejected"
        return {
            "status": "rejected",
            "message": "Post rejected by user"
        }

@app.get("/status/{workflow_id}")
async def get_status(workflow_id: str):
    """Get workflow status"""
    if workflow_id not in pending_posts:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return pending_posts[workflow_id]

@app.get("/pending")
async def list_pending():
    """List all pending posts"""
    return {
        "count": len(pending_posts),
        "posts": pending_posts
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)




# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from src.workflows.approval_workflow import SocialMediaWorkflow
# import uuid

# app = FastAPI()
# workflow = SocialMediaWorkflow()

# # Store active workflows
# active_workflows = {}

# class PostRequest(BaseModel):
#     topic: str

# class ApprovalRequest(BaseModel):
#     workflow_id: str
#     approved: bool

# @app.post("/generate")
# async def generate_post(request: PostRequest):
#     """Generate a new post"""
#     workflow_id = str(uuid.uuid4())
    
#     # Run workflow until approval needed
#     result = workflow.run(request.topic, workflow_id)
    
#     active_workflows[workflow_id] = {
#         "state": result,
#         "status": "pending_approval"
#     }
    
#     return {
#         "workflow_id": workflow_id,
#         "generated_content": result["generated_content"],
#         "status": "pending_approval"
#     }

# @app.post("/approve")
# async def approve_post(request: ApprovalRequest):
#     """Approve or reject a post"""
#     if request.workflow_id not in active_workflows:
#         raise HTTPException(status_code=404, detail="Workflow not found")
    
#     workflow_state = active_workflows[request.workflow_id]
#     workflow_state["state"]["approval_status"] = "approved" if request.approved else "rejected"
    
#     if request.approved:
#         # Continue workflow to publish
#         result = workflow.run(
#             workflow_state["state"]["topic"],
#             request.workflow_id
#         )
#         return {
#             "status": "published",
#             "result": result["publish_result"]
#         }
#     else:
#         return {
#             "status": "rejected",
#             "message": "Post rejected by user"
#         }

# @app.get("/status/{workflow_id}")
# async def get_status(workflow_id: str):
#     """Get workflow status"""
#     if workflow_id not in active_workflows:
#         raise HTTPException(status_code=404, detail="Workflow not found")
    
#     return active_workflows[workflow_id]

# @app.get("/")
# async def root():
#     return {"message": "Social Media AI Agent API"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
