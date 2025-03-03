from enum import Enum
from datetime import datetime

class PostgresMessageSender(Enum):
    USER = "User"
    CHATBOT = "Chatbot"

class PostgresMessage:
    def __init__(self, content: str, timestamp: datetime, sender: PostgresMessageSender):
        self.__content = content
        self.__timestamp = timestamp
        self.__sender = sender

    def get_content(self) -> str:
        return self.__content
    
    def get_timestamp(self) -> datetime:
        return self.__timestamp
    
    def get_sender(self) -> PostgresMessageSender:
        return self.__sender

    def __eq__(self, other) -> bool:
        if not isinstance(other, PostgresMessage):
            return False
        return self.__content == other.get_content() and self.__timestamp == other.get_timestamp() and self.__sender == other.get_sender()