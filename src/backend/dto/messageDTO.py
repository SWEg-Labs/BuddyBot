from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from utils.beartype_personalized import beartype_personalized

class MessageSenderDTO(str, Enum):
    USER = "USER"
    CHATBOT = "CHATBOT"

@beartype_personalized
class MessageDTO(BaseModel):
    def __init__(self, content: str, timestamp: datetime, sender: MessageSenderDTO):
        super().__init__(content=content, timestamp=timestamp, sender=sender)
        self.__content = content
        self.__timestamp = timestamp
        self.__sender = sender

    def get_content(self) -> str:
        return self.__content

    def get_timestamp(self) ->datetime:
        return self.__timestamp

    def get_sender(self) ->MessageSenderDTO:
        return self.__sender

    def __eq__(self, other)-> bool:
        if not isinstance(other, MessageDTO):
            return False
        return self.__content == other.get_content() and self.__timestamp == other.get_timestamp() and self.__sender == other.get_sender()
