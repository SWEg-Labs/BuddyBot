from use_cases.saveMessageUseCase import SaveMessageUseCase
from dto.messageDtos import Message
from ports.saveMessagePort import SaveMessagePort

class SaveMessageService(SaveMessageUseCase):
    def __init__(self, saveMessagePort: SaveMessagePort):
        self.__saveMessagePort = saveMessagePort

    def save(self, message: Message):
        return self.__saveMessagePort.save_message(message)