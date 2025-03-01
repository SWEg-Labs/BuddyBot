from models.dbSaveOperationResponse import DbSaveOperationResponse
from abc import ABC, abstractmethod
from dto.messageDtos import Message

class SaveMessageUseCase(ABC):
    @abstractmethod
    def save(self, message: Message) -> DbSaveOperationResponse:
        pass