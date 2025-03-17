from beartype.typing import Dict, List, Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dto.messageDTO import MessageDTO
from dto.lastLoadOutcomeDTO import LastLoadOutcomeDTO
from utils.dependency_injection import dependency_injection_frontend
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized


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


# Inizializzazione dei controller necessari per la gestione delle richieste
frontend_dependencies = dependency_injection_frontend()

chat_controller = frontend_dependencies["chat_controller"]
get_last_load_outcome_controller = frontend_dependencies["get_last_load_outcome_controller"]
save_message_controller = frontend_dependencies["save_message_controller"]
get_messages_controller = frontend_dependencies["get_messages_controller"]
get_next_possible_questions_controller = frontend_dependencies["get_next_possible_questions_controller"]


@beartype_personalized
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


@beartype_personalized
@app.post("/api/get_next_possible_questions", summary="Get the next possible questions based on the last question and the last answer",
          response_model=Dict[str, str])
async def get_next_possible_questions(question_answer_quantity: Dict[str, Union[str, int]]) -> Dict[str, str] | JSONResponse:
    """
    Retrieves the next possible questions based on the provided question-answer-quantity data.
    Args:
        question_answer_quantity (Dict[str, Union[str, int]]): A dictionary containing the question, answer, and quantity.
    Returns:
        Union[Dict[str, str], JSONResponse]: 
            - If successful, returns a dictionary containing the next possible questions.
            - If an error occurs, returns a JSONResponse with error details and 500 status code
    """
    try:
        return get_next_possible_questions_controller.get_next_possible_questions(question_answer_quantity)
    except Exception as e:
        error_message = f"Error getting the next possible questions: {e}"
        logger.error(error_message)
        return JSONResponse(content={"status": "error", "message": error_message}, status_code=500)


@beartype_personalized
@app.post("/api/save_message", summary="Save a message to the Postgres database", response_model=dict[str, bool | str])
async def save_message(message: MessageDTO) -> dict[str, bool | str] | JSONResponse:
    """
    Save a message to the Postgres database.
    Args:
        message (MessageDTO): The message to save.
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


@beartype_personalized
@app.post("/api/get_messages", summary="Get messages from the Postgres database", response_model=List[MessageDTO])
async def get_messages(request_data: dict[str, int]) -> List[MessageDTO] | JSONResponse:
    """
    Retrieves a specified quantity of messages from the chat history with pagination support.
    Args:
        request_data (dict[str, int]): A dictionary containing:
            - quantity (int): The number of messages to retrieve per page
            - page (int), optional: The page number, defaults to 1
    Returns:
        Union[List[MessageDTO], JSONResponse]: 
            - If successful, returns a list of MessageDTO objects containing the messages
            - If an error occurs, returns a JSONResponse with error details and 500 status code
    """
    try:
        return get_messages_controller.get_messages(request_data)
    except Exception as e:
        error_message = f"Error getting the previous messages: {e}"
        logger.error(error_message)
        return JSONResponse(content={"status": "error", "message": error_message}, status_code=500)


@beartype_personalized
@app.post("/api/get_last_load_outcome", summary="Get the last load outcome", response_model=LastLoadOutcomeDTO)
async def get_last_load_outcome() -> LastLoadOutcomeDTO | JSONResponse:
    """
    Retrieves the last load outcome.
    Returns:
        Union[LastLoadOutcomeDTO, JSONResponse]: 
            - If successful, returns a LastLoadOutcomeDTO object containing the last load outcome.
            - If an error occurs, returns a JSONResponse with error details and 500 status code
    """
    try:
        return get_last_load_outcome_controller.get_last_load_outcome()
    except Exception as e:
        error_message = f"Error getting the last load outcome: {e}"
        logger.error(error_message)
        return JSONResponse(content={"status": "error", "message": error_message}, status_code=500)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
