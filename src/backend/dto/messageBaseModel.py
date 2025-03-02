from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class MessageSenderBaseModel(Enum, BaseModel):
    USER = "User"
    CHATBOT = "Chatbot"

class MessageBaseModel(BaseModel):

    def __init__(self, content: str, timestamp: datetime, sender: MessageSenderBaseModel):
        self.__content = content
        self.__timestamp = timestamp
        self.__sender = sender
    
    def get_content(self):
        return self.__content
    
    def get_timestamp(self):
        return self.__timestamp
    
    def get_sender(self):
        return self.__sender
    
    def __eq__(self, other)-> bool:
        if not isinstance(other, MessageBaseModel):
            return False
        return self.__content == other.__content and self.__timestamp == other.__timestamp and self.__sender == other.__sender