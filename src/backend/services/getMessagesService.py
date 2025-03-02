from use_cases.getMessagesUseCase import GetMessagesUseCase
from ports.getMessagesPort import GetMessagesPort
from models.quantity import Quantity
from models.message import Message
from typing import List

class GetMessagesService(GetMessagesUseCase):
    """
    Service class to handle the retrieval of messages.
    This class implements the GetMessagesUseCase interface and uses a 
    GetMessagesPort to fetch messages.
    """
    def __init__(self, getMessagesPort: GetMessagesPort):
        self.__getMessagesPort = getMessagesPort

    def get_messages(self, quantity: Quantity) -> List[Message]:
        """
        Retrieve a specified quantity of messages.
        Args:
            quantity (Quantity): The number of messages to retrieve.
        Returns:
            List[Message]: A list of retrieved messages.
        """

        return self.__getMessagesPort.get_messages(quantity)