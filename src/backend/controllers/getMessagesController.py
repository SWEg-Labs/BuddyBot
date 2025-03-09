from typing import List

from dto.messageDTO import MessageDTO, MessageSenderDTO
from models.quantity import Quantity
from use_cases.getMessagesUseCase import GetMessagesUseCase
from utils.logger import logger

class GetMessagesController:
    """
    Controller class to handle the retrieval of messages.
    Attributes:
        __get_messages_use_case (GetMessagesUseCase): The use case instance to retrieve messages.
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
            raise e

    def get_messages(self, quantity: dict[str, int]) -> List[MessageDTO]:
        """
        Retrieve a list of messages based on the provided quantity dictionary.
        Args:
            quantity (dict[str, int]): A dictionary with a single key-value pair where the key is a string and the value
            is the number of messages to retrieve.
        Returns:
            List[MessageDTO]: A list of messages, each represented as a MessageDTO instance.
        Raises:
            Exception: If an error occurs while retrieving messages.
        """
        try:
            quantity_value = list(quantity.values())[0]
            message_list = self.__get_messages_use_case.get_messages(Quantity(quantity_value))

            if not message_list:
                return []

            return_list = []
            for message in message_list:
                return_list.append(MessageDTO(content=message.get_content(), timestamp=message.get_timestamp(),
                                                    sender=MessageSenderDTO(message.get_sender().value)))
            return return_list
        except Exception as e:
            logger.error(f"An error occurred while retrieving messages: {e}")
            raise e
