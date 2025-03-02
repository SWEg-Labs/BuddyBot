from use_cases.getMessagesUseCase import GetMessagesUseCase
from dto.messageBaseModel import MessageBaseModel, MessageSenderBaseModel
from typing import List
from models.message import Message, MessageSender
from models.quantity import Quantity

class GetMessagesController:
    """
    Controller class to handle the retrieval of messages.
    """

    def __init__(self, getMessagesUseCase:GetMessagesUseCase) -> None :
        self.__getMessagesUseCase = getMessagesUseCase
    
    def get_messages(self, quantity: int) -> List[MessageBaseModel]:
        """
        Retrieve a list of (quantity) messages.
        Args:
            quantity (int): The number of messages to retrieve.
        Returns:
            List[MessageBaseModel]: A list of messages, each represented as a MessageBaseModel instance.
        """

        message_list = self.__getMessagesUseCase.get_messages(Quantity(quantity))
        return_list = []
        for message in message_list:
            return_list.append(MessageBaseModel(content=message.get_content(), timestamp=message.get_timestamp(), sender=MessageSenderBaseModel(message.get_sender().value)))

        return return_list