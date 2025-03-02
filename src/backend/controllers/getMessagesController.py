from use_cases.getMessagesUseCase import GetMessagesUseCase
from dto.messageBaseModel import MessageBaseModel, MessageSenderBaseModel
from typing import List
from models.quantity import Quantity
from utils.logger import logger

class GetMessagesController:
    """
    Controller class to handle the retrieval of messages.
    """

    def __init__(self, get_messages_use_case: GetMessagesUseCase) :
        """
        Initialize the GetMessagesController with the provided use case.
            get_messages_use_case (GetMessagesUseCase): The use case instance to retrieve messages.
        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            self.__get_messages_use_case = get_messages_use_case
        except Exception as e:
            logger.error(f"An error occurred while initializing GetMessagesController: {e}")
            raise
    
    def get_messages(self, quantity: int) -> List[MessageBaseModel]:
        """
        Retrieve a list of (quantity) messages.
        Args:
            quantity (int): The number of messages to retrieve.
        Returns:
            List[MessageBaseModel]: A list of messages, each represented as a MessageBaseModel instance.
        Raises:
            Exception: If an error occurs while retrieving messages.
        """
        try:
            message_list = self.__get_messages_use_case.get_messages(Quantity(quantity))
            return_list = []
            for message in message_list:
                return_list.append(MessageBaseModel(content=message.get_content(), timestamp=message.get_timestamp(), sender=MessageSenderBaseModel(message.get_sender().value)))
            return return_list
        except Exception as e:
            logger.error(f"An error occurred while retrieving messages: {e}")
            return []
