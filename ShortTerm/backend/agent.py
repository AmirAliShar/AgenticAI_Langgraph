from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, AIMessage
from .Schema import State
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model="gemma2-9b-it", groq_api_key=GROQ_API_KEY)


def chatbot(state: State):
    history=state["messages"][-5:] # Keep last 5 messages for context
    prompt = [
        SystemMessage(content="""You are helpful AI assistant. 
        Remember the user's name if they tell you and use it in future responses.
        Be friendly and conversational.
        """),
    ] + history  
    
    response = llm.invoke(prompt).content
    return {"messages": [AIMessage(content=response)]}

workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)