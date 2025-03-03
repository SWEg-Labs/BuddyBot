from typing import List

from models.quantity import Quantity
from models.message import Message
from use_cases.getMessagesUseCase import GetMessagesUseCase
from ports.getMessagesPort import GetMessagesPort
from utils.logger import logger

class GetMessagesService(GetMessagesUseCase):
    """
    Service class to handle the retrieval of messages.
    This class implements the GetMessagesUseCase interface and uses a 
    GetMessagesPort to fetch messages.

    """
    def __init__(self, get_messages_port: GetMessagesPort):
        """
        Initialize the GetMessagesService with a GetMessagesPort.
        Args:
            get_messages_port (GetMessagesPort): The port to fetch messages.
        Raises:
            Exception: If initialization of GetMessagesService fails.
        """
        try:
            self.__get_messages_port = get_messages_port
        except Exception as e:
            logger.error(f"Failed to initialize GetMessagesService: {e}")
            raise

    def get_messages(self, quantity: Quantity) -> List[Message]:
        """
        Retrieve a specified quantity of messages.
        Args:
            quantity (Quantity): The number of messages to retrieve.
        Returns:
            List[Message]: A list of retrieved messages.
        Raises:
            Exception: If retrieval of messages fails.
        """
        try:
            return self.__get_messages_port.get_messages(quantity)
        except Exception as e:
            logger.error(f"Failed to retrieve messages: {e}")
            raise
