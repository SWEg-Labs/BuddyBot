from datetime import datetime

from dto.messageDTO import MessageDTO
from models.message import Message, MessageSender
from use_cases.saveMessageUseCase import SaveMessageUseCase
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
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
        """
        self.__save_message_use_case = save_message_use_case

    def save(self, message: MessageDTO) -> dict[str, bool | str]:
        """
        Saves a message using the SaveMessageUseCase and returns the result.
        Args:
            message (MessageDTO): The message to be saved.
        Returns:
            dict: A dictionary containing the success status and message of the save operation.
        Raises:
            Exception: If there is an error during the save operation.
        """
        try:
            sender_str = message.get_sender()
            if sender_str == 'USER':
                sender = MessageSender.USER
            elif sender_str == 'CHATBOT':
                sender = MessageSender.CHATBOT
            else:
                raise ValueError(f"Invalid sender: {sender_str}")

            try:
                timestamp = datetime.strptime(message.get_timestamp(), '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError as ve:
                raise ValueError(f"Invalid timestamp format: {message.get_timestamp()}") from ve

            message = Message(
                content=message.get_content(),
                timestamp=timestamp,
                sender=sender
            )
            db_save_operation_response = self.__save_message_use_case.save(message)
            result = {"success": db_save_operation_response.get_success(), "message": db_save_operation_response.get_message()}
            return result
        except Exception as e:
            logger.error(f"Failed to save message: {e}")
            raise e
