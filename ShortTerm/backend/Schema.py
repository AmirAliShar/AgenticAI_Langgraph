from pydantic import BaseModel
from typing import TypedDict,Annotated,List
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[List, add_messages]

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
