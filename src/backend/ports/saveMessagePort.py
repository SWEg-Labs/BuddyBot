from abc import ABC, abstractmethod
from dto.messageDtos import Message
from models.dbSaveOperationResponse import DbSaveOperationResponse

class SaveMessagePort(ABC):
    @abstractmethod
    def save_message(self, message: Message)  -> DbSaveOperationResponse:
        pass