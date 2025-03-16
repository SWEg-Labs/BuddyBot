from abc import ABC, abstractmethod
from beartype.typing import List

from models.message import Message
from models.quantity import Quantity
from models.page import Page

class GetMessagesUseCase(ABC):
    """
    Abstract base class that defines the interface for retrieving messages.
    """

    @abstractmethod
    def get_messages(self, quantity: Quantity, page: Page) -> List[Message]:
        """
        Retrieve a specified quantity of messages with pagination support.
        Args:
            quantity (Quantity): The quantity of messages to retrieve.
            page (Page): The page number to retrieve.
        Returns:
            List[Message]: A list of retrieved messages.
        """
