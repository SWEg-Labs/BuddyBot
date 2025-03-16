from beartype.typing import List

from dto.messageDTO import MessageDTO
from models.quantity import Quantity
from use_cases.getMessagesUseCase import GetMessagesUseCase
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
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
        """
        self.__get_messages_use_case = get_messages_use_case

    def get_messages(self, request_data: dict) -> List[MessageDTO]:
        """
        Retrieve a list of messages based on the provided request data with pagination support.
        Args:
            request_data (dict): A dictionary containing:
                - quantity (int): The number of messages to retrieve per page
                - page (int, optional): The page number, defaults to 1    
        Returns:
            List[MessageDTO]: A list of messages, each represented as a MessageDTO instance.
        Raises:
            Exception: If an error occurs while retrieving messages.
        """
        try:
            quantity_value = request_data.get("quantity", 50)
            page_value = request_data.get("page", 1)
            message_list = self.__get_messages_use_case.get_messages(
                Quantity(quantity_value), 
                page_value
            )
            if not message_list:
                return []
            
            return_list = []
            for message in message_list:
                timestamp_str = message.get_timestamp().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                sender_str = message.get_sender().name
                return_list.append(MessageDTO(
                    content=message.get_content(), 
                    timestamp=timestamp_str, 
                    sender=sender_str
                ))
            return return_list
        except Exception as e:
            logger.error(f"An error occurred while retrieving messages: {e}")
            raise e