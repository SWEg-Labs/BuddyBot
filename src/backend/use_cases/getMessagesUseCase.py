from models.message import Message
from typing import List
from abc import ABC, abstractmethod
from models.quantity import Quantity

class GetMessagesUseCase(ABC):
    """
    Abstract base class that defines the interface for retrieving messages.
    """

    @abstractmethod
    def get_messages(self, quantity: Quantity) -> List[Message]:
        """
        Retrieve a specified quantity of messages.
        Args:
            quantity (int): The number of messages to retrieve.
        Returns:
            List[Message]: A list of retrieved messages.
        """
        pass