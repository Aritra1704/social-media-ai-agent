from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.agents.content_generator import ContentGenerator
from src.tools.social_publisher import SocialPublisher
import operator

class AgentState(TypedDict):
    topic: str
    generated_content: str
    approval_status: Literal["pending", "approved", "rejected"]
    publish_result: dict
    messages: Annotated[list, operator.add]

class SocialMediaWorkflow:
    def __init__(self):
        self.generator = ContentGenerator()
        self.publisher = SocialPublisher()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("generate", self.generate_content)
        workflow.add_node("wait_approval", self.wait_for_approval)
        workflow.add_node("publish", self.publish_content)
        
        # Add edges
        workflow.set_entry_point("generate")
        workflow.add_edge("generate", "wait_approval")
        workflow.add_conditional_edges(
            "wait_approval",
            self.check_approval,
            {
                "approved": "publish",
                "rejected": END,
                "pending": "wait_approval"
            }
        )
        workflow.add_edge("publish", END)
        
        # Add memory for persistence
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    def generate_content(self, state: AgentState) -> AgentState:
        """Generate social media content"""
        content = self.generator.generate_post(state["topic"])
        state["generated_content"] = content
        state["approval_status"] = "pending"
        state["messages"].append(f"Generated content: {content}")
        return state
    
    def wait_for_approval(self, state: AgentState) -> AgentState:
        """Wait for human approval (handled by API)"""
        state["messages"].append("Waiting for approval...")
        return state
    
    def check_approval(self, state: AgentState) -> str:
        """Check approval status"""
        return state["approval_status"]
    
    def publish_content(self, state: AgentState) -> AgentState:
        """Publish approved content"""
        result = self.publisher.publish_to_twitter(state["generated_content"])
        state["publish_result"] = result
        state["messages"].append(f"Published: {result}")
        return state
    
    def run(self, topic: str, thread_id: str):
        """Run the workflow"""
        initial_state = {
            "topic": topic,
            "generated_content": "",
            "approval_status": "pending",
            "publish_result": {},
            "messages": []
        }
        
        config = {"configurable": {"thread_id": thread_id}}
        return self.workflow.invoke(initial_state, config)