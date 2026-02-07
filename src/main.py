from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.workflows.approval_workflow import SocialMediaWorkflow
import uuid

app = FastAPI()
workflow = SocialMediaWorkflow()

# Store active workflows
active_workflows = {}

class PostRequest(BaseModel):
    topic: str

class ApprovalRequest(BaseModel):
    workflow_id: str
    approved: bool

@app.post("/generate")
async def generate_post(request: PostRequest):
    """Generate a new post"""
    workflow_id = str(uuid.uuid4())
    
    # Run workflow until approval needed
    result = workflow.run(request.topic, workflow_id)
    
    active_workflows[workflow_id] = {
        "state": result,
        "status": "pending_approval"
    }
    
    return {
        "workflow_id": workflow_id,
        "generated_content": result["generated_content"],
        "status": "pending_approval"
    }

@app.post("/approve")
async def approve_post(request: ApprovalRequest):
    """Approve or reject a post"""
    if request.workflow_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow_state = active_workflows[request.workflow_id]
    workflow_state["state"]["approval_status"] = "approved" if request.approved else "rejected"
    
    if request.approved:
        # Continue workflow to publish
        result = workflow.run(
            workflow_state["state"]["topic"],
            request.workflow_id
        )
        return {
            "status": "published",
            "result": result["publish_result"]
        }
    else:
        return {
            "status": "rejected",
            "message": "Post rejected by user"
        }

@app.get("/status/{workflow_id}")
async def get_status(workflow_id: str):
    """Get workflow status"""
    if workflow_id not in active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return active_workflows[workflow_id]

@app.get("/")
async def root():
    return {"message": "Social Media AI Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
