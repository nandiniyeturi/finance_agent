import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from financial_agent.agent import root_agent
import uuid

app = FastAPI(
    title="Financial Agent API",
    description="API for interacting with the Aura financial agent.",
    version="1.0.0",
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Global runner and session service
runner: Runner
session_service: InMemorySessionService

@app.on_event("startup")
async def startup_event():
    global runner, session_service
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="financial_agent",
        session_service=session_service,
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a message to the financial agent and get a response.
    """
    # For simplicity, we'll use a new session for each request.
    # For conversation history, the client would need to manage and send a session_id.
    user_id = "flutter_user"
    session_id = str(uuid.uuid4())
    await session_service.create_session(
        app_name="financial_agent", user_id=user_id, session_id=session_id
    )

    try:
        user_content = Content(role='user', parts=[Part(text=request.message)])

        events = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content
        )

        final_response = "Sorry, I could not process your request."
        async for event in events:
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
                break

        return ChatResponse(response=final_response)

    except Exception as e:
        print(f"An error occurred: {e}")
        return ChatResponse(response=f"An error occurred while processing your request: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
