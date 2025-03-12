from fastapi import Request
from fastapi.responses import JSONResponse

from models.question import Question
from services.chatService import ChatUseCase
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class ChatController:
    """
    Controller class to manage chat interactions.
    """

    def __init__(self, chat_use_case: ChatUseCase):
        """
        Initializes the ChatController with the given chat use case.
        Args:
            chat_use_case (ChatUseCase): The use case to process chat interactions.
        """
        self.__chat_use_case = chat_use_case

    async def get_answer(self, user_input: Request) -> dict[str, str] | JSONResponse:
        """
        Processes the user's input and fetches a response from the chat use case.
        Args:
            user_input (Request): The HTTP request containing the user's input message.
        Returns:
            dict[str, str] | JSONResponse: A dictionary containing the chatbot's response or a JSON response with an error message.
        Raises:
            Exception: If there is an error processing the user's input or fetching the response.
        """
        try:
            data = await user_input.json()
            user_message = data.get("message", "")

            if not user_message:
                return JSONResponse(content={"error": "Messaggio vuoto"}, status_code=400)
            
            # Converti il messaggio dell'utente in un oggetto Question
            user_message = Question(content=user_message)

            # Ottieni la risposta dal chatbot
            response = self.__chat_use_case.get_answer(user_message)
            response = response.get_content()

            return {"response": response}
        except Exception as e:
            logger.error(f"Error fetching response of ChatController: {e}")
            raise e
