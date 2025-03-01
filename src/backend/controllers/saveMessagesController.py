from use_cases.saveMessageUseCase import SaveMessageUseCase
from models.dbSaveOperationResponse import DbSaveOperationResponse

class SaveMessagesController:
    def __init__(self, SaveMessageUseCase: SaveMessageUseCase):
        self.SaveMessageUseCase = SaveMessageUseCase
    
    def save(self, message):
        dbSaveOperationResponse = DbSaveOperationResponse(self.SaveMessageUseCase.save(message))
        result = {"success": dbSaveOperationResponse.success, "message": dbSaveOperationResponse.message}
        return result