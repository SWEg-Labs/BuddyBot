from fastapi import Request
from fastapi.responses import JSONResponse

from models.question import Question
from services.chatService import ChatUseCase
from utils.logger import logger

class ChatController:
    """
    Controller class to manage chat interactions.
    """
    def __init__(self, chat_use_case: ChatUseCase):
        self.chat_use_case = chat_use_case

    async def get_answer(self, user_input: Request):
        """Processes user input and fetches a response from the chat use case."""
        try:
            data = await user_input.json()
            user_message = data.get("message", "")

            if not user_message:
                return JSONResponse(content={"error": "Messaggio vuoto"}, status_code=400)
            
            # Converti il messaggio dell'utente in un oggetto Question
            user_message = Question(content=user_message)

            # Ottieni la risposta dal chatbot
            response = self.chat_use_case.get_answer(user_message)
            response = response.content

            return {"response": response}
        except Exception as e:
            logger.error(f"Error fetching response: {e}")
            raise e
