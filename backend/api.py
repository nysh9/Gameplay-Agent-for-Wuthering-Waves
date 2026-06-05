from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal
import uvicorn

from agent import create_wuwa_agent, build_rag_prompt

app = FastAPI(title="Wuthering Waves Build Advisor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = create_wuwa_agent()


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    history = [m.model_dump() for m in req.messages]

    if history and history[-1]["role"] == "user":
        history[-1] = {
            "role": "user",
            "content": build_rag_prompt(history[-1]["content"]),
        }

    result = agent.invoke({"messages": history})
    final_message = result["messages"][-1]
    content = getattr(final_message, "content", "") or ""
    return ChatResponse(response=content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
