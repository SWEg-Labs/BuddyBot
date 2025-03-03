from dto.messageBaseModel import MessageBaseModel
from models.message import Message, MessageSender
from use_cases.saveMessageUseCase import SaveMessageUseCase
from utils.logger import logger

class SaveMessageController:
    """
    A controller class responsible for saving messages.
    Attributes:
        __save_message_use_case (SaveMessageUseCase): The use case instance responsible for saving messages.
    """

    def __init__(self, save_message_use_case: SaveMessageUseCase):
        """
        Initializes the SaveMessagesController with the given SaveMessageUseCase.
        Args:
            save_message_use_case (SaveMessageUseCase): The use case instance responsible for saving messages.
        Raises:
            Exception: If there is an error during initialization.
        """
        try:
            self.__save_message_use_case = save_message_use_case
        except Exception as e:
            logger.error(f"Failed to initialize SaveMessagesController: {e}")
            raise

    def save(self, message: MessageBaseModel) -> dict[str, bool | str]:
        """
        Saves a message using the SaveMessageUseCase and returns the result.
        Args:
            message (MessageBaseModel): The message to be saved.
        Returns:
            dict: A dictionary containing the success status and message of the save operation.
        Raises:
            Exception: If there is an error during the save operation.
        """
        try:
            message = Message(
                content=message.get_content(),
                timestamp=message.get_timestamp(),
                sender=MessageSender[message.get_sender().name]
            )
            db_save_operation_response = self.__save_message_use_case.save(message)
            result = {"success": db_save_operation_response.get_success(), "message": db_save_operation_response.get_message()}
        except Exception as e:
            logger.error(f"Failed to save message: {e}")
            result = {"success": False, "message": str(e)}
        return result
