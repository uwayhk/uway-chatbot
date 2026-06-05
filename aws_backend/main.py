"""
UWAY Chatbot Backend - FastAPI Service
Handles LLM routing, session management, and compliance logic
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import redis
from contextlib import asynccontextmanager
from pathlib import Path

from provider_manager import ProviderRouter

# Knowledge Base Loader
def load_knowledge_base():
    """Load all markdown files from knowledge base directory"""
    knowledge = {}
    kb_path = Path("/app/knowledge_base")
    if not kb_path.exists():
        kb_path = Path(os.path.join(os.path.dirname(__file__), "..", "knowledge_base"))
    
    if kb_path.exists():
        for md_file in kb_path.rglob("*.md"):
            if "node_modules" in str(md_file):
                continue
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                rel_path = md_file.relative_to(kb_path)
                knowledge[str(rel_path)] = content
    return knowledge

def build_system_prompt(knowledge_base: dict) -> str:
    """Build enhanced system prompt with knowledge base context"""
    base_prompt = """You are UWAY's financial compliance assistant specializing in:
- Anti-Money Laundering (AML) regulations
- Know Your Customer (KYC) requirements  
- Hong Kong Monetary Authority (HKMA) guidelines
- Securities and Futures Commission (SFC) rules
- FATF Recommendations

Always cite relevant regulatory frameworks when applicable. If uncertain, state that you're providing general guidance and recommend consulting a licensed compliance officer.

## Knowledge Base Context
Use the following reference materials to provide accurate, detailed answers:
"""
    
    # Add summarized knowledge base content
    for path, content in list(knowledge_base.items())[:5]:  # Limit to top 5 files
        base_prompt += f"\n\n### {path}\n{content[:500]}..."  # First 500 chars of each file
    
    return base_prompt

app = FastAPI(title="UWAY Chatbot Backend", version="1.0.0")

# Load knowledge base at startup
KNOWLEDGE_BASE = {}
SYSTEM_PROMPT = ""

# In-memory message history (use Redis in production)
conversation_history: dict = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown handlers"""
    global KNOWLEDGE_BASE, SYSTEM_PROMPT
    
    # Load knowledge base
    KNOWLEDGE_BASE = load_knowledge_base()
    print(f"Loaded {len(KNOWLEDGE_BASE)} knowledge base files")
    
    # Build system prompt with knowledge base context
    SYSTEM_PROMPT = build_system_prompt(KNOWLEDGE_BASE)
    
    app.state.router = ProviderRouter()
    yield

app.router.lifespan_context = lifespan


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    max_history: int = 10


class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = ["Gemini 2.5"]
    confidence_score: float = 0.9


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """Process a chat request with LLM routing"""
    try:
        # Build conversation history
        history = conversation_history.get(req.session_id, [])[-req.max_history:]
        
        messages = history + [{"role": "user", "content": req.message}]
        
        # Get response from LLM
        router = app.state.router
        answer = router.chat(messages, system_prompt=SYSTEM_PROMPT)
        
        # Update history
        conversation_history[req.session_id] = messages + [{"role": "assistant", "content": answer}]
        
        return ChatResponse(answer=answer)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "uway-chatbot-backend", "version": "1.0.0"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "UWAY Chatbot Backend API", "docs": "/docs"}