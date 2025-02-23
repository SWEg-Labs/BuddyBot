from fastapi import Request
from fastapi.responses import JSONResponse

from services.chatService import ChatUseCase
from utils.logger import logger

class ChatController:
    """
    Controller class to manage chat interactions.
    """
    def __init__(self, chat_use_case: ChatUseCase):
        self.chat_use_case = chat_use_case

    async def process_chat(self, user_input: Request):
        """Processes user input and fetches a response from the chat use case."""
        try:
            data = await user_input.json()
            user_message = data.get("message", "")

            if not user_message:
                return JSONResponse(content={"error": "Messaggio vuoto"}, status_code=400)

            # Ottieni la risposta dal chatbot
            response = self.chat_use_case.process_user_input(user_message)

            return {"response": response}
        except Exception as e:
            logger.error(f"Error fetching response: {e}")
            raise e
