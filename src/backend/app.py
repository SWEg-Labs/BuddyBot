from typing import Dict, List
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dto.messageBaseModel import MessageBaseModel
from utils.dependency_injection import dependency_injection_frontend
from utils.logger import logger


# Inizializzazione dell'app FastAPI
app = FastAPI(
    title="BuddyBot API",
    description="Un'API per interagire con un chatbot che utilizza dati da GitHub, Jira e "\
    "Confluence.",
    version="1.0.0"
)

# Configurazione CORS per permettere richieste dal client Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dependencies = dependency_injection_frontend()
chat_controller = frontend_dependencies["chat_controller"]
save_message_controller = frontend_dependencies["save_message_controller"]
get_messages_controller = frontend_dependencies["get_messages_controller"]


@app.post("/api/chat", summary="Send a messagge to the chatbot", response_model=Dict[str, str])
async def chat(request: Request) -> Dict[str, str] | JSONResponse:
    """
    Endpoint to send a message to the chatbot and get a response.
    Args:
        request (Request): The JSON request containing the user's message.
    Returns:
        Union[Dict[str, str], JSONResponse]: 
            - If successful, returns a dictionary containing the chatbot's reply.
            - If an error occurs, returns a JSONResponse with error details and 500 status code
    Example Request JSON body:
        {
            "message": "Hello, chatbot!"
        }
    """
    try:
        return await chat_controller.get_answer(request)
    except Exception as e:
        error_message = f"Error processing chat request: {e}"
        logger.error(error_message)
        return JSONResponse(content={"status": "error", "message": error_message}, status_code=500)


@app.post("/api/save_message", summary="Save a message to the Postgres database", response_model=dict[str, bool | str])
async def save_message(message: MessageBaseModel) -> dict[str, bool | str] | JSONResponse:
    """
    Save a message to the Postgres database.
    Args:
        message (MessageBaseModel): The message to save.
    Returns:
        Union[dict[str, bool | str], JSONResponse]: 
            - If successful, returns a dictionary containing the operation status.
            - If an error occurs, returns a JSONResponse with error details and 500 status code
    """
    try:
        return save_message_controller.save(message)
    except Exception as e:
        error_message = f"Error saving the given message: {e}"
        logger.error(error_message)
        return JSONResponse(content={"status": "error", "message": error_message}, status_code=500)


@app.post("/api/get_messages", summary="Get messages from the Postgres database", response_model=List[MessageBaseModel])
async def get_messages(quantity: dict[str, int]) -> List[MessageBaseModel] | JSONResponse:
    """
    Retrieves a specified quantity of messages from the chat history.
    Args:
        quantity (dict[str, int]): A dictionary containing the number of messages to retrieve as value
    Returns:
        Union[List[MessageBaseModel], JSONResponse]: 
            - If successful, returns a list of MessageBaseModel objects containing the messages
            - If an error occurs, returns a JSONResponse with error details and 500 status code
    """
    try:
        return get_messages_controller.get_messages(quantity)
    except Exception as e:
        error_message = f"Error getting the previous messages: {e}"
        logger.error(error_message)
        return JSONResponse(content={"status": "error", "message": error_message}, status_code=500)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
