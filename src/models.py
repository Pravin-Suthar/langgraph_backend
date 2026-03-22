from typing import Optional, Any
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class ChatMessage(BaseModel):
    """A single chat message from conversation history."""
    role: str  # "user" or "assistant"
    content: str


class QueryRequest(BaseModel):
    """Request model for country information queries."""
    question: str
    chat_history: list[ChatMessage] = Field(
        default_factory=list,
        max_length=6,
        description="Last few chat messages for context (sent by frontend)",
    )


class QueryResponse(BaseModel):
    """Response model for country information queries."""
    success: bool
    answer: Optional[str] = None
    country: Optional[str] = None
    fields_requested: Optional[list[str]] = None
    data: Optional[dict[str, Any]] = None
    error: Optional[str] = None


class AgentState(TypedDict, total=False):
    """LangGraph state for the country information agent."""
    question: str
    chat_history: list[dict]
    rewritten_question: str
    country: Optional[str]
    fields: list[str]
    api_data: Optional[dict]
    answer: Optional[str]
    error: Optional[str]
