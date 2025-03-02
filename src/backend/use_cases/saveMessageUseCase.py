from models.dbSaveOperationResponse import DbSaveOperationResponse
from abc import ABC, abstractmethod
from backend.models.message import Message

class SaveMessageUseCase(ABC):
    """
    Abstract base class for saving messages.
    This class defines the interface for saving messages to a database or any other storage system.
    Subclasses must implement the `save` method to handle the actual saving logic.
    """

    @abstractmethod
    def save(self, message: Message) -> DbSaveOperationResponse:
        """
        Saves the provided message to the database.
        Args:
            message (Message): The message object to be saved.
        Returns:
            DbSaveOperationResponse: The response object containing the result of the save operation.
        """

        pass