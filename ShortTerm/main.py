from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from langchain_core.messages import HumanMessage

from backend.agent import graph
from backend.Schema import ChatResponse, ChatRequest
app = FastAPI(title="Chatbot with Memory")



@app.post("/chat",response_model=ChatResponse)
async def chat_with_memory(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": "2"}}
        
        # LangGraph handles ALL memory automatically here
        result = graph.invoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config
        )
        
        ai_response = result["messages"][-1].content
        data={"response": ai_response}
        return JSONResponse(status_code=200,content=data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
