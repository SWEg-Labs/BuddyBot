from enum import Enum
from datetime import datetime

class MessageSenderBaseModel(Enum):
    USER = "User"
    CHATBOT = "Chatbot"

class MessageBaseModel:
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