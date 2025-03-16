from abc import ABC, abstractmethod
from beartype.typing import List

from models.message import Message
from models.quantity import Quantity

class GetMessagesPort(ABC):
    """
    GetMessagesPort is an abstract base class that defines the interface for retrieving messages.
    """
    @abstractmethod
    def get_messages(self, quantity: Quantity, page: int = 1) -> List[Message]:
        """
        Retrieve a specified quantity of messages with pagination support.
        Args:
            quantity (Quantity): The number of messages to retrieve per page.
            page (int, optional): The page number to retrieve, defaults to 1.
        Returns:
            List[Message]: A list of retrieved messages.
        """
        pass