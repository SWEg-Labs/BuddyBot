from enum import Enum
from datetime import datetime

class PostgresMessageSender(Enum):
    USER = "User"
    CHATBOT = "Chatbot"

class PostgresMessage:
    def __init__(self, content: str, timestamp: datetime, sender: PostgresMessageSender):
        self.content = content
        self.timestamp = timestamp
        self.sender = sender

    def __eq__(self, other) -> bool:
        if not isinstance(other, PostgresMessage):
            return False
        return self.content == other.content and self.timestamp == other.timestamp and self.sender == other.sender