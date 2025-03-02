from use_cases.saveMessageUseCase import SaveMessageUseCase
from models.message import Message
from ports.saveMessagePort import SaveMessagePort
from models.dbSaveOperationResponse import DbSaveOperationResponse

class SaveMessageService(SaveMessageUseCase):
    """
    Service class responsible for saving messages.
    This class implements the SaveMessageUseCase interface and uses a SaveMessagePort
    to persist messages.
    """

    def __init__(self, saveMessagePort: SaveMessagePort):
        self.__saveMessagePort = saveMessagePort

    def save(self, message: Message) ->DbSaveOperationResponse:
        """
        Saves the given message using the save message port.
        Args:
            message (Message): The message object to be saved.
        Returns:
            The result of the save operation from the save message port.
        """
        return self.__saveMessagePort.save_message(message)