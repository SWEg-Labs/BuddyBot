from abc import ABC, abstractmethod

from models.message import Message
from models.dbSaveOperationResponse import DbSaveOperationResponse

class SaveMessagePort(ABC):
    """
    Abstract base class for saving messages to a database.
    This class defines the interface for saving messages, which must be implemented
    by any concrete class that inherits from it.
    """

    @abstractmethod
    def save_message(self, message: Message)  -> DbSaveOperationResponse:
        """
        Saves a message to the database.
        Args:
            message (Message): The message object to be saved.
        Returns:
            DbSaveOperationResponse: The response object containing the result of the save operation.
        """
        pass
