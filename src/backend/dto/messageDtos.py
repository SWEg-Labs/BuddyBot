from datetime import datetime
from enum import Enum

class MessageSender(Enum):
    USER = "User"
    CHATBOT = "Chatbot"

class Message:
    def __init__(self, content: str, timestamp: datetime, sender: MessageSender):
        self.__content = content
        self.__timestamp = timestamp
        self.__sender = sender

    def get_content(self):
        return self.__content
    
    def get_timestamp(self):
        return self.__timestamp
    
    def get_sender(self):
        return self.__sender
