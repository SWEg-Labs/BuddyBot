from models.message import Message
from models.dbSaveOperationResponse import DbSaveOperationResponse

from use_cases.saveMessageUseCase import SaveMessageUseCase
from ports.saveMessagePort import SaveMessagePort
from utils.logger import logger

class SaveMessageService(SaveMessageUseCase):
    """
    Service class responsible for saving messages.
    This class implements the SaveMessageUseCase interface and uses a SaveMessagePort
    to persist messages.
    """

    def __init__(self, save_message_port: SaveMessagePort):
        """
        Initializes the SaveMessageService with the given SaveMessagePort.
        Args:
            save_message_port (SaveMessagePort): The port used to save messages.
        Raises:
            Exception: If there is an error initializing the SaveMessagePort.
        """
        try:
            self.__save_message_port = save_message_port
        except Exception as e:
            logger.error(f"Failed to initialize SaveMessageService: {e}")
            raise e

    def save(self, message: Message) -> DbSaveOperationResponse:
        """
        Saves the given message using the save message port.
        Args:
            message (Message): The message object to be saved.
        Returns:
            DbSaveOperationResponse: The result of the save operation from the save message port.
        Raises:
            Exception: If there is an error saving the message.
        """
        try:
            return self.__save_message_port.save_message(message)
        except Exception as e:
            logger.error(f"Failed to save message: {e}")
            raise e
